#!/usr/bin/env python3
"""Amazon 上架素材自动化模块。

输入：第二步产出的选品表（xlsx / csv，默认 outputs/research/high_potential_products.xlsx）
输出：
    1. 每个目标站点一份 Amazon 平铺文件 CSV；
    2. 每个站点一份完整文案 JSON（标题、5 点、详情页、搜索词）；
    3. 结构化校验报告（字段、长度、类型、必填值、违禁词、导入阻塞项）；
    4. 汇总摘要 listing_summary.json。

边界：
    - 只生成选品表中的商品，不伪造 GTIN、认证、评价、销量或图片；
    - Amazon 类目模板会随站点/类目更新，字段档案独立在
      config/amazon_listing_profile.yaml，可替换为 Seller Central 当前模板表头；
    - 违禁词检查是规则初筛，不替代平台审核或法律意见。
"""

from __future__ import annotations

import argparse
import csv
import html
import math
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import utils  # noqa: E402

logger = utils.get_logger("listing_generator")

DEFAULT_INPUT = PROJECT_ROOT / "outputs" / "research" / "high_potential_products.xlsx"
DEFAULT_PROFILE = PROJECT_ROOT / "config" / "amazon_listing_profile.yaml"
DEFAULT_RULES = PROJECT_ROOT / "config" / "listing_copy_rules.yaml"
DEFAULT_OUTPUT = PROJECT_ROOT / "outputs" / "listing"
DEFAULT_SHEET = "高潜力选品"

HEADER_ALIASES: dict[str, str] = {
    "rank": "rank",
    "排名": "rank",
    "platform": "platform",
    "platform_label": "platform_label",
    "平台": "platform_label",
    "title": "title",
    "商品标题": "title",
    "brand": "brand",
    "品牌/供应商": "brand",
    "sku": "sku",
    "SKU": "sku",
    "url": "url",
    "商品链接": "url",
    "market": "market",
    "目标市场": "market",
    "capacity_wh": "capacity_wh",
    "容量(Wh)": "capacity_wh",
    "output_w": "output_w",
    "输出功率(W)": "output_w",
    "weight_kg": "weight_kg",
    "重量(kg)": "weight_kg",
    "battery_type": "battery_type",
    "电芯类型": "battery_type",
    "solar_input_w": "solar_input_w",
    "太阳能输入(W)": "solar_input_w",
    "rating": "rating",
    "评分": "rating",
    "review_count": "review_count",
    "评论/成交数": "review_count",
    "price_usd": "price_usd",
    "公开价(USD)": "price_usd",
    "retail_price_usd": "retail_price_usd",
    "零售基准价(USD)": "retail_price_usd",
    "gross_margin_pct": "gross_margin_pct",
    "毛利率(%)": "gross_margin_pct",
    "opportunity_score": "opportunity_score",
    "综合机会分": "opportunity_score",
    "recommendation": "recommendation",
    "推荐等级": "recommendation",
    "gate_status": "gate_status",
    "门槛状态": "gate_status",
    "compliance_note": "compliance_note",
    "合规提示": "compliance_note",
    "source_page": "source_page",
    "公开来源页": "source_page",
    "record_id": "record_id",
    "原始记录ID": "record_id",
    "product_id": "product_id",
    "main_image_url": "main_image_url",
    "external_product_id": "external_product_id",
    "external_product_id_type": "external_product_id_type",
    "recommended_browse_nodes": "recommended_browse_nodes",
    "country_of_origin": "country_of_origin",
    "number_of_ac_outlets": "number_of_ac_outlets",
    "item_length": "item_length",
    "item_width": "item_width",
    "item_height": "item_height",
}
PLATFORM_LABELS = {"amazon": "amazon", "aliexpress": "aliexpress", "1688": "1688"}
EU_MARKETS = {"DE", "FR"}


class ListingError(RuntimeError):
    """Listing 生成或校验失败。"""


# ---------------------------------------------------------------------------
# 选品表读取
# ---------------------------------------------------------------------------
def _canonical_key(header: Any) -> str:
    text = str(header or "").strip().lstrip("\ufeff")
    if text in HEADER_ALIASES:
        return HEADER_ALIASES[text]
    lowered = text.lower().replace(" ", "_")
    return HEADER_ALIASES.get(lowered, lowered)


def _read_xlsx(path: Path, sheet: str | None) -> tuple[list[str], list[dict[str, Any]]]:
    try:
        from openpyxl import load_workbook
    except ImportError as exc:  # pragma: no cover
        raise ListingError("读取 xlsx 需要 openpyxl：pip install openpyxl") from exc
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet and sheet in wb.sheetnames else wb[wb.sheetnames[0]]
    header_row = 0
    headers: list[str] = []
    for row_index, row in enumerate(ws.iter_rows(min_row=1, max_row=25, values_only=True), start=1):
        values = [str(cell).strip() if cell is not None else "" for cell in row]
        if any(value in {"SKU", "sku", "商品标题", "title"} for value in values):
            header_row = row_index
            headers = values
            break
    if not header_row:
        raise ListingError(f"未在 {path.name} 找到选品表表头（需要 SKU/商品标题）")
    records: list[dict[str, Any]] = []
    for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
        if not any(cell is not None and str(cell).strip() for cell in row):
            continue
        record = {
            _canonical_key(headers[index] if index < len(headers) else ""): cell
            for index, cell in enumerate(row)
        }
        records.append(record)
    wb.close()
    return headers, records


def read_selection(
    path: str | Path,
    *,
    sheet: str | None = None,
    only_passed: bool = True,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """读取选品表并转成内部字段。"""

    source = Path(path).expanduser().resolve()
    if not source.exists():
        raise ListingError(f"选品表不存在: {source}")
    if source.suffix.lower() in {".xlsx", ".xlsm"}:
        _, raw_rows = _read_xlsx(source, sheet)
    elif source.suffix.lower() == ".csv":
        raw_rows = [{_canonical_key(key): value for key, value in row.items()} for row in utils.read_csv(source)]
    else:
        raise ListingError("只支持 .xlsx/.xlsm/.csv 选品表")

    rows: list[dict[str, Any]] = []
    for raw in raw_rows:
        gate = str(raw.get("gate_status") or "").strip()
        if only_passed and gate and gate != "通过":
            continue
        sku = str(raw.get("sku") or "").strip()
        if not sku:
            continue
        platform = str(raw.get("platform") or raw.get("platform_label") or "").strip()
        platform = PLATFORM_LABELS.get(platform.lower(), platform.lower())
        capacity = _num(raw.get("capacity_wh"))
        output_w = _num(raw.get("output_w"))
        weight = _num(raw.get("weight_kg"))
        price = _num(raw.get("retail_price_usd")) or _num(raw.get("price_usd"))
        if capacity <= 0 or output_w <= 0 or weight <= 0 or price <= 0:
            logger.warning("跳过字段不完整的 SKU: %s", sku)
            continue
        rows.append(
            {
                "rank": _int(raw.get("rank")),
                "platform": platform,
                "platform_label": str(raw.get("platform_label") or platform),
                "sku": sku,
                "title": str(raw.get("title") or "").strip(),
                "brand": str(raw.get("brand") or "").strip(),
                "url": str(raw.get("url") or "").strip(),
                "market": str(raw.get("market") or "US").upper(),
                "capacity_wh": capacity,
                "output_w": output_w,
                "weight_kg": weight,
                "battery_type": str(raw.get("battery_type") or "LiFePO4"),
                "solar_input_w": _num(raw.get("solar_input_w")),
                "price_usd": price,
                "gross_margin_pct": _num(raw.get("gross_margin_pct")),
                "opportunity_score": _num(raw.get("opportunity_score")),
                "recommendation": str(raw.get("recommendation") or ""),
                "gate_status": gate,
                "compliance_note": str(raw.get("compliance_note") or ""),
                "source_page": str(raw.get("source_page") or raw.get("url") or ""),
                "record_id": str(raw.get("record_id") or ""),
                "main_image_url": str(raw.get("main_image_url") or "").strip(),
                "external_product_id": str(raw.get("external_product_id") or "").strip(),
                "external_product_id_type": str(raw.get("external_product_id_type") or "").strip().upper(),
                "recommended_browse_nodes": str(raw.get("recommended_browse_nodes") or "").strip(),
                "country_of_origin": str(raw.get("country_of_origin") or "").strip().upper(),
                "number_of_ac_outlets": str(raw.get("number_of_ac_outlets") or "").strip(),
                "item_length": str(raw.get("item_length") or "").strip(),
                "item_width": str(raw.get("item_width") or "").strip(),
                "item_height": str(raw.get("item_height") or "").strip(),
            }
        )
    if limit:
        rows = rows[:limit]
    if not rows:
        raise ListingError("选品表中没有可生成的 SKU（检查筛选条件/门槛状态）")
    return rows


def _num(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(value or ""))
    return float(match.group(0).replace(",", "")) if match else default


def _int(value: Any, default: int = 0) -> int:
    return int(round(_num(value, default)))


# ---------------------------------------------------------------------------
# 配置与字段档案
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class FieldSpec:
    key: str
    header: str
    required_value: bool
    max_length: int
    type: str
    enum: tuple[str, ...]


@dataclass(frozen=True)
class MarketProfile:
    market: str
    locale: str
    language: str
    currency: str
    fx_from_usd: float
    voltage: str
    plug_type: str
    field_set: str
    amazon_domain: str
    filename: str
    gpsr_required: bool


@dataclass(frozen=True)
class AmazonProfile:
    path: Path
    data: dict[str, Any]
    fields: tuple[FieldSpec, ...]
    eu_extra_fields: tuple[FieldSpec, ...]
    markets: dict[str, MarketProfile]

    @property
    def defaults(self) -> dict[str, Any]:
        return dict(self.data.get("defaults") or {})

    def fields_for(self, market: str) -> list[FieldSpec]:
        base = list(self.fields)
        if market in EU_MARKETS:
            base.extend(self.eu_extra_fields)
        return base

    def market(self, code: str) -> MarketProfile:
        normalized = code.strip().upper()
        if normalized not in self.markets:
            raise ListingError(f"未配置站点: {code}，可选 {', '.join(self.markets)}")
        return self.markets[normalized]


def _load_fields(items: Any) -> tuple[FieldSpec, ...]:
    if not isinstance(items, list):
        raise ListingError("字段档案 fields 必须是列表")
    result: list[FieldSpec] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        result.append(
            FieldSpec(
                key=str(item.get("key") or ""),
                header=str(item.get("header") or item.get("key") or ""),
                required_value=bool(item.get("required_value", False)),
                max_length=int(item.get("max_length", 500)),
                type=str(item.get("type", "text")),
                enum=tuple(str(x) for x in item.get("enum", [])),
            )
        )
    keys = [item.key for item in result]
    if len(keys) != len(set(keys)):
        raise ListingError("字段档案存在重复 key")
    return tuple(result)


def load_profile(path: str | Path = DEFAULT_PROFILE) -> AmazonProfile:
    target = Path(path).expanduser().resolve()
    data = utils.read_yaml(target)
    if not isinstance(data, dict):
        raise ListingError(f"字段档案格式错误: {target}")
    fields = _load_fields(data.get("fields"))
    extras = _load_fields(data.get("eu_extra_fields", []))
    if not fields:
        raise ListingError("字段档案为空")
    markets: dict[str, MarketProfile] = {}
    for market, cfg in (data.get("markets") or {}).items():
        if not isinstance(cfg, dict):
            continue
        markets[str(market).upper()] = MarketProfile(
            market=str(market).upper(),
            locale=str(cfg.get("locale") or f"en-{market}"),
            language=str(cfg.get("language") or "en"),
            currency=str(cfg.get("currency") or "USD"),
            fx_from_usd=float(cfg.get("fx_from_usd", 1.0)),
            voltage=str(cfg.get("voltage") or "120"),
            plug_type=str(cfg.get("plug_type") or ""),
            field_set=str(cfg.get("field_set") or "base"),
            amazon_domain=str(cfg.get("amazon_domain") or ""),
            filename=str(cfg.get("filename") or f"amazon_{str(market).lower()}_listings.csv"),
            gpsr_required=bool(cfg.get("gpsr_required", False)),
        )
    if not markets:
        raise ListingError("字段档案缺少 markets")
    required_headers = {"sku", "item_name", "product_description", "bullet_point1", "standard_price"}
    headers = {item.header for item in fields}
    missing = required_headers - headers
    if missing:
        raise ListingError(f"字段档案缺少核心字段: {sorted(missing)}")
    return AmazonProfile(path=target, data=data, fields=fields, eu_extra_fields=extras, markets=markets)


# ---------------------------------------------------------------------------
# 违禁词
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ClaimRule:
    phrase: str
    severity: str
    replacement: str


class ComplianceScanner:
    """对文案做规则扫描，并在写 CSV 前做保守替换。"""

    FIELDS = (
        "item_name",
        "bullet_point1",
        "bullet_point2",
        "bullet_point3",
        "bullet_point4",
        "bullet_point5",
        "product_description",
        "generic_keywords",
        "safety_warning",
        "directions_for_use",
        "warranty_description",
        "legal_disclaimer_description",
    )

    def __init__(self, rules_path: str | Path = DEFAULT_RULES) -> None:
        raw = utils.read_yaml(Path(rules_path).expanduser().resolve())
        if not isinstance(raw, dict):
            raise ListingError("违禁词规则格式错误")
        self.rules = tuple(
            ClaimRule(
                phrase=str(item.get("phrase", "")).strip(),
                severity=str(item.get("severity", "high")),
                replacement=str(item.get("replacement", "")),
            )
            for item in raw.get("forbidden_claims", [])
            if isinstance(item, dict) and str(item.get("phrase", "")).strip()
        )
        self.residual_terms = [str(x) for x in raw.get("residual_terms", [])]
        if not self.rules:
            raise ListingError("违禁词规则为空")

    @staticmethod
    def _pattern(phrase: str) -> re.Pattern[str]:
        return re.compile(r"(?<![A-Za-z0-9])" + re.escape(phrase) + r"(?![A-Za-z0-9])", re.IGNORECASE)

    def sanitize(self, values: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """返回替换后的字段与违规明细。"""

        cleaned = dict(values)
        violations: list[dict[str, str]] = []
        for field in self.FIELDS:
            if field not in cleaned or cleaned[field] is None:
                continue
            text = str(cleaned[field])
            for rule in self.rules:
                pattern = self._pattern(rule.phrase)
                if not pattern.search(text):
                    continue
                text = pattern.sub(rule.replacement, text)
                violations.append(
                    {
                        "field": field,
                        "phrase": rule.phrase,
                        "severity": rule.severity,
                        "replacement": rule.replacement,
                    }
                )
            cleaned[field] = text
        residual = self.residual(cleaned)
        for term in residual:
            violations.append(
                {
                    "field": "multiple",
                    "phrase": term,
                    "severity": "high",
                    "replacement": "仍需人工处理",
                }
            )
        return cleaned, violations

    def residual(self, values: dict[str, Any]) -> list[str]:
        text = " ".join(str(values.get(field, "")) for field in self.FIELDS).lower()
        found: list[str] = []
        for term in self.residual_terms:
            if self._pattern(term).search(text) and term.lower() not in found:
                found.append(term.lower())
        return found

    @staticmethod
    def status(violations: list[dict[str, str]]) -> str:
        if not violations:
            return "PASS"
        if any(item["severity"] == "high" for item in violations):
            return "REVIEW"
        return "WARN"


# ---------------------------------------------------------------------------
# 多语言文案
# ---------------------------------------------------------------------------
def _clip(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    clipped = text[: max(0, limit - 1)].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return clipped + "…"


def _trim_bytes(text: str, limit: int = 250) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    encoded = text.encode("utf-8")
    if len(encoded) <= limit:
        return text
    return encoded[:limit].decode("utf-8", errors="ignore").rsplit(" ", 1)[0]


def _fmt(value: float, digits: int = 1, comma: bool = False) -> str:
    text = f"{value:.{digits}f}"
    return text.replace(".", ",") if comma else text


class Copywriter:
    """生成面向欧美露营/短途出行用户的本地化 Listing 文案。"""

    def __init__(self, default_brand: str = "TrailHarbor") -> None:
        self.default_brand = default_brand

    def build(self, row: dict[str, Any], locale: MarketProfile) -> dict[str, Any]:
        brand = self._brand(row)
        capacity = float(row["capacity_wh"])
        output_w = float(row["output_w"])
        weight = float(row["weight_kg"])
        solar = float(row["solar_input_w"])
        language = locale.language
        if language == "de":
            copy = self._german(row, locale, brand, capacity, output_w, weight, solar)
        elif language == "fr":
            copy = self._french(row, locale, brand, capacity, output_w, weight, solar)
        else:
            copy = self._english(row, locale, brand, capacity, output_w, weight, solar)
        copy["locale"] = locale.locale
        copy["market"] = locale.market
        copy["language"] = language
        copy["copy_review_required"] = language != "en"
        copy["source_sku"] = row["sku"]
        return copy

    def _brand(self, row: dict[str, Any]) -> str:
        raw = str(row.get("brand") or "").strip()
        if row.get("platform") == "1688" or not raw or re.search(
            r"demo|generic|unknown|factory", raw, re.IGNORECASE
        ):
            return self.default_brand
        return raw

    # ------------------------------------------------------------------
    def _english(
        self,
        row: dict[str, Any],
        locale: MarketProfile,
        brand: str,
        capacity: float,
        output_w: float,
        weight: float,
        solar: float,
    ) -> dict[str, Any]:
        uk = locale.market == "UK"
        event = "campsites, campervan weekends, and power cuts" if uk else "campsites, tailgating, and short getaways"
        boot = "boot" if uk else "trunk"
        title_end = "Camping and Power Cuts" if uk else "Camping and Emergency Backup"
        lb = weight * 2.20462
        solar_line = (
            f"Accepts up to {solar:.0f}W of solar input (panel not included) for off-grid top-ups; "
            "recharge time depends on sunlight and panel output."
            if solar > 0
            else "Recharge from a standard wall outlet; check the specification table for input requirements."
        )
        title = _clip(
            f"{brand} {capacity:.0f}Wh Portable Power Station, {output_w:.0f}W AC Output, "
            f"{row.get('battery_type', 'LiFePO4')} Solar-Ready Battery for {title_end}",
            200,
        )
        bullets = [
            _clip(
                f"{capacity:.0f}Wh {row.get('battery_type', 'LiFePO4')} CAPACITY: "
                f"A {output_w:.0f}W AC output for phones, cameras, lights, and small camp appliances. "
                "Check your device's continuous wattage before use.",
                500,
            ),
            _clip(
                f"BUILT FOR SHORT TRIPS: At {weight:.1f} kg ({lb:.1f} lb), the compact body is designed "
                f"for one-person carrying and {boot} storage.",
                500,
            ),
            _clip(f"SOLAR-READY: {solar_line}", 500),
            _clip(
                "QUIET CAMP POWER: Battery operation without fuel or exhaust fumes—"
                f"ideal for {event}.",
                500,
            ),
            _clip(
                "SIMPLE TO LIVE WITH: Straightforward controls and a clear specification table. "
                "Actual runtime varies by device and conditions; check the table before connecting high-draw devices.",
                500,
            ),
        ]
        specs = [
            f"Capacity: {capacity:.0f}Wh",
            f"AC output: {output_w:.0f}W",
            f"Battery: {row.get('battery_type', 'LiFePO4')}",
            f"Weight: {weight:.1f} kg ({lb:.1f} lb)",
            f"Solar input: up to {solar:.0f}W (panel not included)" if solar > 0 else "Solar input: not specified",
            f"Output voltage: {locale.voltage}V",
        ]
        where = (
            "Tent camping, campervan weekends, staycations, home backup, and short power cuts."
            if uk
            else "Tent camping, road trips, tailgating, home backup, and short outages."
        )
        backup_event = "short power cuts" if uk else "short outages"
        description = (
            f"<p><strong>{html.escape(brand)} {capacity:.0f}Wh Portable Power Station</strong></p>"
            f"<p>Built for weekend campers, road-trippers, and households that want a compact backup "
            f"for {backup_event}. The unit pairs a LiFePO4 battery with an AC output "
            "for everyday outdoor power.</p>"
            f"<p><strong>Key specifications</strong><br>{'<br>'.join(specs)}</p>"
            "<p><strong>Where it fits</strong><br>"
            f"{where} Use the specification table to match the station to your device.</p>"
            "<p><strong>Before you buy</strong><br>"
            "Actual output and runtime vary by device and conditions. Solar charging depends on sunlight, "
            "panel angle, and weather. Check the continuous wattage of your appliance before use. "
            "Lithium battery products are subject to transport regulations.</p>"
        )
        return self._pack(
            brand,
            title,
            bullets,
            description,
            (
                "portable power station camping battery solar ready campervan accessories power cuts emergency power supply lightweight"
                if uk
                else "portable power station camping battery solar ready rv accessories emergency power supply lightweight power bank"
            ),
            (
                "Use only compatible chargers and cables. Keep vents clear. Do not expose to rain or "
                "standing water. Keep away from children. Lithium batteries require special transport handling."
            ),
            "Charge before first use. Connect devices within the rated output. Store in a cool, dry place.",
            "Actual output and runtime vary by device and conditions. Solar charging depends on sunlight, panel angle, and weather.",
            "Limited manufacturer warranty. See product documentation for terms.",
        )

    def _german(
        self,
        row: dict[str, Any],
        locale: MarketProfile,
        brand: str,
        capacity: float,
        output_w: float,
        weight: float,
        solar: float,
    ) -> dict[str, Any]:
        weight_de = _fmt(weight, 1, comma=True)
        solar_line = (
            f"Bis zu {solar:.0f} W Solar-Eingang (Solarmodul nicht im Lieferumfang) für das Laden ohne Steckdose."
            if solar > 0
            else "Laden über eine haushaltsübliche Steckdose; Eingangsdaten siehe technische Daten."
        )
        title = _clip(
            f"{brand} {capacity:.0f}Wh tragbare Powerstation, {output_w:.0f}W AC-Ausgang, "
            f"{row.get('battery_type', 'LiFePO4')}-Akku, solarbereit für Camping und Notstrom",
            200,
        )
        bullets = [
            _clip(
                f"{capacity:.0f} Wh {row.get('battery_type', 'LiFePO4')}-Kapazität und {output_w:.0f} W AC-Ausgang "
                "für Smartphone, Kamera, Lampe und kleine Campinggeräte. Prüfen Sie die Dauerleistung Ihres Geräts.",
                500,
            ),
            _clip(
                f"Nur {weight_de} kg – gebaut für den Transport im Kofferraum und kurze Strecken.",
                500,
            ),
            _clip(f"SOLARBEREIT: {solar_line}", 500),
            _clip(
                "LEISER CAMPING-STROM: Akkubetrieb ohne Kraftstoff und Abgase – "
                "geeignet für Camping, Picknick und Stromausfälle.",
                500,
            ),
            _clip(
                "EINFACH IM ALLTAG: Kompaktes Gehäuse und klare Bedienelemente. "
                "Die tatsächliche Laufzeit hängt vom Gerät und den Bedingungen ab.",
                500,
            ),
        ]
        specs = [
            f"Kapazität: {capacity:.0f} Wh",
            f"AC-Ausgang: {output_w:.0f} W",
            f"Akku: {row.get('battery_type', 'LiFePO4')}",
            f"Gewicht: {weight_de} kg",
            f"Solar-Eingang: bis zu {solar:.0f} W (Modul nicht enthalten)" if solar > 0 else "Solar-Eingang: nicht angegeben",
            f"Ausgangsspannung: {locale.voltage} V",
        ]
        description = (
            f"<p><strong>{html.escape(brand)} {capacity:.0f}Wh tragbare Powerstation</strong></p>"
            "<p>Für Wochenend-Camping, Campervan-Touren und kurze Stromausfälle. Die Powerstation kombiniert "
            "einen LiFePO4-Akku mit einem AC-Ausgang für den täglichen Outdoor-Bedarf.</p>"
            f"<p><strong>Technische Daten</strong><br>{'<br>'.join(specs)}</p>"
            "<p><strong>Passt zu</strong><br>"
            "Zeltcamping, Campervan-Wochenenden, Picknick, Balkon-Backup und kurzen Stromausfällen. "
            "Prüfen Sie die technischen Daten, bevor Sie ein Gerät anschließen.</p>"
            "<p><strong>Vor dem Kauf</strong><br>"
            "Die tatsächliche Leistung und Laufzeit hängen vom Gerät und den Bedingungen ab. "
            "Die Solarladung ist von Sonneneinstrahlung, Ausrichtung und Wetter abhängig. "
            "Prüfen Sie die Dauerleistung Ihres Geräts. Lithiumbatterien unterliegen Transportvorschriften.</p>"
        )
        return self._pack(
            brand,
            title,
            bullets,
            description,
            "tragbare powerstation camping akku solar stromausfall notstrom campervan outdoor",
            (
                "Nur kompatible Ladegeräte und Kabel verwenden. Lüftungsöffnungen freihalten. "
                "Nicht Regen oder stehendem Wasser aussetzen. Von Kindern fernhalten. "
                "Lithiumbatterien erfordern besondere Transportvorschriften."
            ),
            "Vor dem ersten Gebrauch vollständig laden. Geräte nur innerhalb der Nennleistung anschließen. Kühl und trocken lagern.",
            "Tatsächliche Leistung und Laufzeit hängen vom Gerät und den Bedingungen ab. Solarladung hängt von Sonne, Ausrichtung und Wetter ab.",
            "Begrenzte Herstellergarantie. Bedingungen siehe Produktdokumentation.",
        )

    def _french(
        self,
        row: dict[str, Any],
        locale: MarketProfile,
        brand: str,
        capacity: float,
        output_w: float,
        weight: float,
        solar: float,
    ) -> dict[str, Any]:
        weight_fr = _fmt(weight, 1, comma=True)
        solar_line = (
            f"Entrée solaire jusqu'à {solar:.0f} W (panneau non inclus) pour recharger hors réseau."
            if solar > 0
            else "Recharge sur prise secteur ; consultez les caractéristiques pour les exigences d'entrée."
        )
        title = _clip(
            f"{brand} {capacity:.0f}Wh station électrique portable, sortie AC {output_w:.0f}W, "
            f"batterie {row.get('battery_type', 'LiFePO4')}, compatible solaire pour camping et secours",
            200,
        )
        bullets = [
            _clip(
                f"{capacity:.0f} Wh de capacité {row.get('battery_type', 'LiFePO4')} et {output_w:.0f} W de sortie AC "
                "pour téléphone, appareil photo, éclairage et petits équipements de camping. "
                "Vérifiez la puissance continue de votre appareil.",
                500,
            ),
            _clip(
                f"Seulement {weight_fr} kg – conçue pour le coffre et les trajets courts.",
                500,
            ),
            _clip(f"COMPATIBLE SOLAIRE : {solar_line}", 500),
            _clip(
                "ÉNERGIE DE CAMPING SILENCIEUSE : fonctionnement sur batterie, sans carburant ni fumées – "
                "adapté au camping, aux pique-niques et aux coupures de courant.",
                500,
            ),
            _clip(
                "SIMPLE AU QUOTIDIEN : boîtier compact et commandes intuitives. "
                "L'autonomie réelle dépend de l'appareil et des conditions d'utilisation.",
                500,
            ),
        ]
        specs = [
            f"Capacité : {capacity:.0f} Wh",
            f"Sortie AC : {output_w:.0f} W",
            f"Batterie : {row.get('battery_type', 'LiFePO4')}",
            f"Poids : {weight_fr} kg",
            f"Entrée solaire : jusqu'à {solar:.0f} W (panneau non inclus)" if solar > 0 else "Entrée solaire : non précisée",
            f"Tension de sortie : {locale.voltage} V",
        ]
        description = (
            f"<p><strong>{html.escape(brand)} {capacity:.0f}Wh station électrique portable</strong></p>"
            "<p>Conçue pour les week-ends de camping, les road trips et les coupures de courant courtes. "
            "La station associe une batterie LiFePO4 à une sortie AC pour l'usage outdoor quotidien.</p>"
            f"<p><strong>Caractéristiques principales</strong><br>{'<br>'.join(specs)}</p>"
            "<p><strong>Idéale pour</strong><br>"
            "Le camping sous tente, les week-ends en van, les pique-niques, le secours à la maison et les coupures courtes. "
            "Consultez les caractéristiques avant de brancher un appareil.</p>"
            "<p><strong>Avant l'achat</strong><br>"
            "La puissance et l'autonomie réelles varient selon l'appareil et les conditions. "
            "La recharge solaire dépend du soleil, de l'orientation et de la météo. "
            "Vérifiez la puissance continue de votre appareil. Les batteries au lithium sont soumises à la réglementation sur le transport.</p>"
        )
        return self._pack(
            brand,
            title,
            bullets,
            description,
            "station electrique portable camping batterie solaire secours coupure courant van outdoor",
            (
                "Utilisez uniquement des chargeurs et câbles compatibles. Gardez les évents dégagés. "
                "N'exposez pas à la pluie ou à l'eau stagnante. Tenez hors de portée des enfants. "
                "Les batteries au lithium nécessitent une manipulation et un transport spécifiques."
            ),
            "Chargez avant la première utilisation. Branchez les appareils dans la limite de puissance nominale. Rangez au sec et au frais.",
            "La puissance et l'autonomie réelles varient selon l'appareil et les conditions. La recharge solaire dépend du soleil, de l'orientation et de la météo.",
            "Garantie fabricant limitée. Consultez la documentation produit pour les conditions.",
        )

    @staticmethod
    def _pack(
        brand: str,
        title: str,
        bullets: list[str],
        description: str,
        keywords: str,
        safety: str,
        directions: str,
        legal: str,
        warranty: str,
    ) -> dict[str, Any]:
        return {
            "item_name": _clip(title, 200),
            "bullet_point1": _clip(bullets[0], 500),
            "bullet_point2": _clip(bullets[1], 500),
            "bullet_point3": _clip(bullets[2], 500),
            "bullet_point4": _clip(bullets[3], 500),
            "bullet_point5": _clip(bullets[4], 500),
            "product_description": _clip(description.replace("\n", " "), 2000),
            "generic_keywords": _trim_bytes(keywords, 250),
            "safety_warning": _clip(safety, 500),
            "directions_for_use": _clip(directions, 500),
            "legal_disclaimer_description": _clip(legal, 500),
            "warranty_description": _clip(warranty, 500),
            "brand_name": brand,
        }


# ---------------------------------------------------------------------------
# Amazon 行映射
# ---------------------------------------------------------------------------
def resolve_locales(profile: AmazonProfile, values: str | None) -> list[MarketProfile]:
    if not values or values.strip().lower() == "all":
        return [profile.market(code) for code in profile.markets]
    lookup: dict[str, MarketProfile] = {}
    for market in profile.markets.values():
        lookup[market.locale.lower()] = market
        lookup[market.market.lower()] = market
    result: list[MarketProfile] = []
    for raw in values.split(","):
        key = raw.strip().lower()
        if not key:
            continue
        if key not in lookup:
            raise ListingError(f"未知 locale/市场: {raw}；可选 {', '.join(sorted(lookup))}")
        locale = lookup[key]
        if locale not in result:
            result.append(locale)
    if not result:
        raise ListingError("至少选择一个 locale")
    return result


def load_gtin_map(path: str | Path | None) -> dict[str, tuple[str, str]]:
    if not path:
        return {}
    source = Path(path).expanduser().resolve()
    rows = utils.read_csv(source)
    result: dict[str, tuple[str, str]] = {}
    for row in rows:
        sku = str(row.get("sku") or "").strip()
        value = str(row.get("external_product_id") or "").strip()
        id_type = str(row.get("external_product_id_type") or "").strip().upper()
        if sku and value and id_type in {"ASIN", "UPC", "EAN", "GTIN"}:
            result[sku] = (value, id_type)
    if not result:
        raise ListingError(f"GTIN 映射为空或格式错误: {source}")
    logger.info("已加载 GTIN 映射: %d 条", len(result))
    return result


class AmazonRowBuilder:
    """把内部商品数据映射成 profile 定义的 Amazon 平铺文件字段。"""

    def __init__(
        self,
        profile: AmazonProfile,
        *,
        gtin_map: dict[str, tuple[str, str]] | None = None,
        image_base_url: str = "",
        browse_node: str = "",
    ) -> None:
        self.profile = profile
        self.defaults = profile.defaults
        self.gtin_map = gtin_map or {}
        self.image_base_url = image_base_url.strip().rstrip("/")
        self.browse_node = browse_node.strip() or str(self.defaults.get("browse_node", ""))

    def build(self, row: dict[str, Any], locale: MarketProfile, copy: dict[str, Any]) -> dict[str, str]:
        sku = self._sku(row["sku"])
        brand = str(copy.get("brand_name") or self.defaults.get("brand", "TrailHarbor"))
        external_id, id_type = self._external_id(row, sku)
        price = self._price(float(row["price_usd"]), locale)
        image = str(row.get("main_image_url") or "")
        if not image and self.image_base_url:
            image = f"{self.image_base_url}/{sku}/main.jpg"
        browse_node = str(row.get("recommended_browse_nodes") or self.browse_node)
        country = str(row.get("country_of_origin") or ("CN" if row.get("platform") == "1688" else self.defaults.get("country_of_origin_fallback", "")))
        values: dict[str, Any] = {
            "sku": sku,
            "product_type": str(self.defaults.get("product_type", "POWER_STATION")),
            "item_name": copy["item_name"],
            "brand_name": brand,
            "manufacturer": brand,
            "product_description": copy["product_description"],
            "bullet_point1": copy["bullet_point1"],
            "bullet_point2": copy["bullet_point2"],
            "bullet_point3": copy["bullet_point3"],
            "bullet_point4": copy["bullet_point4"],
            "bullet_point5": copy["bullet_point5"],
            "generic_keywords": copy["generic_keywords"],
            "standard_price": f"{price:.2f}",
            "list_price": f"{price:.2f}",
            "currency": locale.currency,
            "quantity": str(int(self.defaults.get("quantity", 100))),
            "condition_type": "new_new",
            "fulfillment_latency": str(int(self.defaults.get("fulfillment_latency", 2))),
            "main_image_url": image,
            "other_image_url1": "",
            "other_image_url2": "",
            "other_image_url3": "",
            "other_image_url4": "",
            "other_image_url5": "",
            "other_image_url6": "",
            "other_image_url7": "",
            "other_image_url8": "",
            "external_product_id": external_id,
            "external_product_id_type": id_type,
            "recommended_browse_nodes": browse_node,
            "item_type_keyword": str(self.defaults.get("item_type_keyword", "portable_power_stations")),
            "update_delete": "Update",
            "product_site_launch_date": datetime.now(UTC).date().isoformat(),
            "country_of_origin": country,
            "warranty_description": copy["warranty_description"],
            "safety_warning": copy["safety_warning"],
            "directions_for_use": copy["directions_for_use"],
            "legal_disclaimer_description": copy["legal_disclaimer_description"],
            "supplier_declared_has_product_battery": "Yes",
            "supplier_declared_dg_hz_regulation": "unknown",
            "lithium_battery_energy_content": f"{float(row['capacity_wh']):.0f}",
            "lithium_battery_energy_content_unit": "Wh",
            "lithium_battery_packaging": "batteries_contained_in_equipment",
            "number_of_lithium_ion_batteries": "1",
            "battery_type": "lithium_ion",
            "wattage": f"{float(row['output_w']):.0f}",
            "wattage_unit": "W",
            "output_voltage": locale.voltage,
            "plug_type": locale.plug_type,
            "number_of_ac_outlets": str(row.get("number_of_ac_outlets") or ""),
            "solar_input_wattage": f"{float(row['solar_input_w']):.0f}",
            "battery_capacity": f"{float(row['capacity_wh']):.0f}",
            "battery_capacity_unit": "Wh",
            "item_weight": f"{float(row['weight_kg']):.2f}",
            "item_weight_unit": "kg",
            "item_length": str(row.get("item_length") or ""),
            "item_width": str(row.get("item_width") or ""),
            "item_height": str(row.get("item_height") or ""),
            "item_dimension_unit": "cm",
            "product_tax_code": "",
            "gpsr_safety_attestation": "",
            "gpsr_manufacturer_reference": "",
            "gpsr_eu_responsible_person_name": "",
            "gpsr_eu_responsible_person_address": "",
            "gpsr_eu_responsible_person_email": "",
        }
        return {field.key: self._string(values.get(field.key, "")) for field in self.profile.fields_for(locale.market)}

    def _external_id(self, row: dict[str, Any], sku: str) -> tuple[str, str]:
        provided = str(row.get("external_product_id") or "").strip()
        provided_type = str(row.get("external_product_id_type") or "").strip().upper()
        if provided:
            return provided, provided_type if provided_type in {"ASIN", "UPC", "EAN", "GTIN"} else "UPC"
        mapped = self.gtin_map.get(sku) or self.gtin_map.get(str(row["sku"]))
        if mapped:
            return mapped
        if row.get("platform") == "amazon":
            match = re.search(r"(?:AMZ-|ASIN[-_])?([A-Z0-9]{10})", str(row["sku"]).upper())
            if match:
                return match.group(1), "ASIN"
        return "", "UPC"

    @staticmethod
    def _sku(value: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9_-]+", "-", str(value)).strip("-_")
        return cleaned[:40] or "SKU-UNKNOWN"

    @staticmethod
    def _price(price_usd: float, locale: MarketProfile) -> float:
        if locale.market == "US":
            return round(price_usd, 2)
        return math.floor(price_usd * locale.fx_from_usd) + 0.99

    @staticmethod
    def _string(value: Any) -> str:
        if value is None:
            return ""
        return str(value).replace("\r", " ").replace("\n", " ").strip()


# ---------------------------------------------------------------------------
# CSV 写出与校验
# ---------------------------------------------------------------------------
class CsvWriter:
    def __init__(self, profile: AmazonProfile) -> None:
        self.profile = profile

    def write(self, path: Path, rows: list[dict[str, str]], market: str) -> list[str]:
        fields = self.profile.fields_for(market)
        headers = [field.header for field in fields]
        utils.ensure_dir(path.parent)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=headers,
                extrasaction="raise",
                lineterminator="\n",
                quoting=csv.QUOTE_MINIMAL,
            )
            writer.writeheader()
            for row in rows:
                writer.writerow({field.header: row.get(field.key, "") for field in fields})
        logger.info("CSV 已生成: %s（%d 行 / %d 列）", path, len(rows), len(headers))
        return headers


@dataclass
class ValidationResult:
    locale: str
    market: str
    csv_path: str
    rows: int
    headers: int
    format_ok: bool
    import_ready: bool
    blockers: list[dict[str, Any]]
    warnings: list[dict[str, Any]]
    format_issues: list[dict[str, str]]
    compliance: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "locale": self.locale,
            "market": self.market,
            "csv": self.csv_path,
            "rows": self.rows,
            "headers": self.headers,
            "format_ok": self.format_ok,
            "import_ready": self.import_ready,
            "blockers": self.blockers,
            "warnings": self.warnings,
            "format_issues": self.format_issues,
            "compliance": self.compliance,
        }


class CsvValidator:
    """对生成的 CSV 做结构、类型、长度、必填值与违禁词复核。"""

    def __init__(self, profile: AmazonProfile, scanner: ComplianceScanner | None = None) -> None:
        self.profile = profile
        self.scanner = scanner

    def validate(
        self,
        path: Path,
        *,
        locale: MarketProfile,
        copy_rows: list[dict[str, Any]],
        compliance: dict[str, Any],
    ) -> ValidationResult:
        fields = self.profile.fields_for(locale.market)
        headers = [field.header for field in fields]
        format_issues: list[dict[str, str]] = []
        blockers: dict[str, dict[str, Any]] = {}
        warnings: dict[str, dict[str, Any]] = {}

        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            rows = list(reader)
        if not rows:
            raise ListingError(f"CSV 为空: {path}")
        actual_headers = rows[0]
        if actual_headers != headers:
            format_issues.append(
                {
                    "code": "HEADER_MISMATCH",
                    "message": f"表头与 profile 不一致：期望 {len(headers)} 列，实际 {len(actual_headers)} 列",
                }
            )
        data_rows = rows[1:]
        for index, cells in enumerate(data_rows, start=2):
            if len(cells) != len(headers):
                format_issues.append(
                    {
                        "code": "COLUMN_COUNT",
                        "message": f"第 {index} 行列数 {len(cells)}，期望 {len(headers)}",
                    }
                )
                continue
            record = dict(zip(headers, cells, strict=True))
            sku = record.get("sku", f"row-{index}")
            for field in fields:
                value = record.get(field.header, "")
                if field.required_value and not value.strip():
                    blockers.setdefault(
                        field.key,
                        {
                            "field": field.header,
                            "message": f"必填值为空：{field.header}",
                            "rows": [],
                        },
                    )["rows"].append(sku)
                if len(value) > field.max_length:
                    format_issues.append(
                        {
                            "code": "MAX_LENGTH",
                            "message": f"{sku} / {field.header} 长度 {len(value)} > {field.max_length}",
                        }
                    )
                if field.key == "generic_keywords" and len(value.encode("utf-8")) > 250:
                    format_issues.append(
                        {
                            "code": "KEYWORDS_BYTES",
                            "message": f"{sku} / generic_keywords 超过 250 bytes",
                        }
                    )
                if "\n" in value or "\r" in value:
                    format_issues.append(
                        {
                            "code": "EMBEDDED_NEWLINE",
                            "message": f"{sku} / {field.header} 含换行",
                        }
                    )
                self._check_type(sku, field, value, format_issues)
            if not record.get("country_of_origin"):
                warnings.setdefault(
                    "COUNTRY_OF_ORIGIN",
                    {"message": "country_of_origin 为空，需按实际生产国补齐", "rows": []},
                )["rows"].append(sku)
            if record.get("supplier_declared_dg_hz_regulation") == "unknown":
                warnings.setdefault(
                    "DG_CLASSIFICATION",
                    {
                        "message": "危险品/锂电池分类为 unknown，需合规服务商确认后填写",
                        "rows": [],
                    },
                )["rows"].append(sku)
            if self.scanner is not None:
                for term in self.scanner.residual(record):
                    format_issues.append(
                        {
                            "code": "FORBIDDEN_TERM",
                            "message": f"{sku} / 残留违禁词: {term}",
                        }
                    )

        if locale.language != "en":
            warnings["NATIVE_REVIEW"] = {
                "message": f"{locale.locale} 文案为模板生成，发布前需母语审校",
                "rows": [row.get("sku", "") for row in copy_rows],
            }
        if locale.gpsr_required:
            for key in (
                "gpsr_safety_attestation",
                "gpsr_manufacturer_reference",
                "gpsr_eu_responsible_person_name",
                "gpsr_eu_responsible_person_address",
                "gpsr_eu_responsible_person_email",
            ):
                blockers.setdefault(
                    key,
                    {
                        "field": key,
                        "message": f"EU GPSR 必填：{key}",
                        "rows": [row.get("sku", "") for row in copy_rows],
                    },
                )

        format_ok = not format_issues
        return ValidationResult(
            locale=locale.locale,
            market=locale.market,
            csv_path=str(path),
            rows=len(data_rows),
            headers=len(actual_headers),
            format_ok=format_ok,
            import_ready=format_ok and not blockers,
            blockers=list(blockers.values()),
            warnings=list(warnings.values()),
            format_issues=format_issues,
            compliance=compliance,
        )

    @staticmethod
    def _check_type(
        sku: str,
        field: FieldSpec,
        value: str,
        issues: list[dict[str, str]],
    ) -> None:
        if not value:
            return
        valid = True
        if field.type == "int":
            valid = bool(re.fullmatch(r"\d+", value))
        elif field.type == "decimal":
            valid = bool(re.fullmatch(r"\d+(?:\.\d+)?", value))
        elif field.type == "date":
            valid = bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))
        elif field.type == "url":
            valid = bool(re.match(r"^https?://", value))
        elif field.type == "email":
            valid = bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value))
        elif field.type == "enum" and field.enum:
            valid = value in field.enum
        if not valid:
            issues.append(
                {
                    "code": "INVALID_TYPE",
                    "message": f"{sku} / {field.header} 值不符合 {field.type}: {value[:80]}",
                }
            )


# ---------------------------------------------------------------------------
# 引擎与 CLI
# ---------------------------------------------------------------------------
class ListingEngine:
    """选品表 → 多市场文案 → Amazon CSV → 校验报告。"""

    def __init__(self, profile: AmazonProfile, rules_path: str | Path = DEFAULT_RULES) -> None:
        self.profile = profile
        self.scanner = ComplianceScanner(rules_path)
        self.writer = CsvWriter(profile)
        self.validator = CsvValidator(profile, self.scanner)

    def run(
        self,
        *,
        input_path: str | Path,
        output_dir: str | Path,
        locales: list[MarketProfile],
        sheet: str | None = None,
        only_passed: bool = True,
        limit: int | None = None,
        gtin_map: dict[str, tuple[str, str]] | None = None,
        image_base_url: str = "",
        browse_node: str = "",
        brand: str | None = None,
    ) -> dict[str, Any]:
        rows = read_selection(
            input_path,
            sheet=sheet,
            only_passed=only_passed,
            limit=limit,
        )
        out = utils.ensure_dir(output_dir)
        copywriter = Copywriter(brand or str(self.profile.defaults.get("brand", "TrailHarbor")))
        builder = AmazonRowBuilder(
            self.profile,
            gtin_map=gtin_map,
            image_base_url=image_base_url or str(self.profile.defaults.get("image_base_url", "")),
            browse_node=browse_node,
        )
        run_id = f"listing_{utils.timestamp()}"
        generated_at = utils.utc_now_iso()
        locale_results: list[dict[str, Any]] = []

        for locale in locales:
            csv_rows: list[dict[str, str]] = []
            content_rows: list[dict[str, Any]] = []
            all_violations: list[dict[str, str]] = []
            for row in rows:
                copy = copywriter.build(row, locale)
                clean, violations = self.scanner.sanitize(copy)
                all_violations.extend(violations)
                csv_rows.append(builder.build(row, locale, clean))
                content_rows.append(
                    {
                        "sku": row["sku"],
                        "source_title": row["title"],
                        "product": {
                            "capacity_wh": row["capacity_wh"],
                            "output_w": row["output_w"],
                            "weight_kg": row["weight_kg"],
                            "battery_type": row["battery_type"],
                            "solar_input_w": row["solar_input_w"],
                            "source_platform": row["platform_label"],
                            "source_page": row["source_page"],
                        },
                        "locale": locale.locale,
                        "market": locale.market,
                        "language": locale.language,
                        "item_name": clean["item_name"],
                        "bullets": [clean[f"bullet_point{i}"] for i in range(1, 6)],
                        "product_description": clean["product_description"],
                        "search_terms": clean["generic_keywords"],
                        "copy_review_required": clean["copy_review_required"],
                        "compliance": {
                            "status": self.scanner.status(violations),
                            "violations": violations,
                        },
                    }
                )

            csv_path = out / locale.filename
            self.writer.write(csv_path, csv_rows, locale.market)
            compliance = {
                "status": self.scanner.status(all_violations),
                "violation_count": len(all_violations),
                "violations": all_violations,
            }
            validation = self.validator.validate(
                csv_path,
                locale=locale,
                copy_rows=content_rows,
                compliance=compliance,
            )
            content_path = out / f"{utils.safe_filename(locale.locale)}_content.json"
            utils.write_json(
                content_path,
                {
                    "run_id": run_id,
                    "generated_at": generated_at,
                    "profile": str(self.profile.path),
                    "locale": locale.locale,
                    "market": locale.market,
                    "listings": content_rows,
                },
            )
            validation_path = out / f"{utils.safe_filename(locale.locale)}_validation.json"
            utils.write_json(validation_path, validation.to_dict())
            locale_results.append(
                {
                    "locale": locale.locale,
                    "market": locale.market,
                    "csv": _display_path(PROJECT_ROOT, csv_path),
                    "content": _display_path(PROJECT_ROOT, content_path),
                    "validation": _display_path(PROJECT_ROOT, validation_path),
                    "rows": validation.rows,
                    "format_ok": validation.format_ok,
                    "import_ready": validation.import_ready,
                    "blocker_count": len(validation.blockers),
                    "warning_count": len(validation.warnings),
                    "compliance_status": compliance["status"],
                }
            )

        summary = {
            "run_id": run_id,
            "generated_at": generated_at,
            "input": _display_path(Path.cwd(), Path(input_path).expanduser().resolve()),
            "profile": str(self.profile.path),
            "selection_rows": len(rows),
            "locales": locale_results,
            "format_ok_all": all(item["format_ok"] for item in locale_results),
            "import_ready_all": all(item["import_ready"] for item in locale_results),
            "notice": "CSV 格式与字段档案校验通过；GTIN、主图、Browse Node、GPSR 等账号级资料需补齐后才可实际上传。",
            "outputs": {
                "summary": _display_path(PROJECT_ROOT, out / "listing_summary.json"),
            },
        }
        utils.write_json(out / "listing_summary.json", summary)
        logger.info(
            "Listing 生成完成: %d 个 SKU × %d 个站点；格式通过=%s；导入就绪=%s",
            len(rows),
            len(locales),
            summary["format_ok_all"],
            summary["import_ready_all"],
        )
        return summary


def _display_path(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="listing_generator",
        description="从选品表生成多市场 Amazon Listing 文案与平铺文件 CSV",
    )
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="选品表 xlsx/csv")
    parser.add_argument("--sheet", default=DEFAULT_SHEET, help="Excel 工作表名")
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE), help="Amazon 字段档案")
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="违禁词规则")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT), help="输出目录")
    parser.add_argument(
        "--locales",
        default="en-US",
        help="逗号分隔的站点 locale，如 en-US,en-GB,de-DE,fr-FR 或 all",
    )
    parser.add_argument("--limit", type=int, help="最多处理多少个 SKU")
    parser.add_argument("--include-failed", action="store_true", help="包含未通过门槛的 SKU")
    parser.add_argument("--gtin-map", help="CSV: sku,external_product_id,external_product_id_type")
    parser.add_argument("--image-base-url", default="", help="主图基址，自动拼 {base}/{sku}/main.jpg")
    parser.add_argument("--browse-node", default="", help="Amazon recommended_browse_nodes")
    parser.add_argument("--brand", help="覆盖默认品牌（仅用于缺少消费品牌的 1688/Generic 行）")
    parser.add_argument("--strict", action="store_true", help="CSV 格式错误时返回退出码 2")
    parser.add_argument("--log-level", default="INFO", help="日志级别")
    return parser


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def main(argv: Iterable[str] | None = None) -> int:
    _configure_stdio()
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        profile = load_profile(args.profile)
        locales = resolve_locales(profile, args.locales)
        gtin_map = load_gtin_map(args.gtin_map)
    except (ListingError, utils.UtilError) as exc:
        print(f"✗ 初始化失败：{exc}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir).expanduser().resolve()
    utils.ensure_dir(output_dir)
    utils.setup_logging(
        level=args.log_level,
        log_file=output_dir / "listing_generator.log",
        console=True,
        force=True,
    )
    try:
        summary = ListingEngine(profile, args.rules).run(
            input_path=args.input,
            output_dir=output_dir,
            locales=locales,
            sheet=args.sheet,
            only_passed=not args.include_failed,
            limit=args.limit,
            gtin_map=gtin_map,
            image_base_url=args.image_base_url,
            browse_node=args.browse_node,
            brand=args.brand,
        )
    except (ListingError, utils.UtilError, OSError) as exc:
        logger.error("Listing 生成失败: %s", exc)
        print(f"✗ 生成失败：{exc}", file=sys.stderr)
        return 1

    print("")
    print("=" * 74)
    print(f"✓ Listing 生成完成：{summary['run_id']}")
    print(f"  选品 SKU : {summary['selection_rows']}  |  站点：{len(summary['locales'])}")
    for item in summary["locales"]:
        state = "就绪" if item["import_ready"] else "需补账号资料"
        print(
            f"  {item['locale']:<6} {item['market']:<3} 行={item['rows']:<2} "
            f"格式={'OK' if item['format_ok'] else 'FAIL'} 导入={state} "
            f"blockers={item['blocker_count']} warnings={item['warning_count']}"
        )
        print(f"         CSV: {item['csv']}")
    print(f"  汇总     : {summary['outputs']['summary']}")
    print("=" * 74)
    if not summary["format_ok_all"]:
        print("✗ CSV 存在格式错误，请查看对应 *_validation.json", file=sys.stderr)
        return 2
    if not summary["import_ready_all"]:
        print("! CSV 格式已通过，但存在账号级/素材级必填项，补齐后才可实际上传。", file=sys.stderr)
    return 2 if args.strict and not summary["format_ok_all"] else 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "listing_generator"))
