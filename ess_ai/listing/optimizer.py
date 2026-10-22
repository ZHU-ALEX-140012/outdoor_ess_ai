"""规则驱动的 Listing 生成与本地化占位。

本模块不伪造认证、销量或评价；认证状态只引用商品数据中的真实字段。
DE/FR 文案为可运行的模板版本，上线前仍需母语审校。
"""

from __future__ import annotations

from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


class ListingOptimizer:
    """基于选品机会生成标题、五点、描述和搜索词。"""

    def __init__(self, settings: Settings, *, max_per_market: int = 2) -> None:
        self.settings = settings
        self.max_per_market = max_per_market
        self.listings_dir = utils.ensure_dir(settings.path("paths.listings_dir"))
        self.title_max = int(settings.get("channels.listing.title_max_chars", 200))
        self.bullet_count = int(settings.get("channels.listing.bullet_count", 5))
        self.description_max = int(settings.get("channels.listing.description_max_chars", 2000))
        self.search_terms_max_bytes = int(
            settings.get("channels.listing.search_terms_max_bytes", 250)
        )
        self.disclosures = list(settings.get("compliance.required_disclosures", []) or [])

    def generate(self, analysis: dict[str, Any], normalized: dict[str, Any]) -> dict[str, Any]:
        selected = self._select_targets(analysis.get("opportunities", []))
        keywords_by_market = self._keywords_by_market(normalized.get("keywords", []))
        listings = [
            self._build_listing(item, keywords_by_market.get(str(item["market"]), []))
            for item in selected
        ]
        payload = {
            "run_id": analysis.get("run_id"),
            "generated_at": utils.utc_now_iso(),
            "notice": "文案为模拟生成，不包含未经验证的认证、销量或评价声明。",
            "listings": listings,
        }
        payload["artifacts"] = self._persist(payload)
        logger.info("Listing 生成完成: %d 条", len(listings))
        return payload

    # ------------------------------------------------------------------
    def _select_targets(self, opportunities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        selected: list[dict[str, Any]] = []
        for item in opportunities:
            market = str(item.get("market", "")).upper()
            if counts.get(market, 0) >= self.max_per_market:
                continue
            counts[market] = counts.get(market, 0) + 1
            selected.append(item)
        return selected

    @staticmethod
    def _keywords_by_market(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            grouped.setdefault(str(row.get("market", "")).upper(), []).append(row)
        for market in grouped:
            grouped[market].sort(key=lambda x: float(x.get("opportunity_index", 0)), reverse=True)
        return grouped

    def _build_listing(
        self,
        opportunity: dict[str, Any],
        keywords: list[dict[str, Any]],
    ) -> dict[str, Any]:
        market = str(opportunity.get("market", "")).upper()
        language = "de" if market == "DE" else ("fr" if market == "FR" else "en")
        name = str(opportunity.get("name", "Portable Power Station"))
        capacity = int(opportunity.get("capacity_wh") or 0)
        output_w = int(opportunity.get("output_w") or 0)
        weight = float(opportunity.get("weight_kg") or 0)
        price = float(opportunity.get("price_usd") or 0)
        gaps = list(opportunity.get("compliance_gaps") or [])

        title = self._title(name, capacity, output_w, market, language)
        bullets = self._bullets(opportunity, language)[: self.bullet_count]
        description = self._description(opportunity, language, gaps)
        search_terms = self._search_terms(keywords)
        return {
            "listing_id": utils.safe_filename(f"{market}_{opportunity.get('sku', name)}"),
            "market": market,
            "language": language,
            "channel": self.settings.get("channels.listing.channel_name", "generic-marketplace"),
            "title": title,
            "bullets": bullets,
            "description": description,
            "search_terms": search_terms,
            "price_usd": price,
            "price_local": opportunity.get("price_local"),
            "currency": opportunity.get("currency"),
            "sku": opportunity.get("sku"),
            "product_name": name,
            "capacity_wh": capacity,
            "output_w": output_w,
            "weight_kg": weight,
            "certifications": list(opportunity.get("certifications") or []),
            "compliance": {
                "required": list(opportunity.get("compliance_required") or []),
                "gaps": gaps,
                "ready": not gaps,
                "review_required": True,
            },
            "disclosures": self.disclosures,
            "copy_review_required": language in {"de", "fr"},
            "generated_by": "rule-template/v1",
        }

    def _title(self, name: str, capacity: int, output_w: int, market: str, language: str) -> str:
        if capacity <= 0:
            raw = f"{name} — {output_w}W Foldable Portable Solar Panel for Camping and RV"
        elif language == "de":
            raw = (
                f"{name} – {capacity}Wh tragbare Powerstation, {output_w}W AC-Ausgang, "
                "solarbereit für Camping und Notstrom"
            )
        elif language == "fr":
            raw = (
                f"{name} – station électrique portable {capacity}Wh, sortie AC {output_w}W, "
                "compatible solaire pour camping et secours"
            )
        else:
            raw = (
                f"{name}, {capacity}Wh Portable Power Station, {output_w}W AC Output, "
                "Solar-Ready for Camping and Emergency Backup"
            )
        return self._clip(raw, self.title_max)

    def _bullets(self, item: dict[str, Any], language: str) -> list[str]:
        capacity = int(item.get("capacity_wh") or 0)
        output_w = int(item.get("output_w") or 0)
        weight = float(item.get("weight_kg") or 0)
        solar = int(item.get("solar_input_w") or 0)
        cycles = int(item.get("cycles") or 0)
        warranty = int(item.get("warranty_years") or 0)
        chemistry = str(item.get("chemistry") or "LiFePO4")
        use_cases = ", ".join(item.get("use_cases") or ["camping", "emergency backup"])

        if language == "de":
            return [
                f"{capacity} Wh {chemistry}-Kapazität und {output_w} W AC-Ausgang für Camping und Notstrom.",
                f"Wiegt nur {weight:.1f} kg – für den Transport im Fahrzeug und kurze Strecken geeignet.",
                f"Unterstützt bis zu {solar} W Solar-Eingang für längere Aufenthalte ohne Steckdose.",
                f"Geeignet für {use_cases}; Laufzeit abhängig vom angeschlossenen Gerät.",
                f"{chemistry}-Zellen mit bis zu {cycles} Ladezyklen und {warranty} Jahren Garantie.",
            ]
        if language == "fr":
            return [
                f"Capacité {capacity} Wh {chemistry} et sortie AC {output_w} W pour le camping et le secours.",
                f"Seulement {weight:.1f} kg, conçue pour le transport en voiture et les déplacements courts.",
                f"Entrée solaire jusqu'à {solar} W pour prolonger l'autonomie hors réseau.",
                f"Adaptée à {use_cases} ; l'autonomie dépend des appareils connectés.",
                f"Cellules {chemistry} jusqu'à {cycles} cycles et garantie limitée de {warranty} ans.",
            ]
        return [
            f"{capacity}Wh {chemistry} capacity with a {output_w}W AC output for camping and backup power.",
            f"Weighs {weight:.1f} kg, designed for single-person carrying and compact vehicle storage.",
            f"Accepts up to {solar}W solar input, so you can recharge away from a wall outlet.",
            f"Built for {use_cases}; actual runtime varies by device and conditions.",
            f"{chemistry} cells rated for up to {cycles} cycles, backed by a {warranty}-year limited warranty.",
        ]

    def _description(self, item: dict[str, Any], language: str, gaps: list[str]) -> str:
        name = str(item.get("name", "Product"))
        capacity = int(item.get("capacity_wh") or 0)
        output_w = int(item.get("output_w") or 0)
        weight = float(item.get("weight_kg") or 0)
        solar = int(item.get("solar_input_w") or 0)
        differentiators = item.get("differentiators") or []
        cert_status = (
            "Certification package under review; no certification claim is made in this draft."
            if gaps
            else "Referenced certifications are listed in the product data; verify scope before publishing."
        )
        lines = [
            f"{name} is designed for campers and households that need compact, portable power.",
            "",
            f"- Capacity: {capacity}Wh" if capacity else f"- Output: {output_w}W",
            f"- AC output: {output_w}W",
            f"- Weight: {weight:.1f} kg",
            f"- Solar input: up to {solar}W",
            f"- Highlights: {', '.join(str(x) for x in differentiators)}",
            "",
            "What is in the box: power station, AC charging cable, quick-start guide.",
            "Please confirm the final package contents with your supplier before publishing.",
            "",
            cert_status,
        ]
        lines.extend(f"- {text}" for text in self.disclosures)
        if language in {"de", "fr"}:
            lines.append("- Localized copy requires native-speaker review before publishing.")
        return self._clip("\n".join(lines), self.description_max)

    def _search_terms(self, keywords: list[dict[str, Any]]) -> str:
        parts: list[str] = []
        for item in keywords:
            word = str(item.get("keyword", "")).strip()
            if word and word.lower() not in {p.lower() for p in parts}:
                parts.append(word)
        raw = " ".join(parts)
        encoded = raw.encode("utf-8")
        if len(encoded) <= self.search_terms_max_bytes:
            return raw
        clipped = encoded[: self.search_terms_max_bytes].decode("utf-8", errors="ignore")
        return clipped.rsplit(" ", 1)[0]

    @staticmethod
    def _clip(text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[: max(0, limit - 1)].rsplit(" ", 1)[0].rstrip(",;:-") + "…"

    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        artifacts: dict[str, str] = {}
        for listing in payload["listings"]:
            path = utils.write_json(
                self.listings_dir / f"{listing['listing_id']}.json",
                listing,
            )
            artifacts[listing["listing_id"]] = str(path.relative_to(self.settings.root))
        aggregate = utils.write_json(self.listings_dir / "listings.json", payload)
        artifacts["listings"] = str(aggregate.relative_to(self.settings.root))
        return artifacts
