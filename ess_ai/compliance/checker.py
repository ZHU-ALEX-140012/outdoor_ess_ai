"""合规规则初筛。

这是“投放前风险提示”，不是法律意见。认证范围、标签、电池运输与
目的国法规必须由具备资质的合规服务商复核。
"""

from __future__ import annotations

import re
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)

_CERT_PATTERN = re.compile(r"\b(UL 2743|UL2743|FCC|CE|UKCA|RoHS|WEEE|UN38\.3)\b", re.IGNORECASE)
_SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1, "info": 0}


class ComplianceChecker:
    """对生成的 Listing 做禁用词、披露项与认证缺口检查。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.compliance_dir = utils.ensure_dir(settings.path("paths.compliance_dir"))
        self.forbidden_claims = [
            str(x).lower() for x in (settings.get("compliance.forbidden_claims", []) or [])
        ]
        self.disclosures = [
            str(x) for x in (settings.get("compliance.required_disclosures", []) or [])
        ]
        self.title_max = int(settings.get("channels.listing.title_max_chars", 200))
        self.description_max = int(settings.get("channels.listing.description_max_chars", 2000))

    def check(self, listings_payload: dict[str, Any]) -> dict[str, Any]:
        listings = [x for x in listings_payload.get("listings", []) if isinstance(x, dict)]
        results = [self._check_one(listing) for listing in listings]
        issue_counts = {"high": 0, "medium": 0, "low": 0, "info": 0}
        for result in results:
            for issue in result["issues"]:
                issue_counts[issue["severity"]] = issue_counts.get(issue["severity"], 0) + 1
        failed = [x for x in results if not x["passed"]]
        payload = {
            "run_id": listings_payload.get("run_id"),
            "checked_at": utils.utc_now_iso(),
            "notice": "规则初筛结果不构成法律或认证意见，发布前必须人工复核。",
            "summary": {
                "listings": len(results),
                "passed": len(results) - len(failed),
                "failed": len(failed),
                "issue_counts": issue_counts,
                "highest_risk": max(
                    (x["risk_level"] for x in results),
                    key=lambda level: _SEVERITY_ORDER.get(level, 0),
                    default="clear",
                ),
            },
            "results": results,
        }
        payload["artifacts"] = self._persist(payload)
        logger.info(
            "合规初筛完成: %d 条通过 / %d 条需处理", payload["summary"]["passed"], len(failed)
        )
        return payload

    # ------------------------------------------------------------------
    def _check_one(self, listing: dict[str, Any]) -> dict[str, Any]:
        issues: list[dict[str, str]] = []
        title = str(listing.get("title", ""))
        description = str(listing.get("description", ""))
        bullets = [str(x) for x in (listing.get("bullets") or [])]
        full_text = " ".join([title, *bullets, description])
        lowered = full_text.lower()

        for claim in self.forbidden_claims:
            if claim and claim in lowered:
                issues.append(
                    self._issue(
                        "FORBIDDEN_CLAIM",
                        "high",
                        "title/bullets/description",
                        f"出现禁用或高风险绝对化表述：{claim}",
                        "删除绝对化承诺，改为可验证、有限定条件的表述。",
                    )
                )

        for disclosure in self.disclosures:
            if disclosure.lower() not in lowered:
                issues.append(
                    self._issue(
                        "MISSING_DISCLOSURE",
                        "medium",
                        "description",
                        "缺少必填披露项。",
                        f"在描述中加入：{disclosure}",
                    )
                )

        compliance = listing.get("compliance") or {}
        gaps = [str(x) for x in (compliance.get("gaps") or [])]
        if gaps:
            issues.append(
                self._issue(
                    "CERTIFICATION_GAP",
                    "high",
                    "compliance",
                    f"目标市场仍缺少认证/合规项：{', '.join(gaps)}",
                    "在正式投放前由合规服务商确认适用范围并补齐证据，不得在文案中声称已认证。",
                )
            )

        certifications = [str(x) for x in (listing.get("certifications") or [])]
        certified_lower = {x.lower() for x in certifications}
        for match in _CERT_PATTERN.findall(full_text):
            normalized = match.lower().replace(" ", "")
            if normalized not in {x.replace(" ", "") for x in certified_lower}:
                issues.append(
                    self._issue(
                        "UNVERIFIED_CERT_CLAIM",
                        "high",
                        "title/bullets/description",
                        f"文案提及认证 {match}，但商品数据中无该认证记录。",
                        "删除该认证声明，或先补充可核验的证书编号与范围。",
                    )
                )

        if len(title) > self.title_max:
            issues.append(
                self._issue(
                    "TITLE_TOO_LONG",
                    "medium",
                    "title",
                    f"标题长度 {len(title)} 超过配置上限 {self.title_max}。",
                    "压缩标题，保留核心参数与使用场景。",
                )
            )
        if len(description) > self.description_max:
            issues.append(
                self._issue(
                    "DESCRIPTION_TOO_LONG",
                    "medium",
                    "description",
                    f"描述长度 {len(description)} 超过配置上限 {self.description_max}。",
                    "精简描述或拆分 A+ 内容模块。",
                )
            )

        if listing.get("copy_review_required"):
            issues.append(
                self._issue(
                    "NATIVE_REVIEW_REQUIRED",
                    "low",
                    "language",
                    "DE/FR 文案由模板生成，尚未经过母语审校。",
                    "发布前交由母语运营审校，重点检查参数单位、语法与本地法规措辞。",
                )
            )

        if not listing.get("price_usd") or float(listing.get("price_usd") or 0) <= 0:
            issues.append(
                self._issue(
                    "INVALID_PRICE",
                    "medium",
                    "price_usd",
                    "价格缺失或非正数。",
                    "补齐含税/不含税口径与本地币种价格。",
                )
            )

        high_count = sum(1 for x in issues if x["severity"] == "high")
        medium_count = sum(1 for x in issues if x["severity"] == "medium")
        risk_level = "high" if high_count else ("medium" if medium_count else ("low" if issues else "clear"))
        return {
            "listing_id": listing.get("listing_id"),
            "market": listing.get("market"),
            "sku": listing.get("sku"),
            "passed": high_count == 0,
            "risk_level": risk_level,
            "high_risk_count": high_count,
            "medium_risk_count": medium_count,
            "issues": issues,
        }

    @staticmethod
    def _issue(
        code: str,
        severity: str,
        field: str,
        message: str,
        suggestion: str,
    ) -> dict[str, str]:
        return {
            "code": code,
            "severity": severity,
            "field": field,
            "message": message,
            "suggestion": suggestion,
        }

    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        json_path = utils.write_json(self.compliance_dir / "compliance_report.json", payload)
        md_path = utils.write_text(
            self.compliance_dir / "compliance_report.md",
            self._to_markdown(payload),
        )
        return {
            "compliance_json": str(json_path.relative_to(self.settings.root)),
            "compliance_md": str(md_path.relative_to(self.settings.root)),
        }

    @staticmethod
    def _to_markdown(payload: dict[str, Any]) -> str:
        summary = payload["summary"]
        issue_counts = summary["issue_counts"]
        lines = [
            "# 合规初筛报告",
            "",
            f"- 生成时间：{payload['checked_at']}",
            f"- Listing 数量：{summary['listings']}",
            f"- 通过（无高风险）：{summary['passed']}",
            f"- 需处理：{summary['failed']}",
            f"- 风险计数：高 {issue_counts.get('high', 0)} / 中 {issue_counts.get('medium', 0)} / 低 {issue_counts.get('low', 0)}",
            "",
            "> 本报告为规则初筛，不构成法律或认证意见。",
            "",
            "| Listing | 市场 | SKU | 通过 | 风险 | 问题数 |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for item in payload["results"]:
            lines.append(
                f"| {item.get('listing_id')} | {item.get('market')} | {item.get('sku')} "
                f"| {'是' if item.get('passed') else '否'} | {item.get('risk_level')} | {len(item.get('issues', []))} |"
            )
        lines.extend(["", "## 问题明细", ""])
        for item in payload["results"]:
            if not item["issues"]:
                lines.append(f"### {item['listing_id']}：未发现规则问题")
                lines.append("")
                continue
            lines.append(f"### {item['listing_id']}（{item['risk_level']}）")
            for issue in item["issues"]:
                lines.append(
                    f"- **[{issue['severity']}] {issue['code']}**（{issue['field']}）："
                    f"{issue['message']} 建议：{issue['suggestion']}"
                )
            lines.append("")
        return "\n".join(lines)
