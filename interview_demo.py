#!/usr/bin/env python3
"""面试演示脚本：按顺序运行全链路，并生成 JD 能力点映射讲稿。

用法：
    python interview_demo.py            # 实际执行全部模块并生成讲稿
    python interview_demo.py --no-run   # 只基于现有产物生成讲稿
    python interview_demo.py --quick    # 跳过基础 7 阶段演示
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import utils  # noqa: E402
from error_guard import log_command_error, log_exception  # noqa: E402

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "interview"
OUTPUT_MD = OUTPUT_DIR / "interview_demo.md"
OUTPUT_JSON = OUTPUT_DIR / "interview_demo.json"

STEPS: list[dict[str, Any]] = [
    {
        "id": "research",
        "name": "01 公开数据选品",
        "command": ["product_research.py"],
        "outputs": ["outputs/research/high_potential_products.xlsx", "outputs/research/research_summary.json"],
        "jd": ["市场调研与选品", "数据分析", "Excel 建模", "供应链/成本意识"],
        "talk": (
            "我先用公开数据把 Amazon、AliExpress、1688 的同类产品统一到 100-500Wh 容量段，"
            "清洗价格、重量、评论和搜索量，再计算单 SKU 毛利、市场容量和竞争度。"
            "最终输出带 50+ 字段的 Excel，并用固定种子保证结果可复现。"
        ),
        "questions": "为什么选 100-500Wh？毛利和竞争度怎么定义？数据来源合法吗？",
    },
    {
        "id": "listing",
        "name": "02 多市场 Listing",
        "command": ["listing_generator.py", "--locales", "all"],
        "outputs": ["outputs/listing/amazon_us_listings.csv", "outputs/listing/listing_summary.json"],
        "jd": ["Amazon Listing 优化", "SEO/关键词", "本地化", "平台合规文案"],
        "talk": (
            "选品表直接进入 Listing 模块，生成美/英/德/法四个站点版本，"
            "每个版本包含合规标题、5 点、详情页 HTML、搜索词和安全/法律字段；"
            "违禁词扫描会替换绝对化、认证、医疗、环保类高风险表述，并输出 CSV 校验报告。"
        ),
        "questions": "Amazon 字段怎么保证匹配？DE/FR 文案谁审？违禁词规则怎么维护？",
    },
    {
        "id": "compliance",
        "name": "03 CE/FCC 合规",
        "command": ["compliance_check.py"],
        "outputs": ["outputs/compliance/compliance_check.xlsx", "outputs/compliance/compliance_summary.json"],
        "jd": ["CE/FCC 合规", "认证与测试", "风险控制", "法规意识"],
        "talk": (
            "我把 LVD/EMC/RoHS/WEEE/Battery/GPSR/RED 和 FCC 15B/15C、UL 2743、Prop 65 "
            "拆成可解释规则，对每个 SKU 输出风险分、不符合项和修改建议。"
            "比如欧盟目标市场但只有 120V/60Hz，会直接判高风险，而不是用文案掩盖。"
        ),
        "questions": "CE 是不是证书？SDoC 和 FCC ID 区别？GPSR 责任人是什么？",
    },
    {
        "id": "reports",
        "name": "04 经营报表",
        "command": ["report_generator.py"],
        "outputs": ["outputs/operations/monthly_profit.xlsx", "outputs/operations/report_summary.json"],
        "jd": ["广告投放分析", "库存管理", "财务/利润核算", "ROI 与经营分析"],
        "talk": (
            "用固定种子模拟 30 天经营数据，生成广告日报、库存预警和月度利润。"
            "每个 SKU 都能看到 ROI、库存周转天数、ACOS/ROAS、覆盖天数和建议补货量，"
            "公式在 Excel 指标说明页可复核，适合面试现场讲解。"
        ),
        "questions": "ROI 分母是什么？周转天数为什么用平均库存？ACOS 和 ROI 怎么联动？",
    },
    {
        "id": "monitor",
        "name": "05 竞品监控",
        "command": ["competitor_monitor.py", "run"],
        "outputs": ["outputs/monitor/alerts/latest_alerts.txt", "outputs/monitor/reports/latest_pain_points.md"],
        "jd": ["竞品分析", "价格/排名监控", "公开数据采集", "预警机制"],
        "talk": (
            "竞品模块支持自定义公开链接，默认 6 小时巡检一次，抓价格、BSR/公开排名和公开差评。"
            "价格或排名超过阈值时生成本地 TXT 预警，并从差评里提取高频痛点分类，"
            "单个无效链接会被跳过，不影响其他竞品。"
        ),
        "questions": "怎么规避反爬/合规风险？BSR 缺失怎么办？预警阈值怎么定？",
    },
]

BASE_STEP = {
    "id": "base",
    "name": "06 基础 7 阶段流水线",
    "command": ["main.py", "demo"],
    "outputs": ["outputs/reports/full_chain_report.md"],
    "jd": ["Python 自动化", "系统集成", "工程化", "文档与可维护性"],
    "talk": (
        "最后用轻量 Python 流水线把采集、清洗、分析、Listing、内容、合规、报告串起来，"
        "每个阶段写 manifest，失败保留现场。Streamlit 只是控制台，核心逻辑全部可 CLI 运行。"
    ),
    "questions": "为什么不用 Airflow？失败怎么重跑？数据边界怎么保证？",
}


def _read(path: Path) -> dict[str, Any]:
    try:
        value = utils.read_json(path, default={})
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def collect_metrics() -> dict[str, Any]:
    research = _read(PROJECT_ROOT / "outputs/research/research_summary.json")
    listing = _read(PROJECT_ROOT / "outputs/listing/listing_summary.json")
    compliance = _read(PROJECT_ROOT / "outputs/compliance/compliance_summary.json")
    monitor = _read(PROJECT_ROOT / "outputs/monitor/reports/monitor_summary.json")
    operations = _read(PROJECT_ROOT / "outputs/operations/report_summary.json")
    return {
        "research": {
            "raw": research.get("raw_records"),
            "clean": research.get("cleaned_records"),
            "high": research.get("high_potential_records"),
            "margin": research.get("quality", {}).get("avg_margin_pct"),
        },
        "listing": {
            "locales": len(listing.get("locales", [])),
            "format_ok": listing.get("format_ok_all"),
            "import_ready": listing.get("import_ready_all"),
        },
        "compliance": {
            "high": compliance.get("severity", {}).get("high"),
            "medium": compliance.get("severity", {}).get("medium"),
            "fail": compliance.get("status", {}).get("FAIL"),
            "pass": compliance.get("status", {}).get("PASS"),
        },
        "monitor": {
            "alerts": monitor.get("counts", {}).get("alerts"),
            "negative_reviews": monitor.get("counts", {}).get("negative_reviews"),
            "failed_links": monitor.get("counts", {}).get("failed"),
        },
        "operations": {
            "revenue": operations.get("revenue"),
            "net_profit": operations.get("net_profit"),
            "roi": operations.get("roi"),
            "acos": operations.get("ad_acos"),
            "inventory_alerts": operations.get("inventory_alerts"),
        },
    }


def _run(command: list[str], timeout: int) -> dict[str, Any]:
    full = [sys.executable, *command]
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = str(VENDOR_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    started = time.time()
    try:
        proc = subprocess.run(
            full,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
            check=False,
        )
        elapsed = round(time.time() - started, 2)
        if proc.returncode != 0:
            log_command_error("interview_demo", full, proc.returncode, proc.stdout or "", proc.stderr or "")
        return {
            "command": " ".join(command),
            "returncode": proc.returncode,
            "elapsed_seconds": elapsed,
            "stdout": (proc.stdout or "")[-4000:],
            "stderr": (proc.stderr or "")[-4000:],
        }
    except Exception as exc:
        log_exception(exc, app="interview_demo", context={"command": full})
        return {
            "command": " ".join(command),
            "returncode": -1,
            "elapsed_seconds": round(time.time() - started, 2),
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
        }


def generate_markdown(metrics: dict[str, Any], results: list[dict[str, Any]], *, executed: bool, run_id: str) -> str:
    operations = metrics.get("operations") or {}

    def money(value: Any) -> str:
        return f"${value:,.0f}" if isinstance(value, (int, float)) else "-"

    lines = [
        "# 户外储能出海 AI 自动化系统 · 面试演示脚本",
        "",
        f"> 生成时间：{datetime.now(UTC).isoformat()} ｜ 运行 ID：`{run_id}` ｜ "
        f"模式：{'实际执行' if executed else '基于已有产物'}",
        "",
        "## 一、30 秒项目定位",
        "",
        "> 这是一个面向欧美市场的**户外储能跨境电商 AI 自动化系统**。它把公开数据选品、",
        "> CE/FCC 合规、Amazon Listing、竞品监控、广告/库存/利润报表串成一条本地可运行的链路；",
        "> 默认使用固定种子和公开快照，不依赖真实店铺后台，适合演示与可复现实验。",
        "",
        "**技术栈：** Python / Streamlit / openpyxl / requests / BeautifulSoup / 规则引擎",
        "",
        "**面试岗位映射：** 跨境电商运营、选品分析、Amazon 运营、合规专员、经营分析、自动化运营。",
        "",
        "## 二、系统架构（可画在白板）",
        "",
        "```text",
        "公开数据/模拟快照",
        "   ↓",
        "选品研究 → Listing 生成 → CE/FCC 合规 → 经营报表",
        "   ↓              ↓              ↓",
        "竞品监控 ←──── 预警/痛点 ←──── 经营异常",
        "   ↓",
        "Streamlit 控制台 / 一键启动脚本 / 全局错误日志",
        "```",
        "",
        "## 三、5 分钟演示顺序",
        "",
        "| 时间 | 模块 | 现场动作 | JD 能力点 |",
        "| --- | --- | --- | --- |",
        "| 0:00-0:30 | 项目定位 | 打开 Streamlit 总览 | 业务理解、系统思维 |",
        "| 0:30-1:30 | 选品 | 点“一键运行选品”，展示 Excel | 市场调研、数据分析、选品 |",
        "| 1:30-2:30 | Listing | 展示四站点 CSV/文案 | Amazon 运营、SEO、本地化 |",
        "| 2:30-3:30 | 合规 | 展示风险分/不符合项 | CE/FCC、风险控制 |",
        "| 3:30-4:30 | 经营 | 展示 ROI/周转/库存预警 | 广告、库存、财务分析 |",
        "| 4:30-5:00 | 竞品/工程 | 展示预警 TXT、错误日志 | 竞品分析、自动化、工程化 |",
        "",
        "## 四、核心指标看板",
        "",
        "| 模块 | 指标 | 当前值 |",
        "| --- | --- | --- |",
        f"| 选品 | 高潜力 SKU | {metrics['research'].get('high')} |",
        f"| 选品 | 平均毛利率 | {metrics['research'].get('margin')}% |",
        f"| Listing | 站点版本 | {metrics['listing'].get('locales')} |",
        f"| Listing | 格式校验 | {'通过' if metrics['listing'].get('format_ok') else '需检查'} |",
        f"| 合规 | 高风险/中风险 | {metrics['compliance'].get('high')} / {metrics['compliance'].get('medium')} |",
        f"| 竞品 | 预警 / 差评 | {metrics['monitor'].get('alerts')} / {metrics['monitor'].get('negative_reviews')} |",
        f"| 经营 | 收入 / 净利润 | {money(operations.get('revenue'))} / {money(operations.get('net_profit'))} |",
        f"| 经营 | ROI / ACOS | {operations.get('roi', '-')}% / {operations.get('acos', '-')}% |",
        f"| 经营 | 库存预警 SKU | {operations.get('inventory_alerts', '-')} |",
        "",
        "## 五、逐模块讲解与 JD 能力点",
        "",
    ]
    result_by_id = {item["id"]: item for item in results}
    for step in STEPS + [BASE_STEP]:
        result = result_by_id.get(step["id"], {})
        lines.extend(
            [
                f"### {step['name']}",
                "",
                f"**对应 JD：** {' / '.join(step['jd'])}",
                "",
                f"**现场命令：** `python {' '.join(step['command'])}`",
                "",
                f"**输出：** {', '.join(f'`{x}`' for x in step['outputs'])}",
                "",
                f"**讲解话术：** {step['talk']}",
                "",
                f"**面试官可能追问：** {step['questions']}",
                "",
            ]
        )
        if executed:
            status = "成功" if result.get("returncode") == 0 else f"失败（{result.get('returncode')}）"
            lines.append(f"**本次运行：** {status}，耗时 {result.get('elapsed_seconds', '-')} 秒。")
            if result.get("returncode") not in (0, None):
                lines.append("")
                lines.append("```text")
                lines.append((result.get("stderr") or result.get("stdout") or "")[-1200:])
                lines.append("```")
            lines.append("")

    lines.extend(
        [
            "## 六、高频追问与回答",
            "",
            "### Q1：这些数据是真实的吗？",
            "A：不是。选品/经营数据是固定种子模拟，竞品默认是公开快照；live 模式只抓公开页面，且遵守 robots。",
            "",
            "### Q2：CE 和 FCC 你能独立负责吗？",
            "A：我负责规则初筛、资料清单和风险分级；最终认证由实验室和持证机构完成，我不会把规则筛查说成认证结论。",
            "",
            "### Q3：ROI 与 ACOS 的关系？",
            "A：ACOS 只衡量广告花费/广告销售额；ROI 是净利润/总成本，包含 COGS、佣金、履约、广告、退款、仓储等。",
            "",
            "### Q4：库存周转天数怎么算？",
            "A：平均库存件数 ÷ 日均销量；同时看覆盖天数（含在途）和再订货点做补货决策。",
            "",
            "### Q5：系统能否接真实店铺后台？",
            "A：当前刻意不接。架构上采集、存储、报表都是适配器；接入真实 API 需要授权、密钥管理和合规评审。",
            "",
            "## 七、边界与风险控制",
            "",
            "- 公开数据/模拟数据，不冒充真实经营结果；",
            "- 不调用平台店铺 API，不使用验证码/代理绕过；",
            "- 合规结论需人工复核；",
            "- 所有失败写入 `outputs/logs/errors.log`，便于现场排查；",
            "- Streamlit 只做控制台，核心逻辑均可 CLI 独立运行。",
            "",
            "## 八、结束语",
            "",
            "> 这套系统展示的不是“会写几个脚本”，而是把**业务指标、合规约束、数据链路和工程化**",
            "> 组织成可演示、可复现、可扩展的运营系统。",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="interview_demo", description="生成面试演示脚本并可选执行全链路")
    parser.add_argument("--run", action="store_true", help="执行全链路（默认行为，保留给 UI/脚本显式调用）")
    parser.add_argument("--no-run", action="store_true", help="只生成讲稿，不执行模块")
    parser.add_argument("--quick", action="store_true", help="跳过基础 7 阶段流水线")
    parser.add_argument("--timeout", type=int, default=300, help="单个模块超时秒数")
    parser.add_argument("--output", default=str(OUTPUT_MD), help="Markdown 输出")
    args = parser.parse_args(list(argv) if argv is not None else None)

    utils.ensure_dir(OUTPUT_DIR)
    executed = not args.no_run
    run_id = f"interview_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    results: list[dict[str, Any]] = []
    steps = STEPS if args.quick else STEPS + [BASE_STEP]
    if executed:
        for step in steps:
            print(f"▶ {step['name']} ...")
            result = _run(step["command"], args.timeout)
            result["id"] = step["id"]
            result["name"] = step["name"]
            results.append(result)
            state = "✓" if result["returncode"] == 0 else "✗"
            print(f"  {state} {result['returncode']} ({result['elapsed_seconds']}s)")

    metrics = collect_metrics()
    markdown = generate_markdown(metrics, results, executed=executed, run_id=run_id)
    output = Path(args.output).expanduser().resolve()
    utils.ensure_dir(output.parent)
    utils.write_text(output, markdown)
    utils.write_json(
        OUTPUT_JSON,
        {
            "run_id": run_id,
            "generated_at": datetime.now(UTC).isoformat(),
            "executed": executed,
            "metrics": metrics,
            "results": results,
            "markdown": str(output),
        },
    )
    print("")
    print(f"✓ 面试演示脚本已生成：{output}")
    print(f"✓ 运行明细：{OUTPUT_JSON}")
    return 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "interview_demo"))
