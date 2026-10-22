#!/usr/bin/env python3
"""竞品公开数据监控模块。

功能：
    - 自定义添加竞品公开商品链接；
    - 按可配置周期（默认 6 小时）巡检；
    - 抓取公开价格、BSR/公开排名、公开差评；
    - 价格/排名超过阈值时生成本地 TXT 预警；
    - 从差评中提取高频痛点并分类输出 Markdown/JSON 报告。

边界：
    - 只读取竞品对外公开的商品页/公开评论页；
    - 不登录、不调用商家后台 API、不使用验证码识别或代理绕过；
    - 公开页面无法访问/结构变化/robots 禁止时跳过该链接并继续；
    - 演示默认使用本地公开快照，真实监控需 --mode live。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

PROJECT_ROOT = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import utils  # noqa: E402

logger = utils.get_logger("competitor_monitor")
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "competitor_monitor.yaml"
DEFAULT_INTERVAL_HOURS = 6.0


class MonitorError(RuntimeError):
    """监控模块异常。"""


class FetchError(MonitorError):
    """公开页面抓取失败。"""


class RobotsDenied(FetchError):
    """robots.txt 禁止抓取。"""


class ParseError(MonitorError):
    """页面结构变化，无法解析商品。"""


# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MonitorConfig:
    root: Path
    path: Path
    data: dict[str, Any]

    def get(self, dotted: str, default: Any = None) -> Any:
        return utils.deep_get(self.data, dotted, default)

    def section(self, name: str) -> dict[str, Any]:
        value = self.get(name, {})
        return dict(value) if isinstance(value, dict) else {}

    def resolve(self, dotted: str) -> Path:
        raw = self.get(dotted)
        if not raw:
            raise MonitorError(f"缺少路径配置: {dotted}")
        path = Path(str(raw)).expanduser()
        return path if path.is_absolute() else (self.root / path).resolve()


def load_config(path: str | Path | None = None, *, root: str | Path | None = None) -> MonitorConfig:
    project_root = Path(root).expanduser().resolve() if root else PROJECT_ROOT
    config_path = Path(path).expanduser() if path else project_root / "config" / "competitor_monitor.yaml"
    if not config_path.is_absolute():
        config_path = (project_root / config_path).resolve()
    data = utils.read_yaml(config_path)
    if not isinstance(data, dict):
        raise MonitorError(f"配置格式错误: {config_path}")
    if not data.get("paths") or not data.get("pain_categories"):
        raise MonitorError("配置缺少 paths 或 pain_categories")
    return MonitorConfig(root=project_root, path=config_path, data=data)


# ---------------------------------------------------------------------------
# 链接识别与注册表
# ---------------------------------------------------------------------------
PLATFORM_LABELS = {
    "amazon": "Amazon",
    "aliexpress": "AliExpress",
    "alibaba_1688": "1688",
    "generic": "Generic",
}
AMAZON_HOSTS = ("amazon.com", "amazon.co.uk", "amazon.de", "amazon.fr", "amazon.ca", "amazon.com.au")


def clean_url(url: str) -> str:
    text = str(url or "").strip()
    if not text:
        raise MonitorError("URL 为空")
    parts = urlsplit(text)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise MonitorError(f"无效 URL（需 http/https）: {url}")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def detect_platform(url: str) -> tuple[str, str]:
    parts = urlsplit(url)
    host = parts.netloc.lower().split("@")[-1].split(":")[0]
    path = parts.path
    if any(host == item or host.endswith("." + item) for item in AMAZON_HOSTS):
        match = re.search(r"/(?:dp|gp/product|product)/([A-Z0-9]{10})", path, re.IGNORECASE)
        return "amazon", match.group(1).upper() if match else ""
    if host.endswith("aliexpress.com"):
        match = re.search(r"/item/(\d+)", path)
        return "aliexpress", match.group(1) if match else ""
    if host.endswith("1688.com"):
        match = re.search(r"/offer/(\d+)", path)
        return "alibaba_1688", match.group(1) if match else ""
    return "generic", ""


def _competitor_id(url: str) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    return f"cmp-{digest}"


def _normalize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    url = clean_url(str(entry.get("url") or ""))
    platform = str(entry.get("platform") or "").lower()
    detected, product_id = detect_platform(url)
    if not platform or platform == "auto":
        platform = detected
    if platform not in PLATFORM_LABELS:
        raise MonitorError(f"不支持的 platform: {platform}")
    return {
        "id": str(entry.get("id") or _competitor_id(url)),
        "name": str(entry.get("name") or f"{PLATFORM_LABELS[platform]} 竞品"),
        "url": url,
        "platform": platform,
        "product_id": str(entry.get("product_id") or product_id),
        "enabled": bool(entry.get("enabled", True)),
        "demo": bool(entry.get("demo", False)),
        "added_at": str(entry.get("added_at") or utils.utc_now_iso()),
        "price_threshold_pct": entry.get("price_threshold_pct"),
        "price_threshold_abs": entry.get("price_threshold_abs"),
        "rank_threshold_abs": entry.get("rank_threshold_abs"),
    }


def load_registry(
    config: MonitorConfig,
    *,
    path: str | Path | None = None,
    create: bool = True,
) -> dict[str, Any]:
    registry_path = Path(path).expanduser().resolve() if path else config.resolve("paths.registry")
    if registry_path.exists():
        payload = utils.read_json(registry_path)
    elif create:
        payload = {
            "notice": "首次运行创建的注册表；demo 条目仅用于离线演示。",
            "competitors": [dict(item) for item in config.get("bootstrap", []) or []],
        }
        utils.write_json(registry_path, payload)
        logger.info("已创建竞品注册表: %s", registry_path)
    else:
        raise MonitorError(f"注册表不存在: {registry_path}")
    entries = payload.get("competitors")
    if not isinstance(entries, list):
        raise MonitorError(f"注册表格式错误: {registry_path}")
    normalized: list[dict[str, Any]] = []
    invalid: list[dict[str, str]] = []
    for item in entries:
        if not isinstance(item, dict):
            invalid.append({"id": "unknown", "error": "注册表条目不是对象"})
            continue
        try:
            normalized.append(_normalize_entry(item))
        except MonitorError as exc:
            invalid.append({"id": str(item.get("id") or item.get("url") or "unknown"), "error": str(exc)})
    payload["competitors"] = normalized
    payload["invalid_entries"] = invalid
    return payload


def save_registry(config: MonitorConfig, payload: dict[str, Any], path: str | Path | None = None) -> Path:
    registry_path = Path(path).expanduser().resolve() if path else config.resolve("paths.registry")
    return utils.write_json(registry_path, payload)


def add_competitor(
    config: MonitorConfig,
    *,
    url: str,
    name: str | None = None,
    platform: str = "auto",
    price_pct: float | None = None,
    price_abs: float | None = None,
    rank_abs: float | None = None,
    registry_path: str | Path | None = None,
) -> dict[str, Any]:
    payload = load_registry(config, path=registry_path)
    clean = clean_url(url)
    if any(item["url"] == clean for item in payload["competitors"]):
        raise MonitorError(f"链接已存在: {clean}")
    entry = _normalize_entry(
        {
            "url": clean,
            "name": name,
            "platform": platform,
            "price_threshold_pct": price_pct,
            "price_threshold_abs": price_abs,
            "rank_threshold_abs": rank_abs,
            "added_at": utils.utc_now_iso(),
            "demo": False,
        }
    )
    payload["competitors"].append(entry)
    save_registry(config, payload, registry_path)
    return entry


def remove_competitor(
    config: MonitorConfig,
    *,
    target: str | None = None,
    all_demo: bool = False,
    registry_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    payload = load_registry(config, path=registry_path)
    removed: list[dict[str, Any]] = []
    kept: list[dict[str, Any]] = []
    for item in payload["competitors"]:
        if all_demo and item.get("demo"):
            removed.append(item)
        elif target and (item["id"] == target or item["url"] == target):
            removed.append(item)
        else:
            kept.append(item)
    if not removed:
        raise MonitorError("没有匹配的竞品可删除")
    payload["competitors"] = kept
    save_registry(config, payload, registry_path)
    return removed


# ---------------------------------------------------------------------------
# 公开页面抓取
# ---------------------------------------------------------------------------
class PublicFetcher:
    def __init__(self, config: MonitorConfig) -> None:
        crawler = config.section("crawler")
        monitor = config.section("monitor")
        self.user_agent = str(crawler.get("user_agent", "OutdoorEssMonitor/0.1"))
        self.accept_language = str(crawler.get("accept_language", "en-US,en;q=0.9"))
        self.timeout = float(monitor.get("timeout_seconds", 20))
        self.delay = max(0.0, float(monitor.get("request_delay_seconds", 2.0)))
        self.respect_robots = bool(monitor.get("respect_robots", True))
        self._robots: dict[str, bool] = {}
        self._last: dict[str, float] = {}
        self._requests: Any = None
        self._session: Any = None

    def _session_or_raise(self) -> Any:
        if self._requests is None:
            try:
                import requests as _requests
            except ImportError as exc:  # pragma: no cover
                raise FetchError("live 模式需要 requests：pip install requests") from exc
            self._requests = _requests
            self._session = _requests.Session()
            self._session.headers.update(
                {
                    "User-Agent": self.user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": self.accept_language,
                }
            )
        return self._session

    def _robots_allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin in self._robots:
            return self._robots[origin]
        robots_url = f"{origin}/robots.txt"
        try:
            response = self._session_or_raise().get(robots_url, timeout=self.timeout)
        except Exception as exc:
            raise FetchError(f"读取 robots.txt 失败: {robots_url}: {exc}") from exc
        if response.status_code == 404:
            allowed = True
        elif response.status_code in {401, 403}:
            allowed = False
        elif not 200 <= response.status_code < 300:
            allowed = False
        else:
            parser = RobotFileParser()
            parser.set_url(robots_url)
            parser.parse(response.text.splitlines())
            allowed = parser.can_fetch(self.user_agent, url)
        self._robots[origin] = allowed
        return allowed

    def get(self, url: str) -> str:
        if not self._robots_allowed(url):
            raise RobotsDenied(f"robots.txt 禁止抓取，已跳过: {url}")
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        wait = self.delay - (time.monotonic() - self._last.get(origin, 0.0))
        if wait > 0:
            time.sleep(wait)
        try:
            response = self._session_or_raise().get(url, timeout=self.timeout, allow_redirects=True)
        except Exception as exc:
            raise FetchError(f"请求失败: {url}: {exc}") from exc
        self._last[origin] = time.monotonic()
        if response.status_code in {401, 403, 429, 503}:
            raise FetchError(f"公开页面拒绝访问（HTTP {response.status_code}），不绕过: {url}")
        if response.status_code >= 400:
            raise FetchError(f"HTTP {response.status_code}: {url}")
        text = response.text or ""
        lowered = text[:5000].lower()
        if "captcha" in lowered or "robot check" in lowered or "verify you are human" in lowered:
            raise FetchError(f"页面要求验证码/人机校验，已跳过: {url}")
        return text

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None


def _soup(html: str) -> Any:
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:  # pragma: no cover
        raise FetchError("live 模式需要 beautifulsoup4：pip install beautifulsoup4") from exc
    return BeautifulSoup(html, "html.parser")


def _num(value: Any, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(value))
    return float(match.group(0).replace(",", "")) if match else default


def _int(value: Any, default: int = 0) -> int:
    parsed = _num(value)
    return int(round(parsed)) if parsed is not None else default


# ---------------------------------------------------------------------------
# 公开商品页解析
# ---------------------------------------------------------------------------
def _first_text(soup: Any, selectors: Iterable[str]) -> str:
    for selector in selectors:
        node = soup.select_one(selector)
        if node:
            text = node.get_text(" ", strip=True)
            if text:
                return text
    return ""


def _walk_jsonld(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        types = value.get("@type")
        if types == "Product" or (isinstance(types, list) and "Product" in types):
            yield value
        for child in value.values():
            yield from _walk_jsonld(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_jsonld(child)


def _jsonld_product(soup: Any) -> dict[str, Any]:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            payload = json.loads(script.string or script.get_text() or "")
        except (TypeError, ValueError):
            continue
        for item in _walk_jsonld(payload):
            return item
    return {}


def _currency_for(url: str, platform: str, default: str = "USD") -> str:
    host = urlsplit(url).netloc.lower()
    if platform == "alibaba_1688" or "1688.com" in host:
        return "CNY"
    if "amazon.co.uk" in host or ".co.uk" in host:
        return "GBP"
    if "amazon.de" in host or "amazon.fr" in host or ".de" in host or ".fr" in host:
        return "EUR"
    return default


def _price_from_html(soup: Any, url: str, platform: str) -> tuple[float | None, str]:
    product = _jsonld_product(soup)
    offers = product.get("offers") if product else None
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    if isinstance(offers, dict):
        price = _num(offers.get("price", offers.get("lowPrice")))
        if price and price > 0:
            return price, str(offers.get("priceCurrency") or _currency_for(url, platform)).upper()
    for meta in soup.find_all("meta"):
        prop = str(meta.get("property") or meta.get("name") or "").lower()
        if prop in {"product:price:amount", "og:price:amount"}:
            price = _num(meta.get("content"))
            if price and price > 0:
                currency_meta = soup.find("meta", attrs={"property": "product:price:currency"})
                currency = str(currency_meta.get("content") if currency_meta else _currency_for(url, platform)).upper()
                return price, currency
    selectors = (
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        ".a-price .a-offscreen",
        "span.price",
        "[class*='price-current']",
        "[class*='product-price']",
        "[class*='price']",
    )
    for selector in selectors:
        node = soup.select_one(selector)
        if node:
            price = _num(node.get_text(" ", strip=True))
            if price and price > 0:
                return price, _currency_for(url, platform)
    return None, _currency_for(url, platform)


def _bsr_from_html(soup: Any) -> tuple[int | None, str]:
    text = soup.get_text(" ", strip=True)
    patterns = (
        r"Best Sellers Rank:?\s*#?([\d,]+)\s+in\s+([^#<()]{2,100})",
        r"#([\d,]+)\s+in\s+([A-Za-z][^#<()]{2,100})",
        r"排名第?\s*([\d,]+)\s*名",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            bsr = _int(match.group(1))
            category = re.sub(r"\s+", " ", match.group(2)).strip(" :-,")
            return bsr, category
    return None, ""


def _review_from_node(node: Any) -> dict[str, Any] | None:
    text = node.get_text(" ", strip=True)
    if len(text) < 8:
        return None
    rating_text = _first_text(
        node,
        ("span.a-icon-alt", "[class*='star']", "[class*='rating']", "[data-hook*='rating']"),
    )
    rating_match = re.search(r"([1-5](?:\.\d)?)", rating_text) if rating_text else None
    title = _first_text(node, ("[data-hook='review-title']", "[class*='title']"))
    body = _first_text(
        node,
        (
            "[data-hook='review-body']",
            "[class*='review-content']",
            "[class*='reviewContent']",
            "[class*='content']",
            "[class*='body']",
        ),
    )
    if not body:
        body = text
    return {
        "rating": int(float(rating_match.group(1))) if rating_match else None,
        "title": re.sub(r"\s+", " ", title).strip()[:200],
        "body": re.sub(r"\s+", " ", body).strip()[:1500],
        "date": _first_text(node, ("[data-hook='review-date']", "[class*='date']")),
        "author": _first_text(node, ("[class*='author']", "[class*='user']", "[class*='profile']")),
    }


def _reviews_from_html(soup: Any) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    product = _jsonld_product(soup)
    raw_reviews = product.get("review") if product else None
    if isinstance(raw_reviews, dict):
        raw_reviews = [raw_reviews]
    if isinstance(raw_reviews, list):
        for item in raw_reviews:
            if not isinstance(item, dict):
                continue
            rating = item.get("reviewRating") or {}
            author = item.get("author") or {}
            reviews.append(
                {
                    "rating": _int(rating.get("ratingValue")) if isinstance(rating, dict) else None,
                    "title": str(item.get("name") or ""),
                    "body": str(item.get("reviewBody") or ""),
                    "date": str(item.get("datePublished") or ""),
                    "author": str(author.get("name") or "") if isinstance(author, dict) else "",
                }
            )
    selectors = (
        "[data-hook='review']",
        "div.review",
        "[class*='review-item']",
        "[class*='reviewItem']",
        "[class*='comment-item']",
        "[class*='commentItem']",
        "[class*='offer-review']",
    )
    for selector in selectors:
        for node in soup.select(selector):
            parsed = _review_from_node(node)
            if parsed:
                reviews.append(parsed)
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for review in reviews:
        key = (str(review.get("body") or "") + str(review.get("title") or "")).lower()[:300]
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(review)
    return deduped


class ProductParser:
    """Amazon / AliExpress / 1688 / Generic 公开商品页解析器。"""

    def parse(
        self,
        *,
        url: str,
        platform: str,
        html: str,
        review_html: str | None = None,
    ) -> dict[str, Any]:
        soup = _soup(html)
        product = _jsonld_product(soup)
        title = _first_text(
            soup,
            ("#productTitle", "h1[itemprop='name']", "h1", "meta[property='og:title']"),
        )
        if not title and product:
            title = str(product.get("name") or "")
        if not title:
            meta = soup.find("meta", attrs={"property": "og:title"})
            title = str(meta.get("content") if meta else "").strip()
        title = re.sub(r"\s+", " ", title).strip()[:300]
        price, currency = _price_from_html(soup, url, platform)
        bsr, bsr_category = _bsr_from_html(soup)
        rating = None
        review_count = 0
        if product:
            aggregate = product.get("aggregateRating") or {}
            if isinstance(aggregate, dict):
                rating = _num(aggregate.get("ratingValue"))
                review_count = _int(aggregate.get("reviewCount") or aggregate.get("ratingCount"))
        if rating is None:
            rating_text = _first_text(soup, ("span.a-icon-alt", "[class*='rating']", "[class*='star']"))
            rating = _num(rating_text)
        reviews = _reviews_from_html(soup)
        if review_html:
            review_soup = _soup(review_html)
            reviews.extend(_reviews_from_html(review_soup))
        # 去重并保留有实际内容的评论
        deduped: list[dict[str, Any]] = []
        seen: set[str] = set()
        for review in reviews:
            body = re.sub(r"\s+", " ", str(review.get("body") or "")).strip()
            if len(body) < 8:
                continue
            key = body.lower()[:300]
            if key in seen:
                continue
            seen.add(key)
            review["body"] = body[:1500]
            deduped.append(review)
        if price is None and bsr is None:
            raise ParseError("公开页面未解析到价格或 BSR，可能页面结构变化/需要登录")
        if review_count <= 0:
            review_count = len(deduped)
        return {
            "title": title or "(untitled public listing)",
            "price": price,
            "currency": currency,
            "bsr": bsr,
            "bsr_category": bsr_category,
            "rating": round(rating, 2) if rating is not None else None,
            "review_count": review_count,
            "reviews": deduped,
            "source_url": url,
            "platform": platform,
            "captured_at": utils.utc_now_iso(),
        }


def _load_fixture(path: Path) -> dict[str, Any]:
    payload = utils.read_json(path)
    if not isinstance(payload, dict) or not isinstance(payload.get("snapshots"), dict):
        raise MonitorError(f"公开快照格式错误: {path}")
    return payload


def _fixture_snapshot(fixture: dict[str, Any], competitor_id: str) -> dict[str, Any]:
    item = fixture["snapshots"].get(competitor_id)
    if not isinstance(item, dict):
        raise ParseError(f"离线快照不包含该竞品: {competitor_id}")
    snapshot = dict(item)
    snapshot.setdefault("source_url", "")
    snapshot.setdefault("platform", "")
    snapshot.setdefault("captured_at", fixture.get("captured_at") or utils.utc_now_iso())
    snapshot.setdefault("reviews", [])
    return snapshot


def collect_snapshot(
    competitor: dict[str, Any],
    config: MonitorConfig,
    *,
    mode: str,
    fixture_path: str | Path | None = None,
    fetcher: PublicFetcher | None = None,
) -> dict[str, Any]:
    mode = mode.lower()
    if mode == "live" and competitor.get("demo"):
        raise FetchError("demo 条目在 live 模式自动跳过；请 add 真实公开链接")
    fixture_file = Path(fixture_path).expanduser().resolve() if fixture_path else config.resolve("fixture.path")
    if mode == "offline":
        return _fixture_snapshot(_load_fixture(fixture_file), competitor["id"])
    if mode == "live":
        return _collect_live(competitor, config, fetcher or PublicFetcher(config))
    if mode == "auto":
        if competitor.get("demo"):
            return _fixture_snapshot(_load_fixture(fixture_file), competitor["id"])
        try:
            return _collect_live(competitor, config, fetcher or PublicFetcher(config))
        except (FetchError, ParseError) as exc:
            logger.warning("live 失败，尝试离线快照：%s：%s", competitor["id"], exc)
            return _fixture_snapshot(_load_fixture(fixture_file), competitor["id"])
    raise MonitorError(f"未知 mode: {mode}")


def _collect_live(
    competitor: dict[str, Any],
    config: MonitorConfig,
    fetcher: PublicFetcher,
) -> dict[str, Any]:
    parser = ProductParser()
    url = competitor["url"]
    html = fetcher.get(url)
    review_html: str | None = None
    if competitor["platform"] == "amazon":
        asin = competitor.get("product_id") or ""
        if asin:
            review_url = f"https://{urlsplit(url).netloc}/product-reviews/{asin}?filterByStar=critical&pageNumber=1"
            try:
                review_html = fetcher.get(review_url)
            except FetchError as exc:
                logger.warning("公开评论页不可用，仅使用商品页评论：%s：%s", competitor["id"], exc)
    snapshot = parser.parse(url=url, platform=competitor["platform"], html=html, review_html=review_html)
    snapshot["source_url"] = url
    snapshot["platform"] = competitor["platform"]
    max_reviews = int(config.get("monitor.max_reviews_per_competitor", 20))
    snapshot["reviews"] = snapshot.get("reviews", [])[:max_reviews]
    return snapshot


# ---------------------------------------------------------------------------
# 状态、快照与预警
# ---------------------------------------------------------------------------
@dataclass
class Alert:
    competitor_id: str
    competitor_name: str
    url: str
    platform: str
    kind: str
    message: str
    old_value: Any
    new_value: Any
    delta: Any
    captured_at: str


def _price_threshold(competitor: dict[str, Any], config: MonitorConfig, key: str, default: float) -> float:
    value = competitor.get(key)
    return float(value) if value not in (None, "") else float(config.get(f"monitor.{key}", default))


def detect_alerts(
    competitor: dict[str, Any],
    previous: dict[str, Any] | None,
    current: dict[str, Any],
    config: MonitorConfig,
) -> list[Alert]:
    if not previous:
        return []
    alerts: list[Alert] = []
    old_price = _num(previous.get("price"))
    new_price = _num(current.get("price"))
    if old_price and new_price and previous.get("currency") == current.get("currency"):
        pct = abs(new_price - old_price) / old_price * 100
        pct_threshold = _price_threshold(competitor, config, "price_threshold_pct", 3.0)
        abs_threshold = _price_threshold(competitor, config, "price_threshold_abs", 5.0)
        if pct >= pct_threshold or abs(new_price - old_price) >= abs_threshold:
            direction = "下降" if new_price < old_price else "上涨"
            alerts.append(
                Alert(
                    competitor_id=competitor["id"],
                    competitor_name=competitor["name"],
                    url=competitor["url"],
                    platform=competitor["platform"],
                    kind="PRICE",
                    message=(
                        f"价格{direction}：{current.get('currency', '')} {old_price:.2f} → "
                        f"{new_price:.2f}（{pct:.2f}%）"
                    ),
                    old_value=old_price,
                    new_value=new_price,
                    delta=round(new_price - old_price, 2),
                    captured_at=str(current.get("captured_at") or utils.utc_now_iso()),
                )
            )
    old_rank = _int(previous.get("bsr"), 0)
    new_rank = _int(current.get("bsr"), 0)
    if old_rank and new_rank and previous.get("bsr_category") == current.get("bsr_category"):
        delta = old_rank - new_rank
        threshold = _price_threshold(competitor, config, "rank_threshold_abs", 20.0)
        if abs(delta) >= threshold:
            direction = "改善" if delta > 0 else "下滑"
            alerts.append(
                Alert(
                    competitor_id=competitor["id"],
                    competitor_name=competitor["name"],
                    url=competitor["url"],
                    platform=competitor["platform"],
                    kind="BSR",
                    message=(
                        f"BSR {direction}：#{old_rank:,} → #{new_rank:,}"
                        f"（变化 {abs(delta):,} 位，类目：{current.get('bsr_category') or '-'}）"
                    ),
                    old_value=old_rank,
                    new_value=new_rank,
                    delta=delta,
                    captured_at=str(current.get("captured_at") or utils.utc_now_iso()),
                )
            )
    return alerts


class StateStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = {"competitors": {}}
        if path.exists():
            loaded = utils.read_json(path, default={})
            if isinstance(loaded, dict):
                self.data = loaded
                self.data.setdefault("competitors", {})

    def previous(self, competitor_id: str) -> dict[str, Any] | None:
        value = self.data["competitors"].get(competitor_id)
        return dict(value) if isinstance(value, dict) else None

    def update(self, competitor_id: str, snapshot: dict[str, Any]) -> None:
        previous = self.previous(competitor_id) or {}
        previous.update(
            {
                "title": snapshot.get("title") or previous.get("title"),
                "price": snapshot.get("price") if snapshot.get("price") is not None else previous.get("price"),
                "currency": snapshot.get("currency") or previous.get("currency"),
                "bsr": snapshot.get("bsr") if snapshot.get("bsr") is not None else previous.get("bsr"),
                "bsr_category": snapshot.get("bsr_category") or previous.get("bsr_category"),
                "rating": snapshot.get("rating") if snapshot.get("rating") is not None else previous.get("rating"),
                "review_count": snapshot.get("review_count")
                if snapshot.get("review_count") is not None
                else previous.get("review_count"),
                "last_seen": snapshot.get("captured_at") or utils.utc_now_iso(),
            }
        )
        self.data["competitors"][competitor_id] = previous

    def save(self) -> Path:
        return utils.write_json(self.path, self.data)


def write_alerts(
    alerts: list[Alert],
    output_dir: Path,
    run_id: str,
    *,
    warning_text: str = "",
) -> list[Path]:
    alert_dir = utils.ensure_dir(output_dir)
    paths: list[Path] = []
    for alert in alerts:
        slug = utils.safe_filename(f"{alert.competitor_id}_{alert.kind}_{run_id}")
        path = alert_dir / f"{slug}.txt"
        content = (
            "[竞品监控预警]\n"
            f"生成时间：{utils.utc_now_iso()}\n"
            f"竞品名称：{alert.competitor_name}\n"
            f"竞品 ID：{alert.competitor_id}\n"
            f"平台：{alert.platform}\n"
            f"链接：{alert.url}\n"
            f"预警类型：{alert.kind}\n"
            f"变动：{alert.message}\n"
            f"旧值：{alert.old_value}\n"
            f"新值：{alert.new_value}\n"
            f"数据时间：{alert.captured_at}\n"
            "备注：仅基于公开页面数据，需人工复核价格口径/排名类目。\n"
        )
        utils.write_text(path, content)
        paths.append(path)
    latest = alert_dir / "latest_alerts.txt"
    if alerts:
        blocks = [
            (
                f"[{item.kind}] {item.competitor_name}\n"
                f"URL: {item.url}\n"
                f"{item.message}\n"
                f"数据时间: {item.captured_at}\n"
            )
            for item in alerts
        ]
        body = f"竞品监控预警汇总 / {utils.utc_now_iso()}\n\n" + "\n".join(blocks)
    else:
        body = f"竞品监控预警汇总 / {utils.utc_now_iso()}\n\n本轮无价格/排名预警。\n"
    if warning_text:
        body += f"\n{warning_text}\n"
    utils.write_text(latest, body)
    return paths


# ---------------------------------------------------------------------------
# 差评痛点分析
# ---------------------------------------------------------------------------
class PainPointAnalyzer:
    def __init__(self, config: MonitorConfig) -> None:
        self.config = config
        self.threshold = int(config.get("monitor.negative_rating_threshold", 2))
        self.max_examples = int(config.get("monitor.max_pain_examples", 3))
        self.categories = [
            item
            for item in (config.get("pain_categories", []) or [])
            if isinstance(item, dict) and item.get("id")
        ]
        self.stopwords = {str(x).lower() for x in (config.get("stopwords", []) or [])}

    def analyze(
        self,
        reviews: list[dict[str, Any]],
        competitors: list[dict[str, Any]],
        *,
        run_id: str,
        failures: list[dict[str, str]],
    ) -> dict[str, Any]:
        negatives = [
            review
            for review in reviews
            if review.get("rating") is not None and int(review["rating"]) <= self.threshold
        ]
        category_hits: dict[str, list[dict[str, Any]]] = defaultdict(list)
        per_competitor: dict[str, dict[str, Any]] = {
            item["id"]: {"id": item["id"], "name": item["name"], "negative_reviews": 0, "categories": Counter()}
            for item in competitors
        }
        for review in negatives:
            text = f"{review.get('title', '')} {review.get('body', '')}".lower()
            matched = [
                str(category["id"])
                for category in self.categories
                if any(self._match(keyword, text) for keyword in category.get("keywords", []))
            ]
            if not matched:
                matched = ["other"]
            for category_id in matched:
                category_hits[category_id].append(review)
            competitor = per_competitor.get(str(review.get("competitor_id")))
            if competitor:
                competitor["negative_reviews"] += 1
                competitor["categories"].update(matched)

        labels = {str(item["id"]): str(item.get("label") or item["id"]) for item in self.categories}
        labels["other"] = "其他/未分类"
        category_stats: list[dict[str, Any]] = []
        for category_id, items in category_hits.items():
            names = sorted({str(item.get("competitor_name") or item.get("competitor_id")) for item in items})
            category_stats.append(
                {
                    "id": category_id,
                    "label": labels.get(category_id, category_id),
                    "mentions": len(items),
                    "share_pct": round(len(items) / len(negatives) * 100, 2) if negatives else 0.0,
                    "competitors": names,
                    "examples": [
                        {
                            "competitor": item.get("competitor_name") or item.get("competitor_id"),
                            "rating": item.get("rating"),
                            "quote": self._quote(str(item.get("body") or item.get("title") or "")),
                        }
                        for item in items[: self.max_examples]
                    ],
                }
            )
        category_stats.sort(key=lambda item: (-item["mentions"], item["label"]))
        competitor_rows = []
        for item in per_competitor.values():
            competitor_rows.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "negative_reviews": item["negative_reviews"],
                    "top_categories": [
                        {"id": key, "label": labels.get(key, key), "mentions": value}
                        for key, value in item["categories"].most_common(3)
                    ],
                }
            )
        competitor_rows.sort(key=lambda item: -item["negative_reviews"])
        top_terms = self._top_terms(negatives)
        report = {
            "run_id": run_id,
            "generated_at": utils.utc_now_iso(),
            "policy": "只分析公开可见差评；样本非全量，不代表真实整体满意度。",
            "total_reviews": len(reviews),
            "negative_reviews": len(negatives),
            "negative_rating_threshold": self.threshold,
            "categories": category_stats,
            "per_competitor": competitor_rows,
            "top_terms": top_terms,
            "failures": failures,
            "recommendations": [self._action(item["id"]) for item in category_stats[:3]],
        }
        report["markdown"] = self._markdown(report)
        return report

    @staticmethod
    def _match(keyword: str, text: str) -> bool:
        phrase = str(keyword).strip().lower()
        if not phrase:
            return False
        return bool(re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", text))

    def _top_terms(self, reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
        counter: Counter[str] = Counter()
        for review in reviews:
            text = f"{review.get('title', '')} {review.get('body', '')}".lower()
            for token in re.findall(r"[a-z][a-z'-]{3,}", text):
                token = token.strip("'-")
                if token and token not in self.stopwords:
                    counter[token] += 1
        return [{"term": term, "count": count} for term, count in counter.most_common(15)]

    def _quote(self, text: str) -> str:
        max_chars = int(self.config.get("monitor.max_alert_quote_chars", 300))
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars] + ("…" if len(text) > max_chars else "")

    def _action(self, category_id: str) -> str:
        mapping = {
            "battery_life": "在详情页明确可用容量、测试负载与续航条件，并优化电芯/逆变效率。",
            "charging_speed": "标注充电功率与 0-80% 时间，提供快充配件与清晰说明。",
            "solar_charging": "标注太阳能输入上限、MPPT 方案与真实日照条件，避免固定时长承诺。",
            "noise": "优化风扇曲线与低噪模式，标注测试距离和负载条件。",
            "power_output": "明确持续/峰值功率与兼容设备，增加过载保护说明。",
            "weight_portability": "强化单人搬运与后备箱场景，提供拉杆包/折叠车等配件。",
            "build_quality": "加强外壳、接口与包装质检，补充跌落/老化测试说明。",
            "display_app": "校准电量显示与 App 连接，提供固件更新与重置指引。",
            "heat_safety": "完善热管理与温控说明，避免长时间满载，明确安全边界。",
            "shipping_packaging": "加固包装与电池运输标签，明确发货时效。",
            "customer_service": "建立响应 SLA、保修与退换流程，缩短首次回复时间。",
            "instructions": "重做快速上手卡/视频，覆盖首次充电、接口与过载处理。",
            "compatibility": "提供插头、接口与设备功率兼容表，减少误购。",
            "value_price": "用每 Wh 成本、循环寿命与质保解释价值，而非单纯低价。",
            "other": "抽取更多负评样本并人工复核，补充细分类别。",
        }
        return mapping.get(category_id, "人工复核该类别的高频负评并制定改进动作。")

    def _markdown(self, report: dict[str, Any]) -> str:
        lines = [
            "# 竞品公开差评痛点分析报告",
            "",
            f"- 运行 ID：`{report['run_id']}`",
            f"- 生成时间：{report['generated_at']}",
            f"- 公开评论样本：{report['total_reviews']} 条",
            f"- 差评样本（≤{report['negative_rating_threshold']} 星）：{report['negative_reviews']} 条",
            "- 数据边界：仅公开页面；样本非全量，不代表整体满意度。",
            "",
            "## 1. 高频痛点总览",
            "",
            "| 排名 | 痛点分类 | 提及次数 | 占差评比例 | 涉及竞品 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for index, item in enumerate(report["categories"], start=1):
            lines.append(
                f"| {index} | {item['label']} | {item['mentions']} | {item['share_pct']:.1f}% | "
                f"{'、'.join(item['competitors']) or '-'} |"
            )
        lines.extend(["", "## 2. 分类样例", ""])
        for item in report["categories"]:
            lines.append(f"### {item['label']}（{item['mentions']} 次）")
            for example in item["examples"]:
                lines.append(
                    f"- [{example['competitor']} / {example['rating']}★] “{example['quote']}”"
                )
            lines.append("")
        lines.extend(
            [
                "## 3. 竞品对比",
                "",
                "| 竞品 | 差评数 | Top 痛点 |",
                "| --- | --- | --- |",
            ]
        )
        for item in report["per_competitor"]:
            top = "；".join(
                f"{entry['label']} {entry['mentions']}" for entry in item["top_categories"]
            ) or "-"
            lines.append(f"| {item['name']} | {item['negative_reviews']} | {top} |")
        lines.extend(
            [
                "",
                "## 4. 高频词",
                "",
                "、".join(f"{item['term']}({item['count']})" for item in report["top_terms"]) or "-",
                "",
                "## 5. 建议动作",
                "",
            ]
        )
        lines.extend(f"{index}. {action}" for index, action in enumerate(report["recommendations"], start=1))
        if report["failures"]:
            lines.extend(["", "## 6. 抓取失败/跳过", ""])
            for failure in report["failures"]:
                lines.append(f"- `{failure.get('id')}`：{failure.get('error')}")
        lines.extend(
            [
                "",
                "---",
                "",
                "*本报告由公开数据规则分析生成，不构成法律、认证或商业决策结论。*",
                "",
            ]
        )
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 监控引擎
# ---------------------------------------------------------------------------
def _display_path(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


class MonitorEngine:
    def __init__(
        self,
        config: MonitorConfig,
        *,
        registry_path: str | Path | None = None,
        state_path: str | Path | None = None,
        output_dir: str | Path | None = None,
        fixture_path: str | Path | None = None,
    ) -> None:
        self.config = config
        self.registry_path = Path(registry_path).expanduser().resolve() if registry_path else config.resolve("paths.registry")
        self.state_path = Path(state_path).expanduser().resolve() if state_path else config.resolve("paths.state")
        self.fixture_path = str(fixture_path) if fixture_path else None
        if output_dir:
            base = Path(output_dir).expanduser().resolve()
            self.snapshots_dir = utils.ensure_dir(base / "snapshots")
            self.alerts_dir = utils.ensure_dir(base / "alerts")
            self.reports_dir = utils.ensure_dir(base / "reports")
            self.output_base = base
        else:
            self.snapshots_dir = utils.ensure_dir(config.resolve("paths.snapshots_dir"))
            self.alerts_dir = utils.ensure_dir(config.resolve("paths.alerts_dir"))
            self.reports_dir = utils.ensure_dir(config.resolve("paths.reports_dir"))
            self.output_base = self.reports_dir.parent
        self.analyzer = PainPointAnalyzer(config)

    def run(self, *, mode: str | None = None, fixture_path: str | Path | None = None) -> dict[str, Any]:
        selected_mode = str(mode or self.config.get("monitor.mode", "offline")).lower()
        registry = load_registry(self.config, path=self.registry_path)
        state = StateStore(self.state_path)
        run_id = f"monitor_{utils.utc_now().strftime('%Y%m%d_%H%M%S_%f')}"
        generated_at = utils.utc_now_iso()
        failures: list[dict[str, str]] = []
        results: list[dict[str, Any]] = []
        reviews: list[dict[str, Any]] = []
        pending_alerts: list[Alert] = []
        selected_fixture = str(fixture_path) if fixture_path else self.fixture_path
        fetcher = PublicFetcher(self.config) if selected_mode in {"live", "auto"} else None

        for bad in registry.get("invalid_entries", []):
            failures.append(
                {
                    "id": str(bad.get("id")),
                    "name": "-",
                    "url": "",
                    "error": f"注册表条目无效：{bad.get('error')}",
                }
            )

        try:
            for competitor in registry["competitors"]:
                if not competitor.get("enabled", True):
                    continue
                try:
                    clean_url(competitor["url"])
                    snapshot = collect_snapshot(
                        competitor,
                        self.config,
                        mode=selected_mode,
                        fixture_path=selected_fixture,
                        fetcher=fetcher,
                    )
                    snapshot["competitor_id"] = competitor["id"]
                    snapshot["competitor_name"] = competitor["name"]
                    snapshot["source_url"] = snapshot.get("source_url") or competitor["url"]
                    snapshot["platform"] = snapshot.get("platform") or competitor["platform"]
                    snapshot["captured_at"] = snapshot.get("captured_at") or generated_at
                    previous = state.previous(competitor["id"])
                    alerts = detect_alerts(competitor, previous, snapshot, self.config)
                    pending_alerts.extend(alerts)
                    state.update(competitor["id"], snapshot)

                    for review in snapshot.get("reviews", []):
                        item = dict(review)
                        item["competitor_id"] = competitor["id"]
                        item["competitor_name"] = competitor["name"]
                        item["platform"] = competitor["platform"]
                        item["source_url"] = competitor["url"]
                        reviews.append(item)

                    snapshot_path = utils.write_json(
                        self.snapshots_dir / run_id / f"{utils.safe_filename(competitor['id'])}.json",
                        snapshot,
                    )
                    utils.write_json(
                        self.snapshots_dir / f"latest_{utils.safe_filename(competitor['id'])}.json",
                        snapshot,
                    )
                    results.append(
                        {
                            "id": competitor["id"],
                            "name": competitor["name"],
                            "url": competitor["url"],
                            "platform": competitor["platform"],
                            "status": "success",
                            "price": snapshot.get("price"),
                            "currency": snapshot.get("currency"),
                            "bsr": snapshot.get("bsr"),
                            "bsr_category": snapshot.get("bsr_category"),
                            "rating": snapshot.get("rating"),
                            "review_count": snapshot.get("review_count"),
                            "negative_reviews": sum(
                                1
                                for review in snapshot.get("reviews", [])
                                if review.get("rating") is not None
                                and int(review["rating"]) <= self.analyzer.threshold
                            ),
                            "alert_count": len(alerts),
                            "snapshot": _display_path(self.config.root, snapshot_path),
                        }
                    )
                    logger.info(
                        "竞品巡检成功: %s / 价格=%s %s / BSR=%s / 预警=%d",
                        competitor["name"],
                        snapshot.get("price"),
                        snapshot.get("currency"),
                        snapshot.get("bsr"),
                        len(alerts),
                    )
                except Exception as exc:  # 单个链接失败不影响其他链接
                    logger.warning("竞品巡检跳过: %s：%s", competitor.get("name"), exc)
                    failures.append(
                        {
                            "id": competitor.get("id", "unknown"),
                            "name": competitor.get("name", "-"),
                            "url": competitor.get("url", ""),
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
        finally:
            if fetcher is not None:
                fetcher.close()

        warning = ""
        if failures:
            warning = f"本轮失败/跳过 {len(failures)} 个链接，详情见报告。"
        alert_paths = write_alerts(pending_alerts, self.alerts_dir, run_id, warning_text=warning)
        state.save()

        report = self.analyzer.analyze(
            reviews,
            registry["competitors"],
            run_id=run_id,
            failures=failures,
        )
        report_md = self.reports_dir / f"pain_points_{run_id}.md"
        report_json = self.reports_dir / f"pain_points_{run_id}.json"
        utils.write_text(report_md, report["markdown"])
        utils.write_json(report_json, report)
        utils.write_text(self.reports_dir / "latest_pain_points.md", report["markdown"])
        utils.write_json(
            self.reports_dir / "latest_pain_points.json",
            {key: value for key, value in report.items() if key != "markdown"},
        )

        summary = {
            "run_id": run_id,
            "generated_at": generated_at,
            "mode": selected_mode,
            "registry": _display_path(self.config.root, self.registry_path),
            "counts": {
                "competitors": len(registry["competitors"]),
                "success": len(results),
                "failed": len(failures),
                "alerts": len(pending_alerts),
                "reviews": len(reviews),
                "negative_reviews": report["negative_reviews"],
            },
            "results": results,
            "failures": failures,
            "report": _display_path(self.config.root, report_md),
            "latest_report": _display_path(self.config.root, self.reports_dir / "latest_pain_points.md"),
            "latest_alerts": _display_path(self.config.root, self.alerts_dir / "latest_alerts.txt"),
            "alert_files": [_display_path(self.config.root, path) for path in alert_paths],
            "state": _display_path(self.config.root, self.state_path),
            "notice": "仅使用公开商品页/公开评论页；失败链接已跳过，不影响其他竞品。",
        }
        summary_path = utils.write_json(self.reports_dir / "monitor_summary.json", summary)
        summary["summary"] = _display_path(self.config.root, summary_path)
        logger.info(
            "巡检完成: 成功 %d / 失败 %d / 预警 %d / 差评 %d",
            len(results),
            len(failures),
            len(pending_alerts),
            report["negative_reviews"],
        )
        return summary


def validate_interval(interval_hours: float) -> float:
    if interval_hours <= 0:
        raise MonitorError("巡检间隔必须大于 0 小时")
    return interval_hours


def run_schedule(
    engine: MonitorEngine,
    *,
    interval_hours: float = DEFAULT_INTERVAL_HOURS,
    max_cycles: int | None = None,
    mode: str | None = None,
    sleeper: Any = time.sleep,
) -> int:
    interval_seconds = validate_interval(interval_hours) * 3600
    cycles = 0
    while True:
        cycles += 1
        started = time.monotonic()
        logger.info("开始第 %d 轮巡检（间隔 %.2f 小时）", cycles, interval_hours)
        try:
            engine.run(mode=mode)
        except Exception as exc:  # 调度循环不因单轮异常退出
            logger.exception("第 %d 轮巡检异常，继续等待下一轮: %s", cycles, exc)
        if max_cycles is not None and cycles >= max_cycles:
            break
        # 按开始到开始的固定节拍等待，扣除本轮执行耗时
        remaining = interval_seconds - (time.monotonic() - started)
        try:
            sleeper(max(0.0, remaining))
        except KeyboardInterrupt:
            logger.info("收到中断，停止定时巡检")
            break
    return cycles


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="competitor_monitor",
        description="竞品公开商品页监控：价格/BSR/差评/痛点/预警",
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="监控配置")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="添加竞品公开链接")
    add.add_argument("url")
    add.add_argument("--name")
    add.add_argument("--platform", default="auto", choices=["auto", "amazon", "aliexpress", "alibaba_1688", "generic"])
    add.add_argument("--price-pct", type=float, help="价格变动百分比阈值")
    add.add_argument("--price-abs", type=float, help="价格变动绝对阈值")
    add.add_argument("--rank-abs", type=float, help="BSR 变动绝对阈值")
    add.add_argument("--registry")

    listing = sub.add_parser("list", help="列出竞品")
    listing.add_argument("--registry")

    remove = sub.add_parser("remove", help="删除竞品")
    remove.add_argument("target", nargs="?", help="竞品 ID 或 URL")
    remove.add_argument("--all-demo", action="store_true", help="删除所有 demo 条目")
    remove.add_argument("--registry")

    run = sub.add_parser("run", help="执行一轮巡检")
    run.add_argument("--mode", choices=["offline", "live", "auto"])
    run.add_argument("--fixture", help="离线快照路径")
    run.add_argument("--registry")
    run.add_argument("--state")
    run.add_argument("--output-dir")
    run.add_argument("--log-level", default="INFO")

    schedule = sub.add_parser("schedule", help="按固定频率循环巡检")
    schedule.add_argument("--interval-hours", type=float, default=None, help="巡检间隔小时，默认取配置 6")
    schedule.add_argument("--max-cycles", type=int, default=None, help="最多执行轮数，便于测试")
    schedule.add_argument("--mode", choices=["offline", "live", "auto"])
    schedule.add_argument("--fixture", help="离线快照路径")
    schedule.add_argument("--registry")
    schedule.add_argument("--state")
    schedule.add_argument("--output-dir")
    schedule.add_argument("--log-level", default="INFO")
    return parser


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def _setup_logging(config: MonitorConfig, output_dir: str | None, level: str) -> None:
    base = Path(output_dir).expanduser().resolve() if output_dir else config.resolve("paths.logs_dir")
    utils.ensure_dir(base)
    log_file = base / "competitor_monitor.log"
    utils.setup_logging(level=level, log_file=log_file, console=True, force=True)


def _print_summary(summary: dict[str, Any]) -> None:
    counts = summary["counts"]
    print("")
    print("=" * 76)
    print(f"✓ 竞品巡检完成：{summary['run_id']}")
    print(f"  模式      : {summary['mode']}")
    print(
        f"  竞品      : {counts['success']} 成功 / {counts['failed']} 失败"
        f"  |  预警: {counts['alerts']}  |  差评: {counts['negative_reviews']}"
    )
    print(f"  痛点报告  : {summary['report']}")
    print(f"  预警汇总  : {summary['latest_alerts']}")
    print(f"  运行摘要  : {summary.get('summary', '-')}")
    for failure in summary["failures"]:
        print(f"  ! 跳过 {failure.get('name')}: {failure.get('error')}")
    print("=" * 76)


def main(argv: Iterable[str] | None = None) -> int:
    _configure_stdio()
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        config = load_config(args.config)
    except (MonitorError, utils.UtilError) as exc:
        print(f"✗ 配置加载失败：{exc}", file=sys.stderr)
        return 1

    if args.command == "list":
        try:
            payload = load_registry(config, path=args.registry)
        except (MonitorError, utils.UtilError) as exc:
            print(f"✗ {exc}", file=sys.stderr)
            return 1
        if not payload["competitors"]:
            print("暂无竞品，使用 add 添加公开商品链接。")
            return 0
        print(f"{'ID':<24} {'平台':<12} {'名称':<28} URL")
        for item in payload["competitors"]:
            print(f"{item['id']:<24} {item['platform']:<12} {item['name'][:28]:<28} {item['url']}")
        if payload.get("invalid_entries"):
            print(f"! 另有 {len(payload['invalid_entries'])} 个无效条目，已跳过")
        return 0

    if args.command == "add":
        try:
            entry = add_competitor(
                config,
                url=args.url,
                name=args.name,
                platform=args.platform,
                price_pct=args.price_pct,
                price_abs=args.price_abs,
                rank_abs=args.rank_abs,
                registry_path=args.registry,
            )
        except (MonitorError, utils.UtilError) as exc:
            print(f"✗ 添加失败：{exc}", file=sys.stderr)
            return 1
        print(f"✓ 已添加竞品：{entry['id']}")
        print(f"  名称: {entry['name']}")
        print(f"  平台: {entry['platform']}")
        print(f"  链接: {entry['url']}")
        return 0

    if args.command == "remove":
        if not args.target and not args.all_demo:
            print("✗ 请指定竞品 ID/URL，或使用 --all-demo", file=sys.stderr)
            return 1
        try:
            removed = remove_competitor(
                config,
                target=args.target,
                all_demo=args.all_demo,
                registry_path=args.registry,
            )
        except (MonitorError, utils.UtilError) as exc:
            print(f"✗ 删除失败：{exc}", file=sys.stderr)
            return 1
        print(f"✓ 已删除 {len(removed)} 个竞品")
        for item in removed:
            print(f"  - {item['id']} {item['name']}")
        return 0

    output_dir = args.output_dir
    _setup_logging(config, output_dir, args.log_level)
    engine = MonitorEngine(
        config,
        registry_path=args.registry,
        state_path=args.state,
        output_dir=output_dir,
        fixture_path=args.fixture,
    )
    if args.command == "run":
        try:
            summary = engine.run(mode=args.mode)
        except (MonitorError, utils.UtilError) as exc:
            logger.error("巡检失败: %s", exc)
            print(f"✗ 巡检失败：{exc}", file=sys.stderr)
            return 1
        _print_summary(summary)
        return 0
    if args.command == "schedule":
        interval = args.interval_hours
        if interval is None:
            interval = float(config.get("monitor.interval_hours", DEFAULT_INTERVAL_HOURS))
        try:
            validate_interval(interval)
        except MonitorError as exc:
            print(f"✗ {exc}", file=sys.stderr)
            return 1
        print(
            f"定时巡检启动：每 {interval:g} 小时执行一次"
            f"（Ctrl+C 停止；max_cycles={args.max_cycles or '不限'}）"
        )
        try:
            cycles = run_schedule(
                engine,
                interval_hours=interval,
                max_cycles=args.max_cycles,
                mode=args.mode,
            )
        except KeyboardInterrupt:
            print("已停止定时巡检")
            return 0
        print(f"✓ 定时巡检结束，共完成 {cycles} 轮")
        return 0
    return 1


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "competitor_monitor"))

