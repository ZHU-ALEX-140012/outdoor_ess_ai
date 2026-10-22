"""全链路冒烟测试与合规规则测试。"""

from __future__ import annotations

import utils
from ess_ai.compliance.checker import ComplianceChecker
from ess_ai.config import Settings
from ess_ai.integrations.llm_client import DeepSeekClient
from ess_ai.pipelines.full_chain import FullChainPipeline


def test_full_chain_pipeline(temp_settings: Settings) -> None:
    pipeline = FullChainPipeline(temp_settings, seed=42, markets=["US", "DE"])
    result = pipeline.run()

    assert result["status"] == "success"
    assert result["run_id"].startswith("run_")
    assert result["summary"]["listing_count"] > 0
    assert result["summary"]["content_pack_count"] > 0
    assert (temp_settings.root / result["report_path"]).exists()
    assert (temp_settings.root / result["manifest_path"]).exists()

    manifest = utils.read_json(temp_settings.root / result["manifest_path"])
    stage_names = [stage["name"] for stage in manifest["stages"]]
    assert stage_names == [
        "01_collect",
        "02_normalize",
        "03_analyze",
        "04_listing",
        "05_content",
        "06_compliance",
        "07_report",
    ]
    assert manifest["status"] == "success"

    analysis = utils.read_json(temp_settings.path("paths.analysis_dir") / "market_analysis.json")
    assert analysis["market_scores"]
    assert analysis["market_scores"][0]["market"] in {"US", "DE"}
    assert 0 <= analysis["market_scores"][0]["overall_score"] <= 100


def test_collector_is_deterministic(temp_settings: Settings) -> None:
    from ess_ai.collectors.mock_collector import MockCollector

    collector = MockCollector(temp_settings, seed=7, markets=["US"])
    first = collector.collect("run_test_a")
    second = collector.collect("run_test_b")
    assert len(first["products"]) == len(second["products"])
    for left, right in zip(first["products"], second["products"], strict=True):
        assert left["price_local"] == right["price_local"]
        assert left["seller_count"] == right["seller_count"]


def test_compliance_flags_forbidden_claim(temp_settings: Settings) -> None:
    checker = ComplianceChecker(temp_settings)
    disclosures = temp_settings.get("compliance.required_disclosures", [])
    description = "\n".join(disclosures)
    listing = {
        "listing_id": "US_TEST",
        "market": "US",
        "sku": "TEST-1",
        "title": "The best in the world portable power station",
        "bullets": ["600Wh LiFePO4 capacity."],
        "description": description,
        "price_usd": 499,
        "certifications": ["UN38.3", "FCC", "UL 2743", "Prop 65"],
        "compliance": {"gaps": [], "ready": True},
        "copy_review_required": False,
    }
    result = checker.check({"run_id": "run_test", "listings": [listing]})
    codes = {issue["code"] for issue in result["results"][0]["issues"]}
    assert "FORBIDDEN_CLAIM" in codes
    assert result["summary"]["failed"] == 1

    clean_listing = {
        **listing,
        "listing_id": "US_CLEAN",
        "title": "TrailCore Mini 300 Portable Power Station",
    }
    clean_result = checker.check({"run_id": "run_test_clean", "listings": [clean_listing]})
    assert clean_result["results"][0]["passed"] is True
    assert clean_result["results"][0]["issues"] == []


def test_llm_offline_fallback(temp_settings: Settings) -> None:
    client = DeepSeekClient(temp_settings)
    assert client.configured is False
    result = client.complete("system", "user", fallback="offline-template-output")
    assert result.offline is True
    assert result.text == "offline-template-output"
    assert result.model == "deepseek-v4.1-flash"
