"""上架素材模块：CSV 字段、文案长度、违禁词与导入校验测试。"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import utils
from listing_generator import (
    ComplianceScanner,
    ListingEngine,
    load_gtin_map,
    load_profile,
    read_selection,
    resolve_locales,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT = PROJECT_ROOT / "outputs" / "research" / "high_potential_products.xlsx"


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def test_read_selection_only_passed() -> None:
    rows = read_selection(INPUT)
    assert len(rows) == 9
    assert all(row["gate_status"] == "通过" for row in rows)
    assert all(100 <= row["capacity_wh"] <= 500 for row in rows)


def test_default_us_csv_copy_and_format(workspace_tmp: Path) -> None:
    profile = load_profile()
    locale = profile.market("US")
    summary = ListingEngine(profile).run(
        input_path=INPUT,
        output_dir=workspace_tmp / "us",
        locales=[locale],
    )
    result = summary["locales"][0]
    assert result["rows"] == 9
    assert result["format_ok"] is True
    assert result["import_ready"] is False
    assert result["blocker_count"] >= 3

    csv_path = workspace_tmp / "us" / "amazon_us_listings.csv"
    headers, rows = _read_csv(csv_path)
    expected = [field.header for field in profile.fields_for("US")]
    assert headers == expected
    assert len(headers) == 60
    assert len(rows) == 9

    scanner = ComplianceScanner()
    banned = ["best", "100% safe", "zero risk", "guaranteed", "unlimited", "cure", "UL listed"]
    for row in rows:
        assert len(row["item_name"]) <= 200
        assert len(row["product_description"]) <= 2000
        assert len(row["generic_keywords"].encode("utf-8")) <= 250
        for index in range(1, 6):
            assert row[f"bullet_point{index}"].strip()
            assert len(row[f"bullet_point{index}"]) <= 500
        assert row["currency"] == "USD"
        assert row["output_voltage"] == "120"
        assert row["standard_price"].replace(".", "").isdigit()
        text = " ".join(
            [row["item_name"], *(row[f"bullet_point{i}"] for i in range(1, 6)), row["product_description"]]
        ).lower()
        assert not any(term in text for term in banned)
        assert scanner.residual(row) == []


def test_all_locales_generate_localized_csv(workspace_tmp: Path) -> None:
    profile = load_profile()
    locales = resolve_locales(profile, "all")
    summary = ListingEngine(profile).run(
        input_path=INPUT,
        output_dir=workspace_tmp / "all",
        locales=locales,
    )
    assert len(summary["locales"]) == 4
    assert summary["format_ok_all"] is True
    for item in summary["locales"]:
        assert item["format_ok"] is True
        path = workspace_tmp / "all" / Path(item["csv"]).name
        assert path.exists()
        headers, rows = _read_csv(path)
        assert len(rows) == 9
        if item["market"] in {"DE", "FR"}:
            assert len(headers) == 65
            assert "gpsr_safety_attestation" in headers

    de_content = json.loads(
        (workspace_tmp / "all" / "de-DE_content.json").read_text(encoding="utf-8")
    )
    fr_content = json.loads(
        (workspace_tmp / "all" / "fr-FR_content.json").read_text(encoding="utf-8")
    )
    assert "Powerstation" in de_content["listings"][0]["item_name"]
    assert "station électrique" in fr_content["listings"][0]["item_name"]
    assert de_content["listings"][0]["copy_review_required"] is True
    assert fr_content["listings"][0]["copy_review_required"] is True


def test_account_assets_make_csv_import_ready(workspace_tmp: Path) -> None:
    profile = load_profile()
    locale = profile.market("US")
    base_dir = workspace_tmp / "ready"
    base_dir.mkdir(parents=True, exist_ok=True)

    selection = read_selection(INPUT)
    gtin_rows = []
    for index, row in enumerate(selection):
        id_type = "ASIN" if row["platform"] == "amazon" else "UPC"
        if id_type == "ASIN":
            value = f"B0{10000000 + index:08d}"
        else:
            value = f"{750000000000 + index:012d}"
        gtin_rows.append(
            {
                "sku": row["sku"],
                "external_product_id": value,
                "external_product_id_type": id_type,
            }
        )
    gtin_path = base_dir / "gtin.csv"
    utils.write_csv(gtin_path, gtin_rows)

    summary = ListingEngine(profile).run(
        input_path=INPUT,
        output_dir=base_dir,
        locales=[locale],
        gtin_map=load_gtin_map(gtin_path),
        image_base_url="https://cdn.example.com/power",
        browse_node="123456",
    )
    result = summary["locales"][0]
    assert result["format_ok"] is True
    assert result["import_ready"] is True
    assert result["blocker_count"] == 0

    _, rows = _read_csv(base_dir / "amazon_us_listings.csv")
    assert all(row["main_image_url"].startswith("https://cdn.example.com/power/") for row in rows)
    assert all(row["recommended_browse_nodes"] == "123456" for row in rows)
    assert all(row["external_product_id"] for row in rows)


def test_forbidden_claim_scanner_rewrites_and_flags() -> None:
    scanner = ComplianceScanner()
    data = {
        "item_name": "Best 100% safe portable power station",
        "generic_keywords": "best camping battery",
    }
    cleaned, violations = scanner.sanitize(data)
    assert "best" not in cleaned["item_name"].lower()
    assert "100% safe" not in cleaned["item_name"].lower()
    assert "best" not in cleaned["generic_keywords"].lower()
    assert violations
    assert scanner.status(violations) == "REVIEW"
    assert scanner.residual(cleaned) == []
