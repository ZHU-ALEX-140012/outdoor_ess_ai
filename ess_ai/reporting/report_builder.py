"""报告汇总层：将各阶段结果编排为可读、可交付的 Markdown 报告。"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


class ReportBuilder:
    """生成全链路报告与机器可读摘要。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.reports_dir = utils.ensure_dir(settings.path("paths.reports_dir"))

    def build(
        self,
        *,
        run_id: str,
        analysis: dict[str, Any],
        listings: dict[str, Any],
        content: dict[str, Any],
        compliance: dict[str, Any],
        manifest: dict[str, Any],
    ) -> dict[str, Any]:
        summary = self._summary(run_id, analysis, listings, content, compliance)
        markdown = self._markdown(
            run_id=run_id,
            analysis=analysis,
            listings=listings,
            content=content,
            compliance=compliance,
            manifest=manifest,
            summary=summary,
        )
        report_path = utils.write_text(self.reports_dir / "full_chain_report.md", markdown)
        summary_path = utils.write_json(self.reports_dir / "report_summary.json", summary)
        logger.info("报告生成完成: %s", report_path)
        return {
            "report_path": str(report_path.relative_to(self.settings.root)),
            "summary_path": str(summary_path.relative_to(self.settings.root)),
            "summary": summary,
        }

    @staticmethod
    def _summary(
        run_id: str,
        analysis: dict[str, Any],
        listings: dict[str, Any],
        content: dict[str, Any],
        compliance: dict[str, Any],
    ) -> dict[str, Any]:
        top_market = (analysis.get("market_scores") or [{}])[0]
        top_product = (analysis.get("top_opportunities") or [{}])[0]
        compliance_summary = compliance.get("summary", {})
        return {
            "run_id": run_id,
            "generated_at": utils.utc_now_iso(),
            "data_mode": analysis.get("data_mode", "simulated-public-proxy"),
            "top_market": top_market.get("market"),
            "top_market_score": top_market.get("overall_score"),
            "top_sku": top_product.get("sku"),
            "top_product": top_product.get("name"),
            "top_opportunity_score": top_product.get("opportunity_score"),
            "listing_count": len(listings.get("listings", [])),
            "content_pack_count": len(content.get("packs", [])),
            "compliance_passed": compliance_summary.get("passed", 0),
            "compliance_failed": compliance_summary.get("failed", 0),
            "highest_risk": compliance_summary.get("highest_risk", "clear"),
            "summary": analysis.get("summary", []),
        }

    def _markdown(
        self,
        *,
        run_id: str,
        analysis: dict[str, Any],
        listings: dict[str, Any],
        content: dict[str, Any],
        compliance: dict[str, Any],
        manifest: dict[str, Any],
        summary: dict[str, Any],
    ) -> str:
        market_scores = analysis.get("market_scores", [])
        opportunities = analysis.get("top_opportunities", [])
        positioning = analysis.get("positioning", {})
        listing_items = listings.get("listings", [])
        compliance_summary = compliance.get("summary", {})
        issue_counts = compliance_summary.get("issue_counts", {})

        lines = [
            "# 欧美轻量化户外储能 · 全链路运营报告",
            "",
            f"> 运行 ID：`{run_id}` ｜ 生成时间：{utils.utc_now_iso()} ｜ 模式：离线模拟",
            "",
            "## 1. 执行摘要",
            "",
        ]
        lines.extend(f"- {item}" for item in summary.get("summary", []))
        lines.extend(
            [
                "",
                "## 2. 市场排名",
                "",
                self._table(
                    ["排名", "市场", "综合分", "等级", "需求", "竞争", "毛利", "合规", "物流"],
                    [
                        [
                            item.get("rank"),
                            item.get("market"),
                            item.get("overall_score"),
                            item.get("tier"),
                            (item.get("sub_scores") or {}).get("demand"),
                            (item.get("sub_scores") or {}).get("competition"),
                            (item.get("sub_scores") or {}).get("margin"),
                            (item.get("sub_scores") or {}).get("compliance"),
                            (item.get("sub_scores") or {}).get("logistics"),
                        ]
                        for item in market_scores
                    ],
                ),
                "",
                "评分口径：需求 30%、竞争 20%、毛利 25%、合规 10%、物流 15%，可按 `settings.yaml` 调整。",
                "",
                "## 3. 选品机会 Top 5",
                "",
                self._table(
                    ["排名", "市场", "SKU", "商品", "售价 USD", "重量 kg", "机会分", "认证", "建议"],
                    [
                        [
                            item.get("rank"),
                            item.get("market"),
                            item.get("sku"),
                            item.get("name"),
                            item.get("price_usd"),
                            item.get("weight_kg"),
                            item.get("opportunity_score"),
                            "齐备" if item.get("compliance_ready") else "有缺口",
                            item.get("recommended_action"),
                        ]
                        for item in opportunities
                    ],
                ),
                "",
                "## 4. 定位与进入策略",
                "",
                f"- **首发市场：** {positioning.get('entry_market', '-')}",
                f"- **首发单品：** {positioning.get('entry_product', '-')}",
                f"- **定位角度：** {positioning.get('positioning_angle', '-')}",
                f"- **核心人群：** {positioning.get('primary_segment', '-')}",
                f"- **风险提示：** {positioning.get('risk_note', '-')}",
                "",
            ]
        )
        if positioning.get("differentiation"):
            lines.append("差异化抓手：")
            lines.extend(f"- {item}" for item in positioning["differentiation"])
            lines.append("")

        lines.extend(["## 5. Listing 与内容资产", ""])
        if listing_items:
            sample = listing_items[0]
            lines.extend(
                [
                    f"### 示例 Listing：{sample.get('listing_id')}",
                    "",
                    f"**标题：** {sample.get('title')}",
                    "",
                    f"**价格：** ${sample.get('price_usd')} USD（本地价 {sample.get('price_local')} {sample.get('currency')}）",
                    "",
                    "**五点描述：**",
                    "",
                ]
            )
            lines.extend(f"{index}. {bullet}" for index, bullet in enumerate(sample.get("bullets", []), start=1))
            lines.extend(
                [
                    "",
                    f"**搜索词：** {sample.get('search_terms')}",
                    "",
                    f"**合规状态：** {'可进入人工复核' if sample.get('compliance', {}).get('ready') else '存在认证缺口'}",
                    "",
                    f"- Listing 总数：{len(listing_items)}",
                    f"- 内容资产包：{len(content.get('packs', []))}",
                    "",
                ]
            )
        else:
            lines.extend(["暂无 Listing 输出。", ""])

        lines.extend(
            [
                "## 6. 合规初筛",
                "",
                f"- 通过（无高风险）：{compliance_summary.get('passed', 0)}",
                f"- 需处理：{compliance_summary.get('failed', 0)}",
                f"- 最高风险：{compliance_summary.get('highest_risk', 'clear')}",
                f"- 问题计数：高 {issue_counts.get('high', 0)} / 中 {issue_counts.get('medium', 0)} / 低 {issue_counts.get('low', 0)}",
                "",
                "> 规则初筛不构成法律或认证意见；认证范围、标签、电池运输与目的国法规需由持证服务商复核。",
                "",
            ]
        )
        failed_results = [x for x in compliance.get("results", []) if not x.get("passed")]
        if failed_results:
            lines.extend(["### 待处理项（前 5 条）", ""])
            for result in failed_results[:5]:
                issue = result["issues"][0]
                lines.append(
                    f"- `{result.get('listing_id')}`：{issue.get('message')}（{issue.get('code')}）"
                )
            lines.append("")

        lines.extend(
            [
                "## 7. 产出清单",
                "",
                self._table(
                    ["阶段", "状态", "耗时 ms", "产物数"],
                    [
                        [
                            stage.get("name"),
                            stage.get("status"),
                            stage.get("elapsed_ms"),
                            len(stage.get("outputs", [])),
                        ]
                        for stage in manifest.get("stages", [])
                    ],
                ),
                "",
                "## 8. 下一步",
                "",
                "1. 由合规服务商核验目标市场认证范围，优先补齐高风险缺口。",
                "2. 用真实供应商报价替换模拟毛利参数，复核 landed cost。",
                "3. 对 DE/FR 文案做母语审校，再进入小批量投放。",
                "4. 接入真实公开数据时，保留来源、采集时间与快照哈希。",
                "",
                "## 9. 数据边界",
                "",
                "- 不接入任何电商平台店铺 API；",
                "- 所有商品、价格、趋势、竞品数据均为固定种子模拟；",
                "- 不收集个人信息，不复制受版权保护的竞品文案；",
                "- 认证、法规与电池运输结论必须人工复核。",
                "",
                "---",
                "",
                f"*本报告由 {self.settings.project_name} v{self.settings.get('project.version', '0.1.0')} 自动生成。*",
                "",
            ]
        )
        return "\n".join(lines)

    @staticmethod
    def _table(headers: Iterable[str], rows: Iterable[Iterable[Any]]) -> str:
        header_list = [str(item) for item in headers]
        lines = [
            "| " + " | ".join(header_list) + " |",
            "| " + " | ".join("---" for _ in header_list) + " |",
        ]
        for row in rows:
            cells = [str(value).replace("|", "\\|").replace("\n", " ") if value is not None else "-" for value in row]
            lines.append("| " + " | ".join(cells) + " |")
        return "\n".join(lines)
