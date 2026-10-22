"""竞品监控模块：链接管理、巡检预警、痛点报告与容错测试。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import utils
from competitor_monitor import (
    MonitorEngine,
    MonitorError,
    ProductParser,
    add_competitor,
    detect_platform,
    load_config,
    load_registry,
    remove_competitor,
    run_schedule,
    validate_interval,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write_registry(config, path: Path, entries: list[dict]) -> None:
    utils.write_json(path, {"competitors": entries})


def _demo_entries(config) -> list[dict]:
    return [dict(item) for item in config.get("bootstrap", [])]


def test_detect_platform() -> None:
    assert detect_platform("https://www.amazon.com/dp/B0ABC12345")[0] == "amazon"
    assert detect_platform("https://www.aliexpress.com/item/1005001234567.html")[0] == "aliexpress"
    assert detect_platform("https://detail.1688.com/offer/600000000001.html")[0] == "alibaba_1688"
    assert detect_platform("https://example.com/product/1")[0] == "generic"


def test_public_product_page_parser() -> None:
    html = """
    <html><body>
      <span id="productTitle">Demo 300Wh Portable Power Station</span>
      <span id="priceblock_ourprice">$299.00</span>
      <div id="detailBullets_feature_div">Best Sellers Rank: #1,200 in Portable Power Stations</div>
      <div data-hook="review">
        <span class="a-icon-alt">1.0 out of 5 stars</span>
        <a data-hook="review-title">Battery drains fast</a>
        <span data-hook="review-body">Battery drained in one evening and runtime was poor.</span>
        <span data-hook="review-date">October 1, 2026</span>
      </div>
    </body></html>
    """
    snapshot = ProductParser().parse(
        url="https://www.amazon.com/dp/B0TEST0001",
        platform="amazon",
        html=html,
    )
    assert snapshot["price"] == 299.0
    assert snapshot["bsr"] == 1200
    assert snapshot["bsr_category"].startswith("Portable Power Stations")
    assert snapshot["reviews"][0]["rating"] == 1
    assert "drained" in snapshot["reviews"][0]["body"]


def test_add_list_remove_custom_link(workspace_tmp: Path) -> None:
    config = load_config()
    registry = workspace_tmp / "registry.json"
    _write_registry(config, registry, _demo_entries(config))
    entry = add_competitor(
        config,
        url="https://www.amazon.com/dp/B0TEST0001",
        name="Custom Public Competitor",
        registry_path=registry,
    )
    assert entry["id"].startswith("cmp-")
    assert entry["platform"] == "amazon"
    assert entry["product_id"] == "B0TEST0001"
    loaded = load_registry(config, path=registry)
    assert any(item["id"] == entry["id"] for item in loaded["competitors"])
    with pytest.raises(MonitorError):
        add_competitor(config, url=entry["url"], registry_path=registry)
    removed = remove_competitor(config, target=entry["id"], registry_path=registry)
    assert removed[0]["id"] == entry["id"]


def test_monitor_alert_and_pain_report(workspace_tmp: Path) -> None:
    config = load_config()
    registry = workspace_tmp / "registry.json"
    _write_registry(config, registry, _demo_entries(config))
    state = workspace_tmp / "state.json"
    output = workspace_tmp / "monitor"
    engine = MonitorEngine(config, registry_path=registry, state_path=state, output_dir=output)

    first = engine.run(mode="offline")
    assert first["counts"]["success"] == 3
    assert first["counts"]["alerts"] == 0
    assert (PROJECT_ROOT / first["report"]).exists()

    second = engine.run(
        mode="offline",
        fixture_path=str(PROJECT_ROOT / "data/mock/competitor_public_snapshots_changed.json"),
    )
    assert second["counts"]["success"] == 3
    assert second["counts"]["alerts"] == 6
    assert second["counts"]["negative_reviews"] == 15
    assert len(second["alert_files"]) == 6
    first_alert = PROJECT_ROOT / second["alert_files"][0]
    assert first_alert.exists()
    assert "竞品监控预警" in first_alert.read_text(encoding="utf-8")
    latest_alerts = output / "alerts" / "latest_alerts.txt"
    text = latest_alerts.read_text(encoding="utf-8")
    assert "PRICE" in text
    assert "BSR" in text
    assert "Demo Amazon 300Wh" in text

    report_md = output / "reports" / "latest_pain_points.md"
    report_text = report_md.read_text(encoding="utf-8")
    assert "高频痛点总览" in report_text
    assert "电池与续航" in report_text
    assert "Demo 1688 320Wh" in report_text

    report_json = json.loads(
        (output / "reports" / "latest_pain_points.json").read_text(encoding="utf-8")
    )
    assert report_json["negative_reviews"] == 15
    assert report_json["categories"]


def test_invalid_link_is_skipped_without_crash(workspace_tmp: Path) -> None:
    config = load_config()
    registry = workspace_tmp / "registry_invalid.json"
    entries = _demo_entries(config)[:1]
    entries.append(
        {
            "id": "bad-link",
            "name": "Broken Link",
            "url": "not-a-valid-url",
            "platform": "amazon",
            "enabled": True,
            "demo": False,
        }
    )
    _write_registry(config, registry, entries)
    engine = MonitorEngine(
        config,
        registry_path=registry,
        state_path=workspace_tmp / "state_invalid.json",
        output_dir=workspace_tmp / "monitor_invalid",
    )
    summary = engine.run(mode="offline")
    assert summary["counts"]["success"] == 1
    assert summary["counts"]["failed"] == 1
    assert any(item["id"] == "bad-link" for item in summary["failures"])


def test_interval_and_schedule_once(workspace_tmp: Path) -> None:
    with pytest.raises(MonitorError):
        validate_interval(0)
    config = load_config()
    registry = workspace_tmp / "registry_schedule.json"
    _write_registry(config, registry, _demo_entries(config)[:1])
    engine = MonitorEngine(
        config,
        registry_path=registry,
        state_path=workspace_tmp / "state_schedule.json",
        output_dir=workspace_tmp / "monitor_schedule",
    )
    cycles = run_schedule(engine, interval_hours=6, max_cycles=1, mode="offline")
    assert cycles == 1
