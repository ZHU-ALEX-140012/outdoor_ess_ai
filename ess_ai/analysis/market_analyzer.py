"""市场评分与选品机会分析。

评分全部为可解释的规则模型，不依赖外部 API；权重来自 ``settings.yaml``。
"""

from __future__ import annotations

from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


def _num(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


class MarketAnalyzer:
    """把标准表转换为市场排名、商品机会与进入策略。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.analysis_dir = utils.ensure_dir(settings.path("paths.analysis_dir"))

    def analyze(self, normalized: dict[str, Any]) -> dict[str, Any]:
        market_scores = self._score_markets(normalized)
        opportunities = self._score_opportunities(normalized, market_scores)
        payload = {
            "run_id": normalized.get("run_id"),
            "generated_at": utils.utc_now_iso(),
            "data_mode": normalized.get("data_mode", ""),
            "market_scores": market_scores,
            "opportunities": opportunities,
            "top_opportunities": opportunities[:5],
            "positioning": self._build_positioning(market_scores, opportunities),
            "summary": self._build_summary(market_scores, opportunities),
            "weights": self.settings.get("business.scoring_weights", {}),
        }
        payload["artifacts"] = self._persist(payload)
        logger.info("分析完成: 市场 %d 个 / 机会 %d 条", len(market_scores), len(opportunities))
        return payload

    # ------------------------------------------------------------------
    def _score_markets(self, normalized: dict[str, Any]) -> list[dict[str, Any]]:
        weights = self.settings.get("business.scoring_weights", {}) or {}
        weight_total = sum(_num(v) for v in weights.values()) or 1.0
        trend_by_market: dict[str, list[dict[str, Any]]] = {}
        for row in normalized.get("trend_summary", []):
            trend_by_market.setdefault(str(row.get("market", "")).upper(), []).append(row)

        scores: list[dict[str, Any]] = []
        for market in normalized.get("market_summary", []):
            code = str(market.get("market", "")).upper()
            trends = trend_by_market.get(code, [])
            trend_avg = (
                sum(_num(x.get("avg_last_7d")) for x in trends) / len(trends) if trends else 0.0
            )
            trend_growth = (
                sum(_num(x.get("growth_pct")) for x in trends) / len(trends) if trends else 0.0
            )
            keyword_opp = _num(market.get("avg_keyword_opportunity"))
            growth_score = _clamp(50 + trend_growth * 4)
            demand_score = _clamp(
                _num(market.get("demand_index")) * 0.55
                + keyword_opp * 0.25
                + trend_avg * 0.10
                + growth_score * 0.10
            )
            competition_score = _clamp(100 - _num(market.get("competition_index")))
            compliance_score = _clamp(100 - _num(market.get("compliance_complexity")))
            logistics_score = _clamp(100 - _num(market.get("logistics_cost_index")) * 4.2)

            cost_ratio = (
                0.48
                + _num(market.get("logistics_cost_index")) / 100 * 0.35
                + _num(market.get("import_duty_pct")) / 100
            )
            margin_ratio = _clamp(1 - cost_ratio - 0.18, 0.0, 1.0)
            margin_score = _clamp(margin_ratio / 0.35 * 100)

            overall = (
                demand_score * _num(weights.get("demand"), 0.30)
                + competition_score * _num(weights.get("competition"), 0.20)
                + margin_score * _num(weights.get("margin"), 0.25)
                + compliance_score * _num(weights.get("compliance"), 0.10)
                + logistics_score * _num(weights.get("logistics"), 0.15)
            ) / weight_total

            scores.append(
                {
                    **market,
                    "sub_scores": {
                        "demand": round(demand_score, 2),
                        "competition": round(competition_score, 2),
                        "margin": round(margin_score, 2),
                        "compliance": round(compliance_score, 2),
                        "logistics": round(logistics_score, 2),
                    },
                    "estimated_gross_margin_pct": round(margin_ratio * 100, 2),
                    "trend_avg_last_7d": round(trend_avg, 2),
                    "trend_growth_pct": round(trend_growth, 2),
                    "overall_score": round(_clamp(overall), 2),
                    "tier": "A" if overall >= 65 else ("B" if overall >= 55 else "C"),
                }
            )
        scores.sort(key=lambda item: item["overall_score"], reverse=True)
        for index, item in enumerate(scores, start=1):
            item["rank"] = index
        return scores

    def _score_opportunities(
        self,
        normalized: dict[str, Any],
        market_scores: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        markets = {str(item["market"]): item for item in market_scores}
        opportunities: list[dict[str, Any]] = []
        for product in normalized.get("products", []):
            market = str(product.get("market", "")).upper()
            market_score = markets.get(market)
            if not market_score:
                continue
            price = _num(product.get("price_usd"))
            aov = _num(market_score.get("avg_order_value_usd"), 500)
            price_ratio = price / aov if aov else 1.0
            price_fit = _clamp(100 - max(0.0, price_ratio - 0.85) * 70)
            required = product.get("compliance_required") or []
            gaps = product.get("compliance_gaps") or []
            compliance_score = (
                _clamp(100 - len(gaps) / len(required) * 100) if required else 100.0
            )
            demand = _num(market_score.get("sub_scores", {}).get("demand"))
            margin = _num(market_score.get("sub_scores", {}).get("margin"))
            portability = _num(product.get("portability_score"))
            overall = (
                demand * 0.30
                + price_fit * 0.20
                + portability * 0.20
                + compliance_score * 0.15
                + margin * 0.15
            )
            opportunities.append(
                {
                    "market": market,
                    "sku": product.get("sku"),
                    "name": product.get("name"),
                    "category": product.get("category"),
                    "price_usd": price,
                    "price_local": product.get("price_local"),
                    "currency": product.get("currency"),
                    "capacity_wh": product.get("capacity_wh"),
                    "output_w": product.get("output_w"),
                    "weight_kg": product.get("weight_kg"),
                    "solar_input_w": product.get("solar_input_w"),
                    "cycles": product.get("cycles"),
                    "warranty_years": product.get("warranty_years"),
                    "chemistry": product.get("chemistry"),
                    "use_cases": list(product.get("use_cases") or []),
                    "differentiators": list(product.get("differentiators") or []),
                    "portability_score": portability,
                    "compliance_ready": bool(product.get("compliance_ready")),
                    "compliance_required": list(product.get("compliance_required") or []),
                    "certifications": list(product.get("certifications") or []),
                    "compliance_gaps": gaps,
                    "market_score": market_score.get("overall_score"),
                    "demand_score": round(demand, 2),
                    "price_fit_score": round(price_fit, 2),
                    "compliance_score": round(compliance_score, 2),
                    "opportunity_score": round(_clamp(overall), 2),
                    "recommended_action": (
                        "优先进入"
                        if overall >= 75
                        else ("小批量测试" if overall >= 65 else "观察/补齐合规后再评估")
                    ),
                    "localization_required": market in {"DE", "FR"},
                }
            )
        opportunities.sort(key=lambda item: item["opportunity_score"], reverse=True)
        for index, item in enumerate(opportunities, start=1):
            item["rank"] = index
        return opportunities

    @staticmethod
    def _build_positioning(
        market_scores: list[dict[str, Any]],
        opportunities: list[dict[str, Any]],
    ) -> dict[str, Any]:
        if not market_scores:
            return {}
        top_market = market_scores[0]
        top_product = opportunities[0] if opportunities else {}
        lightweight = [item for item in opportunities if _num(item.get("weight_kg")) <= 10]
        return {
            "entry_market": top_market.get("market"),
            "entry_market_score": top_market.get("overall_score"),
            "entry_sku": top_product.get("sku"),
            "entry_product": top_product.get("name"),
            "positioning_angle": "轻量化户外储能 + 太阳能快充 + 静音露营用电",
            "primary_segment": "周末露营 / 轻量房车 / 家庭应急备电",
            "lightweight_candidate_count": len(lightweight),
            "price_band_focus": "mid-premium",
            "differentiation": [
                "以 10kg 以内可单人搬运作为第一筛选门槛",
                "用太阳能输入功率与充满时间作为核心对比参数",
                "用静音、循环寿命和质保年限支撑溢价",
            ],
            "risk_note": "认证与电池运输合规必须先于投放完成，不得用文案替代资质。",
        }

    @staticmethod
    def _build_summary(
        market_scores: list[dict[str, Any]],
        opportunities: list[dict[str, Any]],
    ) -> list[str]:
        if not market_scores:
            return ["无可用市场数据。"]
        top = market_scores[0]
        best = opportunities[0] if opportunities else {}
        gap_count = sum(1 for item in opportunities if item.get("compliance_gaps"))
        return [
            f"首选市场：{top.get('market')}（综合 {top.get('overall_score')} 分，{top.get('tier')} 级）。",
            f"首选单品：{best.get('name', '暂无')}（{best.get('market', '-')} / {best.get('opportunity_score', 0)} 分）。",
            f"机会池共 {len(opportunities)} 条，其中 {gap_count} 条存在认证缺口，需先补齐再投放。",
            "建议路径：US 市场小批量验证 → DE/FR 本地化与合规加严 → UK 轻量扩品。",
        ]

    # ------------------------------------------------------------------
    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        json_path = utils.write_json(self.analysis_dir / "market_analysis.json", payload)
        market_csv = utils.write_csv(
            self.analysis_dir / "market_scores.csv",
            payload["market_scores"],
            fieldnames=[
                "rank",
                "market",
                "overall_score",
                "tier",
                "estimated_gross_margin_pct",
                "trend_growth_pct",
                "demand_index",
                "competition_index",
            ],
        )
        opportunity_csv = utils.write_csv(
            self.analysis_dir / "opportunities.csv",
            payload["opportunities"],
            fieldnames=[
                "rank",
                "market",
                "sku",
                "name",
                "price_usd",
                "weight_kg",
                "opportunity_score",
                "compliance_ready",
                "recommended_action",
                "compliance_gaps",
            ],
        )
        return {
            "analysis": str(json_path.relative_to(self.settings.root)),
            "market_scores_csv": str(market_csv.relative_to(self.settings.root)),
            "opportunities_csv": str(opportunity_csv.relative_to(self.settings.root)),
        }
