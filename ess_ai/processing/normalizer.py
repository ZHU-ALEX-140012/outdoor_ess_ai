"""数据清洗与标准化。

输入为采集层的原始快照，输出为统一币种、统一口径、可分析的扁平记录。
"""

from __future__ import annotations

import statistics
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


class DataNormalizer:
    """把原始 JSON 转换为市场、商品、趋势、关键词四类标准表。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.processed_dir = utils.ensure_dir(settings.path("paths.processed_dir"))

    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        market_profiles = {
            str(item.get("market", "")).upper(): item
            for item in raw.get("market_profiles", [])
            if isinstance(item, dict)
        }
        required_by_market = self.settings.get("compliance.market_requirements", {}) or {}

        products = [
            self._normalize_product(item, market_profiles, required_by_market)
            for item in raw.get("products", [])
            if isinstance(item, dict)
        ]
        products = [item for item in products if item.get("market")]

        trends = [item for item in raw.get("trends", []) if isinstance(item, dict)]
        keywords = [self._normalize_keyword(item) for item in raw.get("keywords", []) if isinstance(item, dict)]
        competitors = [item for item in raw.get("competitors", []) if isinstance(item, dict)]

        payload = {
            "run_id": raw.get("run_id"),
            "generated_at": utils.utc_now_iso(),
            "data_mode": raw.get("data_mode", "simulated-public-proxy"),
            "notice": raw.get("notice", ""),
            "products": products,
            "trend_summary": self._summarize_trends(trends),
            "keywords": keywords,
            "competitor_summary": self._summarize_competitors(competitors),
            "market_summary": self._summarize_markets(market_profiles, products, keywords),
            "counts": {
                "products": len(products),
                "trends": len(trends),
                "keywords": len(keywords),
                "competitors": len(competitors),
                "markets": len(market_profiles),
            },
        }
        payload["artifacts"] = self._persist(payload)
        logger.info("清洗完成: %d 条商品市场记录", len(products))
        return payload

    # ------------------------------------------------------------------
    def _normalize_product(
        self,
        item: dict[str, Any],
        market_profiles: dict[str, dict[str, Any]],
        required_by_market: dict[str, Any],
    ) -> dict[str, Any]:
        market = str(item.get("market", "")).upper()
        capacity = _number(item.get("capacity_wh"))
        output_w = _number(item.get("output_w"))
        weight = _number(item.get("weight_kg"))
        price = _number(item.get("price_usd_est"))
        certifications = [str(x) for x in (item.get("certifications") or [])]
        required = [str(x) for x in (required_by_market.get(market, []) or [])]
        gaps = [cert for cert in required if cert not in certifications]

        portability = _clamp(
            100 - max(0.0, weight - 3.0) * 5.2 + min(capacity, 1500.0) / 180.0,
            0.0,
            100.0,
        )
        if capacity > 0:
            price_per_wh: float | None = round(price / capacity, 4)
        else:
            price_per_wh = None

        profile = market_profiles.get(market, {})
        return {
            **item,
            "market": market,
            "capacity_wh": int(capacity),
            "output_w": int(output_w),
            "weight_kg": round(weight, 3),
            "price_usd": round(price, 2),
            "price_local": round(_number(item.get("price_local"), price), 2),
            "price_per_wh": price_per_wh,
            "power_density_w_kg": round(output_w / weight, 3) if weight > 0 else 0.0,
            "portability_score": round(portability, 2),
            "is_lightweight": bool(weight and weight <= 10.0),
            "is_high_capacity": capacity >= 1000,
            "price_band": "budget" if price < 400 else ("mid" if price <= 800 else "premium"),
            "language": profile.get("language", "en"),
            "compliance_required": required,
            "compliance_gaps": gaps,
            "compliance_ready": not gaps,
        }

    @staticmethod
    def _normalize_keyword(item: dict[str, Any]) -> dict[str, Any]:
        search_index = _number(item.get("search_index"))
        difficulty = _number(item.get("difficulty"))
        return {
            **item,
            "market": str(item.get("market", "")).upper(),
            "search_index": round(search_index, 1),
            "difficulty": round(difficulty, 1),
            "cpc_usd": round(_number(item.get("cpc_usd")), 2),
            "opportunity_index": round(search_index * 0.6 + (100 - difficulty) * 0.4, 2),
            "source_id": "public_trend_proxy/simulated",
        }

    @staticmethod
    def _summarize_trends(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in rows:
            key = (str(row.get("market", "")).upper(), str(row.get("keyword", "")))
            grouped.setdefault(key, []).append(row)

        summary: list[dict[str, Any]] = []
        for (market, keyword), items in sorted(grouped.items()):
            ordered = sorted(items, key=lambda x: str(x.get("date", "")))
            values = [_number(x.get("search_index")) for x in ordered]
            if not values:
                continue
            first = values[0]
            last = values[-1]
            growth = ((last - first) / first * 100.0) if first else 0.0
            summary.append(
                {
                    "market": market,
                    "keyword": keyword,
                    "days": len(values),
                    "avg_index": round(statistics.fmean(values), 2),
                    "avg_last_7d": round(statistics.fmean(values[-7:]), 2),
                    "growth_pct": round(growth, 2),
                    "volatility": round(statistics.pstdev(values), 2),
                    "peak_index": round(max(values), 1),
                }
            )
        return summary

    @staticmethod
    def _summarize_competitors(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            grouped.setdefault(str(row.get("market", "")).upper(), []).append(row)
        summary: list[dict[str, Any]] = []
        for market, items in sorted(grouped.items()):
            prices = [_number(x.get("price_usd_est")) for x in items]
            ratings = [_number(x.get("rating")) for x in items]
            summary.append(
                {
                    "market": market,
                    "competitor_count": len(items),
                    "avg_price_usd": round(statistics.fmean(prices), 2) if prices else 0.0,
                    "avg_rating": round(statistics.fmean(ratings), 2) if ratings else 0.0,
                }
            )
        return summary

    @staticmethod
    def _summarize_markets(
        profiles: dict[str, dict[str, Any]],
        products: list[dict[str, Any]],
        keywords: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        summary: list[dict[str, Any]] = []
        for market, profile in sorted(profiles.items()):
            market_products = [x for x in products if x.get("market") == market]
            market_keywords = [x for x in keywords if x.get("market") == market]
            prices = [_number(x.get("price_usd")) for x in market_products]
            weights = [_number(x.get("weight_kg")) for x in market_products if _number(x.get("weight_kg")) > 0]
            summary.append(
                {
                    "market": market,
                    "language": profile.get("language", "en"),
                    "currency": profile.get("currency", "USD"),
                    "demand_index": _number(profile.get("demand_index")),
                    "competition_index": _number(profile.get("competition_index")),
                    "growth_pct": _number(profile.get("growth_pct")),
                    "household_energy_price_usd_kwh": _number(
                        profile.get("household_energy_price_usd_kwh")
                    ),
                    "outdoor_participation_pct": _number(profile.get("outdoor_participation_pct")),
                    "compliance_complexity": _number(profile.get("compliance_complexity")),
                    "logistics_cost_index": _number(profile.get("logistics_cost_index")),
                    "vat_pct": _number(profile.get("vat_pct")),
                    "import_duty_pct": _number(profile.get("import_duty_pct")),
                    "avg_order_value_usd": _number(profile.get("avg_order_value_usd")),
                    "product_count": len(market_products),
                    "keyword_count": len(market_keywords),
                    "avg_price_usd": round(statistics.fmean(prices), 2) if prices else 0.0,
                    "avg_weight_kg": round(statistics.fmean(weights), 2) if weights else 0.0,
                    "avg_keyword_opportunity": round(
                        statistics.fmean([_number(x.get("opportunity_index")) for x in market_keywords]), 2
                    )
                    if market_keywords
                    else 0.0,
                }
            )
        return summary

    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        json_path = utils.write_json(self.processed_dir / "normalized.json", payload)
        csv_fields = [
            "market",
            "sku",
            "name",
            "category",
            "capacity_wh",
            "output_w",
            "weight_kg",
            "price_usd",
            "price_per_wh",
            "portability_score",
            "price_band",
            "compliance_ready",
            "compliance_gaps",
        ]
        csv_path = utils.write_csv(
            self.processed_dir / "products.csv",
            payload["products"],
            fieldnames=csv_fields,
        )
        return {
            "normalized": str(json_path.relative_to(self.settings.root)),
            "products_csv": str(csv_path.relative_to(self.settings.root)),
        }
