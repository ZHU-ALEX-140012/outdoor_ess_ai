"""内容生成层：短视频脚本、社媒文案与博客提纲。

采用确定性模板，确保离线可跑、可审阅、可追溯；live 模式可在此接入
DeepSeek 进行扩写，但不得绕过合规检查。
"""

from __future__ import annotations

from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


class ContentGenerator:
    """根据 Listing 生成内容资产包（默认英文，适配欧美市场）。"""

    def __init__(self, settings: Settings, *, max_packs: int = 4) -> None:
        self.settings = settings
        self.max_packs = max_packs
        self.content_dir = utils.ensure_dir(settings.path("paths.content_dir"))

    def generate(self, listings_payload: dict[str, Any]) -> dict[str, Any]:
        listings = [x for x in listings_payload.get("listings", []) if isinstance(x, dict)]
        selected = listings[: self.max_packs]
        packs = [self._build_pack(listing) for listing in selected]
        payload = {
            "run_id": listings_payload.get("run_id"),
            "generated_at": utils.utc_now_iso(),
            "notice": "内容为模板生成，不含未经验证的认证、销量、评价或绝对化功效声明。",
            "packs": packs,
        }
        payload["artifacts"] = self._persist(payload)
        logger.info("内容资产生成完成: %d 个资产包", len(packs))
        return payload

    # ------------------------------------------------------------------
    def _build_pack(self, listing: dict[str, Any]) -> dict[str, Any]:
        name = str(listing.get("product_name", "Portable Power Station"))
        market = str(listing.get("market", "US"))
        capacity = int(listing.get("capacity_wh") or 0)
        output_w = int(listing.get("output_w") or 0)
        weight = float(listing.get("weight_kg") or 0)
        price = float(listing.get("price_usd") or 0)
        product_line = (
            f"{capacity}Wh / {output_w}W / {weight:.1f}kg"
            if capacity
            else f"{output_w}W foldable solar panel / {weight:.1f}kg"
        )
        keywords = str(listing.get("search_terms", "")).split()
        focus_keywords = keywords[:4]

        script = self._short_video_script(name, product_line, price, market)
        caption = self._social_caption(name, product_line, market)
        blog = self._blog_outline(name, product_line, focus_keywords, market)
        return {
            "content_id": utils.safe_filename(f"content_{market}_{listing.get('sku', name)}"),
            "market": market,
            "language": listing.get("language", "en"),
            "sku": listing.get("sku"),
            "product_name": name,
            "short_video_script": script,
            "social_caption": caption,
            "blog_outline": blog,
            "review_required": True,
            "compliance_note": "发布前需核对认证状态、价格口径、披露项与本地广告法规。",
        }

    @staticmethod
    def _short_video_script(name: str, product_line: str, price: float, market: str) -> dict[str, Any]:
        return {
            "format": "vertical 9:16",
            "duration_seconds": 55,
            "hook": "Your weekend power setup should not weigh more than your cooler.",
            "scenes": [
                {
                    "time": "0-3s",
                    "visual": "Car trunk opens; compact power station slides into the free space.",
                    "voiceover": "Still hauling a heavy generator for a weekend trip?",
                    "on_screen": "Lighter weekend setup",
                },
                {
                    "time": "3-10s",
                    "visual": "Close-up of the product, ports, and carry handle.",
                    "voiceover": f"This is the {name}: {product_line}.",
                    "on_screen": product_line,
                },
                {
                    "time": "10-22s",
                    "visual": "Camp scene: kettle, camera, and phone charging from the unit.",
                    "voiceover": "Run small camp appliances, cameras, and phones without a wall outlet.",
                    "on_screen": "Camp-ready AC output",
                },
                {
                    "time": "22-34s",
                    "visual": "Foldable solar panel connected under daylight; battery display rises.",
                    "voiceover": "Pair it with a compatible solar panel to recharge off-grid.",
                    "on_screen": "Solar-ready",
                },
                {
                    "time": "34-44s",
                    "visual": "Weight check on a luggage scale; one-person lift into a car.",
                    "voiceover": "One-person carry, compact storage, and a quieter campsite.",
                    "on_screen": "Easy to carry",
                },
                {
                    "time": "44-55s",
                    "visual": "Product on a table with price card and CTA end frame.",
                    "voiceover": (
                        f"Check the current {market} price and full specs before you buy."
                    ),
                    "on_screen": f"From ${price:.0f} · see listing for details",
                },
            ],
            "cta": "Tap the link to compare capacity, weight, and solar input.",
            "limitations": "Runtime varies by device and conditions. Solar recharge depends on sunlight.",
        }

    @staticmethod
    def _social_caption(name: str, product_line: str, market: str) -> dict[str, Any]:
        caption = (
            f"Weekend power, minus the generator noise. {name}: {product_line}. "
            "Check the full specs and current price before you choose your setup. "
            "Runtime varies by device; solar recharge depends on sunlight."
        )
        return {
            "caption": caption,
            "hashtags": ["#CampingPower", "#PortablePowerStation", "#OutdoorGear", "#SolarReady"],
            "cta": "See the listing for full specifications.",
            "disclosure": "Add #ad only if this is a paid placement.",
            "market": market,
        }

    @staticmethod
    def _blog_outline(
        name: str,
        product_line: str,
        focus_keywords: list[str],
        market: str,
    ) -> dict[str, Any]:
        keyword_text = ", ".join(focus_keywords) if focus_keywords else "portable power station"
        return {
            "title": f"{name} Review: Specs, Use Cases, and What to Check Before Buying",
            "target_keywords": focus_keywords,
            "sections": [
                {
                    "heading": "Why weight and usable capacity matter",
                    "points": [
                        "Explain the difference between rated capacity and usable output.",
                        "Show how weight affects solo camping and vehicle storage.",
                    ],
                },
                {
                    "heading": f"{name} at a glance",
                    "points": [
                        f"Specs: {product_line}.",
                        "List ports, charging options, and warranty terms.",
                    ],
                },
                {
                    "heading": "Realistic use cases",
                    "points": [
                        "Weekend camping and tailgating.",
                        "Emergency backup for phones, lights, and routers.",
                        "What the product is not designed to power.",
                    ],
                },
                {
                    "heading": "Solar charging expectations",
                    "points": [
                        "Explain sunlight, panel angle, and cable losses.",
                        "Avoid promising a fixed recharge time without test conditions.",
                    ],
                },
                {
                    "heading": "Compliance and safety checklist",
                    "points": [
                        "Verify destination-market certification scope.",
                        "Check lithium battery transport and labeling requirements.",
                    ],
                },
            ],
            "faq": [
                "How long will it run a 500W appliance?",
                "Can I charge it while using the AC output?",
                "What is included in the box?",
            ],
            "seo_note": f"Primary market: {market}; keywords: {keyword_text}.",
        }

    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        artifacts: dict[str, str] = {}
        for pack in payload["packs"]:
            content_id = pack["content_id"]
            json_path = utils.write_json(self.content_dir / f"{content_id}.json", pack)
            md_path = utils.write_text(
                self.content_dir / f"{content_id}.md",
                self._to_markdown(pack),
            )
            artifacts[content_id] = str(json_path.relative_to(self.settings.root))
            artifacts[f"{content_id}_md"] = str(md_path.relative_to(self.settings.root))
        aggregate = utils.write_json(self.content_dir / "content_pack.json", payload)
        artifacts["content_pack"] = str(aggregate.relative_to(self.settings.root))
        return artifacts

    @staticmethod
    def _to_markdown(pack: dict[str, Any]) -> str:
        script = pack["short_video_script"]
        caption = pack["social_caption"]
        blog = pack["blog_outline"]
        lines = [
            f"# 内容资产包：{pack['product_name']}（{pack['market']}）",
            "",
            f"> {pack['compliance_note']}",
            "",
            "## 1. 55 秒短视频脚本",
            "",
            f"**Hook：** {script['hook']}",
            "",
            "| 时间 | 画面 | 口播 | 屏幕文字 |",
            "| --- | --- | --- | --- |",
        ]
        for scene in script["scenes"]:
            lines.append(
                f"| {scene['time']} | {scene['visual']} | {scene['voiceover']} | {scene['on_screen']} |"
            )
        lines.extend(
            [
                "",
                f"**CTA：** {script['cta']}",
                "",
                f"**限制说明：** {script['limitations']}",
                "",
                "## 2. 社媒文案",
                "",
                caption["caption"],
                "",
                " ".join(caption["hashtags"]),
                "",
                f"**披露：** {caption['disclosure']}",
                "",
                "## 3. 博客提纲",
                "",
                f"**标题：** {blog['title']}",
                "",
                f"**目标关键词：** {', '.join(blog['target_keywords']) or '—'}",
                "",
            ]
        )
        for section in blog["sections"]:
            lines.append(f"### {section['heading']}")
            lines.extend(f"- {point}" for point in section["points"])
            lines.append("")
        lines.append("### FAQ")
        lines.extend(f"- {item}" for item in blog["faq"])
        lines.extend(
            [
                "",
                "## 4. 发布前检查",
                "",
                "- [ ] 认证范围可核验",
                "- [ ] 价格与税费口径一致",
                "- [ ] 披露项完整",
                "- [ ] 母语审校完成",
                "",
            ]
        )
        return "\n".join(lines)
