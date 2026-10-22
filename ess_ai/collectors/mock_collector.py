"""离线模拟采集器。

重要边界：
    - 不访问任何电商平台 API、不登录卖家后台、不抓取个人信息；
    - 所有商品、价格、趋势、竞品数据均由固定随机种子生成；
    - 输出中的 ``source_id`` 仅用于说明模拟口径，不代表真实接口。
"""

from __future__ import annotations

import math
import random
from datetime import UTC, datetime, timedelta
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)

_COMPETITOR_BRANDS = (
    "Aurora Grid",
    "PeakCell",
    "Vento Power",
    "Terravolt",
    "Kestrel Energy",
    "NomadWorks",
    "BlueRidge",
    "SolHaven",
)
_CAPACITIES = (300, 500, 600, 768, 1000, 1500, 2000)


class MockCollector:
    """读取本地 mock 商品目录，生成带来源标记的市场快照。"""

    def __init__(
        self,
        settings: Settings,
        *,
        seed: int | None = None,
        markets: list[str] | None = None,
    ) -> None:
        self.settings = settings
        self.seed = int(seed if seed is not None else settings.get("project.seed", 20260401))
        self.markets = [str(item).upper() for item in (markets or settings.markets)]
        self.mock_dir = settings.path("paths.mock_dir")
        self.raw_dir = utils.ensure_dir(settings.path("paths.raw_dir"))

    # ------------------------------------------------------------------
    # 公共入口
    # ------------------------------------------------------------------
    def collect(self, run_id: str) -> dict[str, Any]:
        """执行一次模拟采集并写入 ``data/raw``，返回内存快照。"""

        rng = random.Random(self.seed)
        catalog = self._load_json("product_catalog.json")
        keyword_doc = self._load_json("keywords.json")
        market_doc = self._load_json("market_profiles.json")

        catalog_products = [item for item in catalog.get("products", []) if isinstance(item, dict)]
        keyword_rows = [item for item in keyword_doc.get("keywords", []) if isinstance(item, dict)]
        market_profiles = [
            item
            for item in market_doc.get("markets", [])
            if isinstance(item, dict) and str(item.get("market", "")).upper() in self.markets
        ]
        if not catalog_products or not market_profiles:
            raise utils.FileIOError("mock 数据缺失：商品目录或市场档案为空")

        products = self._build_products(rng, catalog_products, market_profiles)
        trends = self._build_trends(rng, keyword_rows)
        competitors = self._build_competitors(rng, market_profiles)

        payload: dict[str, Any] = {
            "run_id": run_id,
            "generated_at": utils.utc_now_iso(),
            "data_mode": "simulated-public-proxy",
            "notice": "全部数值为离线模拟，不来自任何平台店铺 API 或真实卖家后台。",
            "seed": self.seed,
            "markets": self.markets,
            "products": products,
            "keywords": keyword_rows,
            "trends": trends,
            "competitors": competitors,
            "market_profiles": market_profiles,
            "sources": [
                "public_trend_proxy",
                "public_price_pages",
                "public_competitor_pages",
                "public_macro_energy",
            ],
        }
        payload["artifacts"] = self._persist(payload)
        logger.info(
            "采集完成: %d 个商品市场记录 / %d 条趋势 / %d 个竞品",
            len(products),
            len(trends),
            len(competitors),
        )
        return payload

    # ------------------------------------------------------------------
    # 构造数据
    # ------------------------------------------------------------------
    def _load_json(self, filename: str) -> dict[str, Any]:
        path = self.mock_dir / filename
        value = utils.read_json(path)
        if not isinstance(value, dict):
            raise utils.FileIOError(f"mock 文件根节点必须是对象: {path}")
        return value

    def _build_products(
        self,
        rng: random.Random,
        catalog_products: list[dict[str, Any]],
        market_profiles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        fx = self.settings.get("business.fx_to_usd", {}) or {}
        rows: list[dict[str, Any]] = []
        collected_at = utils.utc_now_iso()
        for market_profile in market_profiles:
            market = str(market_profile["market"]).upper()
            currency = str(market_profile.get("currency", "USD"))
            fx_rate = float(fx.get(currency, 1.0))
            vat = float(market_profile.get("vat_pct", 0)) / 100.0
            for product in catalog_products:
                target_markets = [str(x).upper() for x in product.get("target_markets", [])]
                if target_markets and market not in target_markets:
                    continue
                price_factor = rng.uniform(0.95, 1.05)
                local_price = float(product.get("msrp_usd", 0)) * fx_rate * (1 + vat) * price_factor
                local_price = max(round(local_price) - 0.01, 1.0)
                rows.append(
                    {
                        **product,
                        "market": market,
                        "currency": currency,
                        "price_local": round(local_price, 2),
                        "price_usd_est": round(local_price / fx_rate, 2),
                        "seller_count": rng.randint(8, 65),
                        "rating": round(rng.uniform(4.0, 4.8), 1),
                        "review_count": rng.randint(25, 4800),
                        "source_id": "public_price_pages/simulated",
                        "collected_at": collected_at,
                    }
                )
        return rows

    def _build_trends(
        self,
        rng: random.Random,
        keyword_rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        today = datetime.now(UTC).date()
        for keyword in keyword_rows:
            market = str(keyword.get("market", "")).upper()
            if market not in self.markets:
                continue
            base = float(keyword.get("search_index", 30))
            for offset in range(27, -1, -1):
                day_index = 27 - offset
                seasonality = 7.5 * math.sin((2 * math.pi * day_index) / 28)
                noise = rng.uniform(-4.5, 4.5)
                value = max(0.0, min(100.0, base * 0.72 + 18 + seasonality + noise))
                rows.append(
                    {
                        "date": (today - timedelta(days=offset)).isoformat(),
                        "market": market,
                        "keyword": keyword.get("keyword", ""),
                        "search_index": round(value, 1),
                        "source_id": "public_trend_proxy/simulated",
                    }
                )
        return rows

    def _build_competitors(
        self,
        rng: random.Random,
        market_profiles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for market_profile in market_profiles:
            market = str(market_profile["market"]).upper()
            brands = rng.sample(_COMPETITOR_BRANDS, k=5)
            for brand in brands:
                capacity = rng.choice(_CAPACITIES)
                price = capacity * rng.uniform(0.55, 0.95) + rng.uniform(60, 140)
                rows.append(
                    {
                        "market": market,
                        "brand": brand,
                        "title": f"{brand} {capacity}Wh Portable Power Station",
                        "capacity_wh": capacity,
                        "output_w": int(capacity * rng.uniform(0.8, 1.2)),
                        "weight_kg": round(capacity * 0.009 + rng.uniform(2.2, 4.5), 2),
                        "price_usd_est": round(price, 2),
                        "rating": round(rng.uniform(3.9, 4.8), 1),
                        "review_count": rng.randint(15, 9000),
                        "source_id": "public_competitor_pages/simulated",
                    }
                )
        return rows

    # ------------------------------------------------------------------
    # 持久化
    # ------------------------------------------------------------------
    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        artifacts: dict[str, str] = {}
        mapping = {
            "products": "products.json",
            "keywords": "keywords.json",
            "trends": "trends.json",
            "competitors": "competitors.json",
            "market_profiles": "market_profiles.json",
        }
        for key, filename in mapping.items():
            path = utils.write_json(self.raw_dir / filename, payload[key])
            artifacts[key] = str(path.relative_to(self.settings.root))
        manifest = {
            "run_id": payload["run_id"],
            "generated_at": payload["generated_at"],
            "data_mode": payload["data_mode"],
            "seed": payload["seed"],
            "counts": {key: len(payload[key]) for key in mapping},
            "files": {
                key: {
                    "path": path,
                    "sha256": utils.file_sha256(self.settings.root / path),
                }
                for key, path in artifacts.items()
            },
        }
        manifest_path = utils.write_json(self.raw_dir / "collector_manifest.json", manifest)
        artifacts["manifest"] = str(manifest_path.relative_to(self.settings.root))
        return artifacts
