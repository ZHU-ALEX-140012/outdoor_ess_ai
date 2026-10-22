"""全链路编排器。

数据流：
    collect → normalize → analyze → listing → content → compliance → report

每个阶段都写入 manifest，失败时保留已完成阶段的产物，便于定位与重跑。
"""

from __future__ import annotations

import time
import traceback
from collections.abc import Callable
from typing import Any

import utils
from ess_ai.analysis.market_analyzer import MarketAnalyzer
from ess_ai.collectors.mock_collector import MockCollector
from ess_ai.compliance.checker import ComplianceChecker
from ess_ai.config import Settings, load_settings
from ess_ai.content.generator import ContentGenerator
from ess_ai.listing.optimizer import ListingOptimizer
from ess_ai.processing.normalizer import DataNormalizer
from ess_ai.reporting.report_builder import ReportBuilder
from ess_ai.storage.repository import RunStore

logger = utils.get_logger(__name__)


class FullChainPipeline:
    """离线优先的端到端流水线。"""

    def __init__(
        self,
        settings: Settings | None = None,
        *,
        seed: int | None = None,
        markets: list[str] | None = None,
    ) -> None:
        self.settings = settings or load_settings()
        self.seed = int(seed if seed is not None else self.settings.get("project.seed", 20260401))
        self.markets = [str(x).upper() for x in (markets or self.settings.markets)]
        self.run_store = RunStore(self.settings.path("paths.runs_dir"))
        self.collector = MockCollector(self.settings, seed=self.seed, markets=self.markets)
        self.normalizer = DataNormalizer(self.settings)
        self.analyzer = MarketAnalyzer(self.settings)
        self.listing = ListingOptimizer(self.settings)
        self.content = ContentGenerator(self.settings)
        self.compliance = ComplianceChecker(self.settings)
        self.reporter = ReportBuilder(self.settings)

    # ------------------------------------------------------------------
    def run(self) -> dict[str, Any]:
        """执行全链路并返回运行结果摘要。"""

        self.settings.ensure_directories()
        run_id = f"run_{utils.timestamp()}_{self.seed}"
        self.run_store.create(
            run_id,
            {
                "project": self.settings.project_name,
                "version": self.settings.get("project.version", "0.1.0"),
                "mode": self.settings.mode,
                "model": self.settings.get("llm.model"),
                "seed": self.seed,
                "markets": self.markets,
                "started_at": utils.utc_now_iso(),
                "data_policy": "simulated-public-proxy / no marketplace API",
            },
        )
        logger.info("流水线启动: %s", run_id)

        artifacts: dict[str, Any] = {}
        try:
            raw = self._stage(run_id, "01_collect", lambda: self.collector.collect(run_id))
            artifacts["raw"] = raw

            normalized = self._stage(
                run_id, "02_normalize", lambda: self.normalizer.normalize(raw)
            )
            artifacts["normalized"] = normalized

            analysis = self._stage(
                run_id, "03_analyze", lambda: self.analyzer.analyze(normalized)
            )
            artifacts["analysis"] = analysis

            listings = self._stage(
                run_id, "04_listing", lambda: self.listing.generate(analysis, normalized)
            )
            artifacts["listings"] = listings

            content = self._stage(
                run_id, "05_content", lambda: self.content.generate(listings)
            )
            artifacts["content"] = content

            compliance = self._stage(
                run_id, "06_compliance", lambda: self.compliance.check(listings)
            )
            artifacts["compliance"] = compliance

            manifest_before_report = self.run_store.load(run_id)
            manifest_before_report.setdefault("stages", []).append(
                {
                    "name": "07_report",
                    "status": "success",
                    "elapsed_ms": 0,
                    "outputs": [],
                }
            )
            report = self._stage(
                run_id,
                "07_report",
                lambda: self.reporter.build(
                    run_id=run_id,
                    analysis=analysis,
                    listings=listings,
                    content=content,
                    compliance=compliance,
                    manifest=manifest_before_report,
                ),
            )
            artifacts["report"] = report

            final_manifest = self.run_store.finalize(
                run_id,
                status="success",
                summary=report["summary"],
            )
            logger.info("流水线完成: %s | 报告: %s", run_id, report["report_path"])
            return {
                "run_id": run_id,
                "status": "success",
                "manifest_path": str(final_manifest.relative_to(self.settings.root)),
                "report_path": report["report_path"],
                "summary": report["summary"],
                "artifacts": artifacts,
            }
        except Exception as exc:
            logger.error("流水线失败: %s", exc)
            logger.debug("失败堆栈:\n%s", traceback.format_exc())
            self.run_store.finalize(
                run_id,
                status="failed",
                summary={"error": f"{type(exc).__name__}: {exc}"},
            )
            raise

    # ------------------------------------------------------------------
    def _stage(self, run_id: str, name: str, func: Callable[[], dict[str, Any]]) -> dict[str, Any]:
        logger.info("▶ 阶段开始: %s", name)
        started = time.perf_counter()
        try:
            result = func()
            elapsed_ms = (time.perf_counter() - started) * 1000
            outputs = self._artifact_paths(result)
            self.run_store.add_stage(
                run_id,
                name=name,
                status="success",
                elapsed_ms=elapsed_ms,
                outputs=outputs,
            )
            logger.info("✓ 阶段完成: %s（%.0f ms）", name, elapsed_ms)
            return result
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - started) * 1000
            self.run_store.add_stage(
                run_id,
                name=name,
                status="failed",
                elapsed_ms=elapsed_ms,
                error=f"{type(exc).__name__}: {exc}",
            )
            raise

    @staticmethod
    def _artifact_paths(result: dict[str, Any]) -> list[str]:
        artifacts = result.get("artifacts")
        if not isinstance(artifacts, dict):
            return []
        return [str(value) for value in artifacts.values() if value]
