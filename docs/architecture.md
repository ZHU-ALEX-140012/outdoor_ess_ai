# 架构说明

## 1. 设计目标

本项目是一个**离线优先、可审计、可扩展**的跨境电商运营自动化骨架，面向欧美市场的
轻量化户外储能品类。第一阶段只搭建基础框架与可运行的模拟全链路，不接入任何电商平台
店铺 API，不依赖真实卖家后台。

三条硬边界：

1. **数据边界**：所有商品、价格、趋势、竞品数据均为固定随机种子模拟，来源标记为
   `simulated-public-proxy`；不抓取个人信息，不绕过平台访问控制。
2. **AI 边界**：默认 `offline` 模式不发起任何模型请求；`live` 模式仅用于文案增强，
   模型不得改写结构化参数，不得编造认证、销量、评价。
3. **合规边界**：规则检查只做风险提示，不构成法律/认证意见；认证、标签、电池运输
   必须由持证服务商复核。

## 2. 分层与依赖方向

```
CLI / main.py
    ↓
pipelines/full_chain.py            # 只做编排，不写业务细节
    ↓
collectors → processing → analysis → listing → content → compliance → reporting
    ↓                                   ↓
integrations/llm_client          storage/repository
    ↓
config.py → utils.py               # 基础设施，被所有层依赖
```

依赖规则：

- 业务层可以依赖 `utils`、`config`，不得反向依赖 CLI；
- `pipelines` 可以依赖所有业务层；
- `integrations` 只负责外部能力适配，不包含业务规则；
- `utils.py` 不导入任何业务模块，避免循环依赖；
- 所有阶段输出 JSON 快照，便于替换为数据库/队列/对象存储。

## 3. 阶段与产物

| 阶段 | 模块 | 关键输入 | 关键产物 |
| --- | --- | --- | --- |
| 采集 | `collectors/mock_collector.py` | mock 商品/关键词/市场档案 | `data/raw/*.json` |
| 清洗 | `processing/normalizer.py` | 原始快照 | `data/processed/normalized.json`、`products.csv` |
| 分析 | `analysis/market_analyzer.py` | 标准表 | `outputs/analysis/market_analysis.json`、评分/机会 CSV |
| Listing | `listing/optimizer.py` | 机会列表 | `outputs/listings/*.json` |
| 内容 | `content/generator.py` | Listing | `outputs/content/*.json`、`*.md` |
| 合规 | `compliance/checker.py` | Listing + 规则配置 | `outputs/compliance/compliance_report.{json,md}` |
| 报告 | `reporting/report_builder.py` | 全阶段结果 + manifest | `outputs/reports/full_chain_report.md` |
| 运行清单 | `storage/repository.py` | 阶段状态 | `outputs/runs/<run_id>/manifest.json` |

## 4. 数据结构契约

### 4.1 商品市场记录

```json
{
  "market": "US",
  "sku": "NP-NOMAD-600",
  "name": "NorthPeak Nomad 600",
  "capacity_wh": 600,
  "output_w": 600,
  "weight_kg": 7.8,
  "price_usd": 499.0,
  "price_per_wh": 0.8317,
  "portability_score": 78.4,
  "compliance_required": ["UL 2743", "FCC", "UN38.3", "Prop 65"],
  "compliance_gaps": ["UL 2743", "Prop 65"],
  "compliance_ready": false
}
```

### 4.2 运行清单

```json
{
  "run_id": "run_20260401_120000_20260401",
  "status": "success",
  "stages": [
    {"name": "01_collect", "status": "success", "elapsed_ms": 12.3, "outputs": ["..."]}
  ],
  "summary": {"top_market": "US", "compliance_failed": 4}
}
```

## 5. 扩展点

| 需求 | 建议改动 |
| --- | --- |
| 接入真实公开数据 | 新增 collector 实现，复用同一输出契约；保留 source、collected_at、sha256 |
| 接入平台 API（未来） | 新增 `integrations/<platform>_client.py`，业务层不直接调用 SDK |
| 接入 DeepSeek 扩写 | 在 `listing` / `content` 注入 `DeepSeekClient`，输出必须过 compliance |
| 多语言 | 增加 locale 词典或翻译适配器，DE/FR 必须母语审校 |
| 数据仓库 | 用 `storage/repository.py` 的接口替换 JSON 实现 |
| 任务调度 | 在 CLI 外增加调度器，调用 `FullChainPipeline.run()` |

## 6. 失败与重试

- 每个阶段独立计时并写入 manifest；失败阶段记录错误，已完成阶段产物保留。
- 默认不自动重试业务阶段，避免重复写入；调度层可按 run_id 幂等重跑。
- LLM 客户端有指数退避与离线回退；密钥不会写入日志。
- 写文件使用临时文件 + `os.replace` 原子替换，避免半截 JSON。

## 7. 版本与兼容

- Python 3.11+，当前在 3.12 验证；
- 核心运行只依赖标准库 + PyYAML + python-dotenv；
- OpenAI SDK 仅在 live 模式惰性导入，离线模式即使未安装也能运行；
- 详细依赖见根目录 `requirements.txt`。

## 8. 外挂模块

项目在 7 阶段流水线之外提供两个独立模块：

| 模块 | 输入 | 输出 | 说明 |
| --- | --- | --- | --- |
| `product_research.py` | 公开页面/公开快照 | Excel/CSV/JSON | 100-500Wh 选品指标 |
| `listing_generator.py` | 选品表 | Amazon CSV/文案/校验 | 多市场 Listing 与字段 profile |
| `competitor_monitor.py` | 公开竞品商品页/公开快照 | 快照/预警 TXT/痛点报告 | 定时巡检与差评分析 |
| `compliance_check.py` | 选品表 + 合规主数据 | 合规 Excel/JSON | CE/FCC 规则初筛 |
| `report_generator.py` | 选品表 | 广告/库存/利润 Excel | 模拟经营指标与 ROI/周转 |

五者都不依赖主流水线的运行状态，可单独执行；`listing_generator.py` 的字段顺序
以 `config/amazon_listing_profile.yaml` 为准，`competitor_monitor.py` 的巡检频率
以 `config/competitor_monitor.yaml` 或 `--interval-hours` 为准。

