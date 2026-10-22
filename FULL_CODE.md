# 欧美轻量化户外储能全链路 AI 自动化系统 · 全量源码

> 本文件由 `python scripts/export_bundle.py` 自动生成。
> 所有代码均为离线模拟版，不接入任何电商平台真实店铺 API。

- 项目根目录：`C:\Users\36494\Desktop\outdoor_ess_ai`
- 文件数量：82

## 文件索引

- `README.md`
- `requirements.txt`
- `main.py`
- `utils.py`
- `pyproject.toml`
- `.env.example`
- `start.ps1`
- `start.sh`
- `ess_ai/__init__.py`
- `ess_ai/analysis/__init__.py`
- `ess_ai/collectors/__init__.py`
- `ess_ai/compliance/__init__.py`
- `ess_ai/content/__init__.py`
- `ess_ai/integrations/__init__.py`
- `ess_ai/listing/__init__.py`
- `ess_ai/pipelines/__init__.py`
- `ess_ai/processing/__init__.py`
- `ess_ai/reporting/__init__.py`
- `ess_ai/storage/__init__.py`
- `.streamlit/config.toml`
- `app.py`
- `competitor_monitor.py`
- `compliance_check.py`
- `config/amazon_listing_profile.yaml`
- `config/competitor_monitor.yaml`
- `config/compliance_rules.yaml`
- `config/data_sources.yaml`
- `config/listing_copy_rules.yaml`
- `config/model_profiles.yaml`
- `config/product_research.yaml`
- `config/report_generator.yaml`
- `config/settings.yaml`
- `data/competitors/competitors.json`
- `data/competitors/state.json`
- `data/mock/competitor_public_snapshots.json`
- `data/mock/competitor_public_snapshots_changed.json`
- `data/mock/keywords.json`
- `data/mock/market_profiles.json`
- `data/mock/product_catalog.json`
- `data/mock/product_compliance_master.json`
- `data/mock/public_research_snapshot.json`
- `docs/amazon_listing.md`
- `docs/architecture.md`
- `docs/competitor_monitor.md`
- `docs/compliance_check.md`
- `docs/final_integration.md`
- `docs/operations_reports.md`
- `docs/product_research.md`
- `error_guard.py`
- `ess_ai/__main__.py`
- `ess_ai/analysis/market_analyzer.py`
- `ess_ai/cli.py`
- `ess_ai/collectors/mock_collector.py`
- `ess_ai/compliance/checker.py`
- `ess_ai/config.py`
- `ess_ai/content/generator.py`
- `ess_ai/integrations/llm_client.py`
- `ess_ai/listing/optimizer.py`
- `ess_ai/pipelines/full_chain.py`
- `ess_ai/processing/normalizer.py`
- `ess_ai/reporting/report_builder.py`
- `ess_ai/storage/repository.py`
- `interview_demo.py`
- `listing_generator.py`
- `product_research.py`
- `prompts/compliance_review.md`
- `prompts/listing_system.md`
- `report_generator.py`
- `scripts/check_syntax.py`
- `scripts/export_bundle.py`
- `start_all.ps1`
- `start_all.sh`
- `stop_all.ps1`
- `stop_all.sh`
- `tests/conftest.py`
- `tests/test_competitor_monitor.py`
- `tests/test_final_integration.py`
- `tests/test_listing_generator.py`
- `tests/test_operations_reports.py`
- `tests/test_pipeline.py`
- `tests/test_product_research.py`
- `tests/test_utils.py`

---

## `README.md`

````markdown
# 欧美轻量化户外储能全链路 AI 自动化系统

面向美国、德国、英国、法国市场的轻量化户外储能（便携电站 / 折叠太阳能板）运营自动化
基础框架，覆盖 **市场洞察 → 选品评分 → Listing 生成 → 内容生产 → 合规初筛 → 运营报告**
全链路。

> **当前阶段：v0.1.0 基础框架。**
> 不接入任何电商平台真实店铺 API，不登录卖家后台，不抓取个人信息。
> 所有商品、价格、趋势与竞品数据均为**固定随机种子模拟**，仅用于流程演示。
> DeepSeek V4.1-Flash 已接入配置与客户端，默认离线运行，不产生模型费用。

---

## 1. 核心能力

| 能力 | 说明 |
| --- | --- |
| 离线可跑 | 无密钥、无网络也能完成全链路演示，适合 CI / 本地验证 |
| 数据可追溯 | 固定 seed、来源字段、采集时间、文件 SHA-256、阶段 manifest |
| 可解释评分 | 市场 5 维评分、商品机会 5 维评分，权重全部配置化 |
| 合规优先 | 禁用词、必填披露、认证缺口、未经验证认证声明检查 |
| 多市场 | US / DE / UK / FR，含本地币种、VAT、合规复杂度 |
| 公开选品 | `product_research.py`：100-500Wh 公开数据清洗、毛利/容量/竞争度、Excel 高潜表 |
| 上架素材 | `listing_generator.py`：多市场文案、违禁词筛查、Amazon 平铺文件 CSV |
| 竞品监控 | `competitor_monitor.py`：公开价格/BSR/差评、6 小时巡检、TXT 预警、痛点报告 |
| 合规校验 | `compliance_check.py`：CE/FCC 风险评分、不符合项、修改建议 |
| 经营报表 | `report_generator.py`：广告日报、库存预警、月度利润、ROI、周转天数 |
| 可替换 | 采集、存储、LLM、报告均为适配器/模块，可按层替换 |

### 明确不做

- 不调用 Amazon / TikTok Shop / Shopify / eBay 等平台店铺 API；
- 不伪造真实销量、评价、认证证书或品牌授权；
- 不生成绝对化安全承诺、医疗功效或“100% 无限续航”等表述；
- 不替代律师、认证机构、报关行或持证合规服务商。

---

## 2. 目录结构（每个文件夹的用途）

```text
outdoor_ess_ai/
├── main.py                     # 一键入口：python main.py <command>
├── product_research.py         # ★ 独立选品模块：公开数据 → 清洗 → 指标 → Excel
├── listing_generator.py        # ★ 上架素材模块：选品表 → 多语言文案 → Amazon CSV
├── competitor_monitor.py       # ★ 竞品监控：公开价格/BSR/差评、预警与痛点报告
├── compliance_check.py         # ★ 合规筛查：CE/FCC 风险、不符合项与修改建议
├── report_generator.py         # ★ 经营报表：广告日报/库存预警/月度利润
├── app.py                      # ★ Streamlit 一体化控制台（Tundra 左导航 + 一键运行）
├── error_guard.py              # ★ 全局异常捕获与错误日志
├── interview_demo.py           # ★ 面试演示脚本（JD 能力点 + 讲稿）
├── utils.py                    # ★ 全局公共工具：文件读写、JSON/YAML/CSV、日志、哈希
├── requirements.txt            # 稳定版依赖清单（逐条备注功能）
├── pyproject.toml              # 打包元数据 + pytest / ruff / mypy 配置
├── start.ps1                   # 旧版演示脚本（建 venv → 装依赖 → 跑 demo）
├── start_all.ps1               # ★ 全链路一键启动（Streamlit + 健康检查 + 浏览器）
├── stop_all.ps1                # 停止 Streamlit
├── start_all.sh / stop_all.sh  # macOS / Linux 版本
├── .streamlit/config.toml      # 本地 Streamlit 配置（关闭 developmentMode）
├── .env.example                # 环境变量模板（不含真实密钥）
├── README.md
│
├── config/                     # 配置层：所有可调参数集中管理
│   ├── settings.yaml           # 主配置：市场、路径、评分权重、Listing 限额、合规规则
│   ├── data_sources.yaml       # 公开数据源口径、字段映射、采集边界
│   ├── model_profiles.yaml     # DeepSeek V4.1-Flash 运行档案与防护规则
│   ├── product_research.yaml   # 选品模块：平台、成本、筛选、评分、输出参数
│   ├── amazon_listing_profile.yaml  # Amazon 平铺文件字段档案（可替换为类目模板）
│   ├── listing_copy_rules.yaml # Listing 违禁词与替换规则
│   ├── competitor_monitor.yaml # 竞品监控：频率、阈值、痛点分类、演示竞品
│   ├── compliance_rules.yaml   # CE/FCC 标准、风险权重、电压/电池阈值
│   └── report_generator.yaml   # 经营模拟：周期、种子、广告/库存/成本假设
│
├── data/                       # 数据层：模拟/原始/清洗后数据，全部本地文件
│   ├── mock/                   # 人工构造的演示商品目录、关键词、市场档案
│   ├── raw/                    # 采集层原始快照（运行时生成）
│   ├── processed/              # 标准化后的分析表与 CSV（运行时生成）
│   └── external/               # 预留：人工下载的公开报告/标准摘要
│
├── docs/                       # 文档层：架构、数据契约、扩展点
│   ├── architecture.md
│   ├── product_research.md     # 选品模块运行说明与可调参数
│   ├── amazon_listing.md       # 上架素材模块、CSV 字段与导入校验说明
│   ├── competitor_monitor.md   # 竞品监控、6 小时调度、预警与痛点报告说明
│   ├── compliance_check.md     # CE/FCC 合规规则、评分与不符合项说明
│   ├── operations_reports.md   # 广告/库存/利润报表与 ROI/周转公式
│   └── final_integration.md    # Streamlit、一键启动、错误日志与面试演示
│
├── ess_ai/                     # 业务代码包
│   ├── cli.py                  # 命令行：init / demo / check / status
│   ├── config.py               # 配置加载、环境变量覆盖、路径解析、校验
│   ├── collectors/             # 采集层：公开数据口径的离线模拟采集器
│   ├── processing/             # 清洗层：币种、单位、合规缺口、派生指标
│   ├── analysis/               # 分析层：市场评分、选品机会、进入策略
│   ├── listing/                # Listing 层：标题 / 五点 / 描述 / 搜索词
│   ├── content/                # 内容层：短视频脚本、社媒文案、博客提纲
│   ├── compliance/             # 合规层：禁用词、披露项、认证缺口规则初筛
│   ├── reporting/              # 报告层：Markdown 全链路报告 + JSON 摘要
│   ├── pipelines/              # 编排层：7 阶段流水线 + manifest
│   ├── integrations/           # 集成层：DeepSeek OpenAI-compatible 客户端
│   └── storage/                # 存储层：JSON 快照与运行清单
│
├── outputs/                    # 运行产物（可删除后重建）
│   ├── analysis/               # 市场评分、机会表
│   ├── reports/                # 全链路 Markdown 报告、摘要 JSON
│   ├── content/                # 内容资产包（JSON + Markdown）
│   ├── listings/               # 每个 SKU×市场的 Listing JSON
│   ├── compliance/             # 合规初筛 + CE/FCC 合规校验
│   ├── runs/                   # 每次运行的 manifest（阶段耗时/状态/产物）
│   ├── logs/                   # 滚动运行日志
│   ├── research/               # 选品模块：Excel/CSV/JSON/日志
│   ├── listing/                # 上架素材：Amazon CSV/文案/校验 JSON/日志
│   ├── monitor/                # 竞品监控：快照/预警 TXT/痛点报告/日志
│   └── operations/             # 经营报表：广告日报/库存预警/月度利润
│
├── prompts/                    # 提示词层：Listing 与合规复核模板（live 模式备用）
├── scripts/                    # 运维脚本：全量语法/结构校验、源码单文件导出
│   ├── check_syntax.py
│   └── export_bundle.py
├── tests/                      # 测试层：工具单元测试 + 全链路冒烟测试
└── FULL_CODE.md                # 全量源码单文件（由 export_bundle.py 生成，便于复制）
```

---

## 3. 一键启动

### Windows（推荐）

在项目根目录打开 PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File .\start_all.ps1
```

脚本会自动：

1. 检测/创建 `.venv`，安装 `requirements.txt`；
2. 初始化目录与日志；
3. 启动 Streamlit（默认 `127.0.0.1:8501`）；
4. 健康检查通过后自动打开浏览器。

首次启动可能需要 1-3 分钟安装依赖，之后几秒内打开。

```powershell
# 换端口 / 不打开浏览器 / 跳过安装
powershell -ExecutionPolicy Bypass -File .\start_all.ps1 -Port 8502 -NoBrowser
powershell -ExecutionPolicy Bypass -File .\start_all.ps1 -SkipInstall

# 停止
powershell -ExecutionPolicy Bypass -File .\stop_all.ps1
```

`start.ps1` 保留为兼容别名，实际也会启动 Streamlit 控制台。

### macOS / Linux

```bash
chmod +x start_all.sh stop_all.sh
./start_all.sh
./stop_all.sh
```

### 手动启动（任意系统）

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py init
streamlit run app.py
```

> 只需要 Python 3.11+。所有可视化操作都在 Streamlit 页面内完成，不需要再手动执行
> 选品/Listing/竞品/合规/报表的零散 Python 命令。
> CLI 仍保留，适合自动化和排障。

### 页面入口

```text
http://127.0.0.1:8501
```

Streamlit 左侧 7 个模块：总览、选品研究、上架素材、竞品监控、合规校验、经营报表、面试演示。
每个模块右上角有一键动作，结果可在线预览并下载 Excel。

### 常用产物

- 全链路报告：`outputs/reports/full_chain_report.md`
- 选品 Excel：`outputs/research/high_potential_products.xlsx`
- Listing CSV：`outputs/listing/amazon_us_listings.csv`
- 合规 Excel：`outputs/compliance/compliance_check.xlsx`
- 经营报表：`outputs/operations/monthly_profit.xlsx`
- 面试讲稿：`outputs/interview/interview_demo.md`
- 错误日志：`outputs/logs/errors.log`
- 运行清单：`outputs/runs/<run_id>/manifest.json`

---

## 4. 常用命令

```bash
python main.py init       # 初始化目录与日志
python main.py status     # 查看模式、模型、市场、API Key 是否配置
python main.py demo       # 运行全链路（默认 4 个市场）
python main.py demo --seed 42 --markets US,DE
python main.py check      # 校验所有 Python/YAML/JSON 语法与目录结构
pytest -q                 # 单元测试 + 全链路冒烟测试
```

指定其他配置：

```bash
python main.py --config config/settings.yaml status
```

---

## 5. 配置与 DeepSeek V4.1-Flash

### 5.1 默认离线

`config/settings.yaml` 中：

```yaml
project:
  mode: "offline"
llm:
  model: "deepseek-v4.1-flash"
  offline_fallback: true
  enable_in_demo: false
```

离线模式不会发起网络请求。`ess_ai/integrations/llm_client.py` 只有在：

1. `project.mode=live`；
2. 环境变量中存在 `DEEPSEEK_API_KEY`；

两个条件同时满足时才会调用 OpenAI-compatible 接口。

### 5.2 启用 live（可选）

```bash
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY，并把 ESS_AI_MODE 改为 live
```

```dotenv
DEEPSEEK_API_KEY=sk-...your-key...
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
ESS_AI_MODE=live
ESS_AI_MODEL=deepseek-v4.1-flash
```

> 当前基础流水线默认不把 LLM 接入 Listing/内容，以保证结果可复现。
> 接入方式见 `docs/architecture.md` 的扩展点；任何模型输出都必须先过合规检查。

### 5.3 数据边界

- 商品/价格/趋势/竞品：`data/mock/` + 固定 seed 模拟；
- 来源字段统一标记 `*/simulated`；
- 不包含真实卖家、个人信息、平台后台数据；
- 真实公开数据接入时，必须补充来源 URL、采集时间、快照哈希与 robots 合规记录。

---

## 6. 流水线

```text
01_collect → 02_normalize → 03_analyze → 04_listing
           → 05_content  → 06_compliance → 07_report
```

每个阶段：

- 独立计时；
- 成功/失败写入 `outputs/runs/<run_id>/manifest.json`；
- 文件写入采用“临时文件 + 原子替换”；
- 失败时保留已完成阶段产物，便于定位与重跑。

评分模型：

```text
市场综合 = 需求 30% + 竞争 20% + 毛利 25% + 合规 10% + 物流 15%
商品机会 = 需求 30% + 价格匹配 20% + 便携性 20% + 合规 15% + 毛利 15%
```

权重可在 `config/settings.yaml` 的 `business.scoring_weights` 中调整。

---

## 7. 公共工具模块 `utils.py`

`utils.py` 是唯一的基础设施入口，被所有层引用，覆盖：

| 分组 | 函数 |
| --- | --- |
| 路径/时间 | `ensure_dir`、`safe_filename`、`utc_now`、`timestamp`、`timer` |
| 文本 | `read_text`、`write_text`、`atomic_write_text` |
| 结构化数据 | `read_json`、`write_json`、`read_jsonl`、`write_jsonl`、`read_yaml`、`write_yaml`、`read_csv`、`write_csv`、`load_any`、`save_any` |
| 哈希/工具 | `file_sha256`、`human_size`、`deep_get`、`deep_merge`、`chunked` |
| 日志 | `setup_logging`、`get_logger` |

日志默认输出到控制台和 `outputs/logs/outdoor_ess_ai.log`，按 5 MB 滚动，保留 5 份。

---

## 8. 校验与测试

```bash
python main.py check
```

该命令执行：

- 所有 `.py` 的 AST 解析 + `compile`；
- 所有 `.yaml` / `.json` / `.jsonl` 解析；
- 必需文件、目录、包初始化文件检查。

测试：

```bash
pytest -q
```

覆盖：

- 文本 / JSON / JSONL / YAML / CSV 读写与默认值；
- 日志文件落盘；
- 深层次配置读取与合并；
- 采集确定性；
- 全链路 7 阶段 manifest；
- 合规禁用词拦截。

---

## 9. 合规声明

本项目的合规检查是**规则初筛**，不是法律意见、认证结论或平台审核结果。正式投放前必须：

1. 由持证合规服务商确认目标市场认证范围与证书型号覆盖；
2. 核对锂电池运输、标签、包装与报关要求；
3. 核对价格含税/不含税、VAT、WEEE/电池注册义务；
4. 由母语运营审校 DE/FR 文案；
5. 保留所有来源、快照与人工复核记录。

---

## 10. 下一步路线

- [ ] 接入真实公开数据的人工导入器（CSV/JSON），保留来源与哈希；
- [ ] 增加供应商报价与 landed cost 模型；
- [ ] 增加广告投放模拟（ACOS / CPC / 预算分配）；
- [ ] 增加 listing A/B 版本与多语言审校工作流；
- [ ] 增加 SQLite/Postgres 存储适配器；
- [ ] 增加任务调度与失败重跑。

架构细节与扩展方式见 [docs/architecture.md](docs/architecture.md)。

---

## 11. 全量源码单文件

项目根目录的 `FULL_CODE.md` 已按“文件路径 + 完整源码”导出全部源码/配置/测试文件，
可直接搜索、复制或交给其他工具审阅。修改代码后可重新生成：

```bash
python scripts/export_bundle.py
```

生成逻辑只包含源码、配置、文档与 mock 数据，不包含 `outputs/`、日志、缓存与密钥。

---

## 12. 选品自动化独立模块

`product_research.py` 是独立的 100-500Wh 户外露营轻量化储能选品模块：

- 公开数据：Amazon / AliExpress / 1688 公开搜索页或本地公开快照；
- 清洗：容量、重量、功率、价格、评分、去重、异常值、关键词排除；
- 指标：单 SKU 毛利、市场容量、竞争度、综合机会分；
- 输出：带格式、筛选、指标说明、参数快照、数据质量的 Excel；
- 默认 `offline`，无网络即可复现；`live` 模式遵守 robots.txt 与限速，不绕过验证码。

```bash
python product_research.py
python product_research.py --min-margin 30 --top-n 15
python product_research.py --mode live --limit 20
```

输出：

```text
outputs/research/
├── high_potential_products.xlsx
├── cleaned_products.csv
├── raw_public_snapshot.json
├── research_summary.json
└── product_research.log
```

完整参数、指标公式、live 模式限制与常见问题见
[docs/product_research.md](docs/product_research.md)。

---

## 13. 上架素材自动化模块

`listing_generator.py` 读取第二步高潜力选品表，生成 Amazon 平铺文件与多市场文案：

- 默认美国站英文，可选 `en-US / en-GB / de-DE / fr-FR`；
- 合规标题、5 点核心描述、完整详情页 HTML、搜索词、安全/使用/法律字段；
- 60 列 US/UK、65 列 DE/FR 的 Amazon CSV（字段档案可替换为 Seller Central 模板）；
- 内置绝对化、认证、安全、环保、医疗、价格类违禁词扫描与保守替换；
- 输出逐站点的 `content.json`、`validation.json` 与汇总 `listing_summary.json`。

```bash
python listing_generator.py
python listing_generator.py --locales all
python listing_generator.py --locales en-US --gtin-map data/gtin_map.csv \
  --image-base-url https://cdn.example.com/power --browse-node 123456
```

输出：

```text
outputs/listing/
├── amazon_us_listings.csv
├── en-US_content.json
├── en-US_validation.json
└── listing_summary.json
```

CSV 格式校验通过不代表账号级资料齐全：主图、GTIN、Browse Node、EU GPSR 等字段
不会被伪造，未提供时会在 validation 中列为 blocker。完整说明见
[docs/amazon_listing.md](docs/amazon_listing.md)。

---

## 14. 竞品监控自动化模块

`competitor_monitor.py` 独立监控竞品公开商品页：

- 自定义添加 Amazon / AliExpress / 1688 / Generic 商品链接；
- 默认每 6 小时巡检，`--interval-hours` 可独立调整；
- 抓取公开价格、BSR/公开排名、公开差评；
- 价格或排名超过阈值时生成本地 TXT 预警；
- 从差评自动提取高频痛点，分类输出 Markdown/JSON 报告；
- 单个链接 404/403/验证码/结构变化时跳过，不中断其他竞品；
- 首次巡检只建立基线，第二次异动才预警。

```bash
python competitor_monitor.py list
python competitor_monitor.py add "https://www.amazon.com/dp/B0XXXXXXXX" --name "竞品 A"
python competitor_monitor.py run
python competitor_monitor.py schedule --interval-hours 6
```

输出：

```text
outputs/monitor/
├── snapshots/                  # 每次巡检快照
├── alerts/                     # 单条 TXT + latest_alerts.txt
├── reports/                    # 痛点 Markdown/JSON + monitor_summary.json
└── logs/
```

完整说明见 [docs/competitor_monitor.md](docs/competitor_monitor.md)。

---

## 15. 合规校验模块

`compliance_check.py` 对 9 个模拟 SKU 做 CE/FCC 规则初筛：

- 欧盟：LVD、EMC、RoHS、WEEE、Battery Regulation、GPSR、RED（无线）；
- 美国：FCC Part 15B/15C、SDoC、FCC ID、UL 2743、Prop 65；
- 通用：UN38.3、IATA >100Wh 运输提示、IP 等级、额定功率一致性；
- 输出每 SKU 的风险分、PASS/CONDITIONAL/FAIL、美国/欧盟状态；
- 不符合项带标准、观察值、修改建议和需要的证据。

```bash
python compliance_check.py
```

输出：

```text
outputs/compliance/
├── compliance_check.xlsx      # 汇总 / 不符合项 / 产品参数 / 标准依据
└── compliance_summary.json
```

完整说明见 [docs/compliance_check.md](docs/compliance_check.md)。

---

## 16. 经营报表自动化模块

`report_generator.py` 使用固定种子模拟经营数据，生成：

- 广告投放日报：展示、点击、CTR、CPC、花费、订单、CVR、ACOS、ROAS、广告贡献毛利；
- 库存预警表：覆盖天数、再订货点、建议补货、库存金额、库龄、周转天数；
- 月度利润核算表：收入、COGS、佣金、履约、广告、退款、仓储、净利润、ROI；
- 每个 SKU 的 ROI 与库存周转天数；
- 经营概览与指标公式说明。

```bash
python report_generator.py
```

输出：

```text
outputs/operations/
├── ad_daily_report.xlsx
├── inventory_alert.xlsx
├── monthly_profit.xlsx
└── report_summary.json
```

完整公式与假设见 [docs/operations_reports.md](docs/operations_reports.md)。

---

## 17. 最终整合：Streamlit 控制台与一键启动

### 17.1 一键启动

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File .\start_all.ps1

# 停止
powershell -ExecutionPolicy Bypass -File .\stop_all.ps1
```

```bash
# macOS / Linux
./start_all.sh
./stop_all.sh
```

启动脚本会检测/创建 `.venv`、安装依赖、执行 `main.py init`、启动 Streamlit、
等待健康检查，并自动打开 `http://127.0.0.1:8501`。

### 17.2 Streamlit 页面

界面采用 **Tundra / 苔原账本（A+C）** 视觉：左侧 232px 导航栏、
苔绿 + 墨色低饱和体系、业务流条、行动队列、右侧深色运行日志抽屉。

7 个模块：

1. 总览（运行全链路）
2. 选品研究（运行选品）
3. 上架素材（生成 Listing）
4. 竞品监控（巡检竞品）
5. 合规校验（合规筛查）
6. 经营报表（生成报表）
7. 面试演示（生成 JD 映射讲稿）

每个模块通过左侧导航进入，右上角一个主操作按钮执行对应子进程；
失败写入 `outputs/logs/errors.log`，运行记录写入 `outputs/logs/ui_commands.log`。

### 17.3 全局异常捕获

`error_guard.py` 已接入所有 CLI 入口和 Streamlit 页面：

- `sys.excepthook` + `threading.excepthook`；
- `errors.log`（人类可读）+ `errors.jsonl`（结构化）；
- 子进程失败记录命令、退出码、stdout/stderr 尾部；
- 不覆盖原始异常，不吞错。

### 17.4 面试演示

```bash
python interview_demo.py            # 执行全部模块并生成讲稿
python interview_demo.py --no-run   # 只生成讲稿
```

输出：

```text
outputs/interview/interview_demo.md
outputs/interview/interview_demo.json
```

讲稿包含 30 秒定位、架构、5 分钟演示顺序、每个模块的 JD 能力点、讲解话术、
追问准备和指标看板。

完整运行说明见 [docs/final_integration.md](docs/final_integration.md)。
````

## `requirements.txt`

````
# =============================================================================
# 欧美轻量化户外储能全链路 AI 自动化系统
# Python 3.11+ / 3.12 验证通过
#
# 版本策略：锁定主版本区间，避免破坏性升级；生产环境建议再生成 lock 文件。
# 安装：python -m pip install -r requirements.txt
# =============================================================================

# -----------------------------------------------------------------------------
# 核心运行依赖（离线演示必需）
# -----------------------------------------------------------------------------
PyYAML>=6.0.1,<7.0            # YAML 配置、数据源目录、模型档案的解析与写入
python-dotenv>=1.0.1,<2.0     # 加载 .env 中的 DEEPSEEK_API_KEY 等环境变量

# -----------------------------------------------------------------------------
# 大模型增强（仅 project.mode=live 时使用；离线模式自动回退）
# -----------------------------------------------------------------------------
openai>=1.55.0,<4.0            # DeepSeek V4.1-Flash 的 OpenAI-compatible 聊天补全 SDK
httpx>=0.27.0,<1.0             # OpenAI SDK 的 HTTP 传输层；显式锁定超时/代理兼容版本

# -----------------------------------------------------------------------------
# 选品研究模块（公开页面抓取 + Excel 输出）
# -----------------------------------------------------------------------------
requests>=2.31.0,<3.0          # 公开搜索页 HTML 请求；遵守 robots.txt 与限速
beautifulsoup4>=4.12.0,<5.0    # 公开页面 HTML 解析（Amazon/AliExpress/1688 适配器）
openpyxl>=3.1.0,<4.0           # 生成结构化、带格式和多工作表的 Excel 选品表

# -----------------------------------------------------------------------------
# 可视化控制台与全链路启动
# -----------------------------------------------------------------------------
streamlit>=1.50.0,<2.0        # 本地可视化控制台：一键运行各模块、查看报表、下载 Excel
pandas>=2.2.0,<4.0             # Streamlit 数据表渲染、批量 CSV 分析与真实数据探索

# -----------------------------------------------------------------------------
# 测试与代码质量（开发/CI 使用，不影响离线运行）
# -----------------------------------------------------------------------------
pytest>=8.0,<10.0              # 单元测试与全链路冒烟测试
pytest-cov>=5.0,<8.0           # 覆盖率统计
ruff>=0.6.0,<1.0               # 快速 lint / import 排序 / 格式化检查
mypy>=1.10.0,<2.0              # 静态类型检查（可选，pipeline 可逐步补齐注解）
````

## `main.py`

````python
#!/usr/bin/env python3
"""项目一键入口：python main.py <command>。"""

from __future__ import annotations

import sys
from pathlib import Path

# 允许从项目根目录直接运行，无需先安装为包。
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from error_guard import run_cli  # noqa: E402
from ess_ai.cli import main  # noqa: E402  (路径注入后再导入)

if __name__ == "__main__":
    raise SystemExit(run_cli(main, "main"))
````

## `utils.py`

````python
"""全局通用工具模块（项目唯一基础设施入口）。

本模块只依赖 Python 标准库，``PyYAML`` 仅在调用 YAML 读写函数时惰性导入。
因此它可以被任意业务层、脚本或测试直接复用，而不会引入循环依赖。

覆盖能力：
    1. 路径与文件名处理；
    2. 文本 / JSON / JSONL / YAML / CSV 的原子读写；
    3. 日志初始化（控制台 + 滚动文件）；
    4. 哈希、分块、深层次配置读取等小型通用函数。

设计原则：
    - 任何写操作先写临时文件，再通过 ``os.replace`` 原子替换；
    - 所有路径默认相对当前工作目录解析，调用方可传入绝对路径；
    - 日志 API 幂等，重复调用 ``setup_logging`` 不会重复挂载 handler。
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
import re
import tempfile
import time
from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

__all__ = [
    "APP_LOGGER_NAME",
    "DEFAULT_ENCODING",
    "FileIOError",
    "UtilError",
    "atomic_write_text",
    "chunked",
    "deep_get",
    "deep_merge",
    "ensure_dir",
    "file_sha256",
    "get_logger",
    "human_size",
    "load_any",
    "read_csv",
    "read_json",
    "read_jsonl",
    "read_text",
    "read_yaml",
    "safe_filename",
    "save_any",
    "setup_logging",
    "timer",
    "timestamp",
    "utc_now",
    "utc_now_iso",
    "write_csv",
    "write_json",
    "write_jsonl",
    "write_text",
    "write_yaml",
]

DEFAULT_ENCODING = "utf-8"
APP_LOGGER_NAME = "outdoor_ess_ai"
_MISSING = object()
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_CONFIGURED = False


class UtilError(RuntimeError):
    """通用工具异常基类。"""


class FileIOError(UtilError):
    """文件读取、解析或写入失败。"""


# ---------------------------------------------------------------------------
# 路径与时间
# ---------------------------------------------------------------------------
def ensure_dir(path: str | os.PathLike[str]) -> Path:
    """确保目录存在并返回其绝对 ``Path``。"""

    target = Path(path).expanduser().resolve()
    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError as exc:  # pragma: no cover - 依赖操作系统错误
        raise FileIOError(f"无法创建目录: {target}") from exc
    return target


def safe_filename(name: str, *, default: str = "untitled", max_length: int = 120) -> str:
    """把任意字符串转为安全的跨平台文件名（不含路径分隔符）。"""

    cleaned = re.sub(r"[^\w.\-]+", "_", str(name), flags=re.UNICODE).strip(" ._-")
    cleaned = re.sub(r"_{2,}", "_", cleaned)
    if not cleaned:
        cleaned = default
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip(" ._-")
    return cleaned or default


def utc_now() -> datetime:
    """返回带 UTC 时区的当前时间。"""

    return datetime.now(UTC)


def timestamp(fmt: str = "%Y%m%d_%H%M%S", *, dt: datetime | None = None) -> str:
    """返回 UTC 时间戳字符串，默认适合拼接到文件名。"""

    return (dt or utc_now()).strftime(fmt)


def utc_now_iso() -> str:
    """返回 ISO-8601 UTC 时间字符串（秒级）。"""

    return utc_now().replace(microsecond=0).isoformat()


@contextmanager
def timer() -> Iterator[dict[str, float]]:
    """计时上下文，用法：``with timer() as t: ...; t['elapsed_ms']``。"""

    result: dict[str, float] = {}
    started = time.perf_counter()
    try:
        yield result
    finally:
        result["elapsed_ms"] = round((time.perf_counter() - started) * 1000, 2)


# ---------------------------------------------------------------------------
# 文本读写
# ---------------------------------------------------------------------------
def atomic_write_text(
    path: str | os.PathLike[str],
    content: str,
    *,
    encoding: str = DEFAULT_ENCODING,
) -> Path:
    """原子写入文本：写同目录临时文件后 ``os.replace``，避免半截文件。"""

    target = Path(path).expanduser().resolve()
    ensure_dir(target.parent)
    tmp_name: str | None = None
    try:
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
        )
        with os.fdopen(fd, "w", encoding=encoding, newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target)
        tmp_name = None
        return target
    except (OSError, UnicodeError) as exc:
        raise FileIOError(f"原子写入失败: {target}") from exc
    finally:
        if tmp_name and Path(tmp_name).exists():
            try:
                Path(tmp_name).unlink()
            except OSError:  # pragma: no cover - 清理失败不覆盖原异常
                pass


def write_text(
    path: str | os.PathLike[str],
    content: str,
    *,
    encoding: str = DEFAULT_ENCODING,
    append: bool = False,
) -> Path:
    """写入文本；``append=True`` 时追加，否则原子覆盖。"""

    if append:
        target = Path(path).expanduser().resolve()
        ensure_dir(target.parent)
        try:
            with target.open("a", encoding=encoding, newline="") as handle:
                handle.write(content)
        except (OSError, UnicodeError) as exc:
            raise FileIOError(f"追加文本失败: {target}") from exc
        return target
    return atomic_write_text(path, content, encoding=encoding)


def read_text(
    path: str | os.PathLike[str],
    *,
    encoding: str = DEFAULT_ENCODING,
    default: Any = _MISSING,
) -> str:
    """读取文本；文件不存在且提供 ``default`` 时返回默认值。"""

    target = Path(path).expanduser().resolve()
    try:
        return target.read_text(encoding=encoding)
    except FileNotFoundError as exc:
        if default is not _MISSING:
            return default
        raise FileIOError(f"文件不存在: {target}") from exc
    except (OSError, UnicodeError) as exc:
        raise FileIOError(f"读取文本失败: {target}") from exc


# ---------------------------------------------------------------------------
# JSON / JSONL / YAML / CSV
# ---------------------------------------------------------------------------
def write_json(
    path: str | os.PathLike[str],
    data: Any,
    *,
    indent: int = 2,
    ensure_ascii: bool = False,
) -> Path:
    """将对象序列化为 JSON 并原子写入。"""

    try:
        payload = json.dumps(data, ensure_ascii=ensure_ascii, indent=indent, default=str)
    except (TypeError, ValueError) as exc:
        raise FileIOError(f"JSON 序列化失败: {path}") from exc
    return atomic_write_text(path, payload + "\n")


def read_json(path: str | os.PathLike[str], default: Any = _MISSING) -> Any:
    """读取 JSON；解析失败抛出 ``FileIOError``，缺失时按需返回默认值。"""

    target = Path(path).expanduser().resolve()
    if not target.exists() and default is not _MISSING:
        return default
    try:
        return json.loads(target.read_text(encoding=DEFAULT_ENCODING))
    except FileNotFoundError as exc:
        raise FileIOError(f"JSON 文件不存在: {target}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FileIOError(f"读取或解析 JSON 失败: {target}") from exc


def write_jsonl(path: str | os.PathLike[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    """将可迭代映射写成 JSON Lines（UTF-8，一行一个对象）。"""

    lines: list[str] = []
    for index, row in enumerate(rows, start=1):
        try:
            lines.append(json.dumps(dict(row), ensure_ascii=False, default=str))
        except (TypeError, ValueError) as exc:
            raise FileIOError(f"JSONL 第 {index} 行序列化失败: {path}") from exc
    return atomic_write_text(path, "\n".join(lines) + ("\n" if lines else ""))


def read_jsonl(path: str | os.PathLike[str], default: Any = _MISSING) -> list[dict[str, Any]]:
    """读取 JSON Lines，忽略空行；任一行损坏即报错并给出行号。"""

    target = Path(path).expanduser().resolve()
    if not target.exists() and default is not _MISSING:
        return default
    rows: list[dict[str, Any]] = []
    line_no = 0
    try:
        with target.open("r", encoding=DEFAULT_ENCODING) as handle:
            for line in handle:
                line_no += 1
                line = line.strip()
                if not line:
                    continue
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError("每行必须是 JSON 对象")
                rows.append(value)
        return rows
    except FileNotFoundError as exc:
        raise FileIOError(f"JSONL 文件不存在: {target}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise FileIOError(f"读取 JSONL 失败（约第 {line_no} 行）: {target}") from exc


def _import_yaml():
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - 依赖缺失路径
        raise UtilError("需要 PyYAML：pip install PyYAML") from exc
    return yaml


def write_yaml(path: str | os.PathLike[str], data: Any) -> Path:
    """将对象安全序列化为 YAML 并原子写入。"""

    yaml = _import_yaml()
    try:
        payload = yaml.safe_dump(
            data,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )
    except (TypeError, ValueError) as exc:
        raise FileIOError(f"YAML 序列化失败: {path}") from exc
    return atomic_write_text(path, payload)


def read_yaml(path: str | os.PathLike[str], default: Any = _MISSING) -> Any:
    """读取 YAML；空文件返回 ``{}`` 或调用方提供的默认值。"""

    target = Path(path).expanduser().resolve()
    if not target.exists() and default is not _MISSING:
        return default
    yaml = _import_yaml()
    try:
        content = target.read_text(encoding=DEFAULT_ENCODING)
        value = yaml.safe_load(content)
    except FileNotFoundError as exc:
        raise FileIOError(f"YAML 文件不存在: {target}") from exc
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise FileIOError(f"读取或解析 YAML 失败: {target}") from exc
    if value is None:
        return {} if default is _MISSING else default
    return value


def write_csv(
    path: str | os.PathLike[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    fieldnames: Sequence[str] | None = None,
) -> Path:
    """写入 CSV；未提供表头时使用首行键名，空数据仅创建空文件。"""

    materialized = [dict(row) for row in rows]
    target = Path(path).expanduser().resolve()
    ensure_dir(target.parent)
    if fieldnames is None and materialized:
        fieldnames = list(materialized[0].keys())
    if fieldnames is None:
        return atomic_write_text(target, "")

    tmp_name: str | None = None
    try:
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
        )
        with os.fdopen(fd, "w", encoding=DEFAULT_ENCODING, newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
            writer.writeheader()
            writer.writerows(materialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target)
        tmp_name = None
        return target
    except (OSError, UnicodeError, csv.Error) as exc:
        raise FileIOError(f"写入 CSV 失败: {target}") from exc
    finally:
        if tmp_name and Path(tmp_name).exists():
            try:
                Path(tmp_name).unlink()
            except OSError:  # pragma: no cover
                pass


def read_csv(path: str | os.PathLike[str], default: Any = _MISSING) -> list[dict[str, str]]:
    """读取 CSV 为字典列表；文件不存在时可按需返回默认值。"""

    target = Path(path).expanduser().resolve()
    if not target.exists() and default is not _MISSING:
        return default
    try:
        with target.open("r", encoding=DEFAULT_ENCODING, newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except FileNotFoundError as exc:
        raise FileIOError(f"CSV 文件不存在: {target}") from exc
    except (OSError, UnicodeError, csv.Error) as exc:
        raise FileIOError(f"读取 CSV 失败: {target}") from exc


def load_any(path: str | os.PathLike[str], default: Any = _MISSING) -> Any:
    """按扩展名自动读取 .json/.jsonl/.yaml/.yml/.csv，其余按文本读取。"""

    target = Path(path).expanduser().resolve()
    suffix = target.suffix.lower()
    if suffix == ".json":
        return read_json(target, default)
    if suffix == ".jsonl":
        return read_jsonl(target, default)
    if suffix in {".yaml", ".yml"}:
        return read_yaml(target, default)
    if suffix == ".csv":
        return read_csv(target, default)
    return read_text(target, default=default)


def save_any(path: str | os.PathLike[str], data: Any) -> Path:
    """按扩展名自动写入 .json/.jsonl/.yaml/.yml/.csv，其余按文本写入。"""

    target = Path(path)
    suffix = target.suffix.lower()
    if suffix == ".json":
        return write_json(target, data)
    if suffix == ".jsonl":
        return write_jsonl(target, data)
    if suffix in {".yaml", ".yml"}:
        return write_yaml(target, data)
    if suffix == ".csv":
        return write_csv(target, data)
    return write_text(target, str(data))


# ---------------------------------------------------------------------------
# 其他通用函数
# ---------------------------------------------------------------------------
def file_sha256(path: str | os.PathLike[str], *, chunk_size: int = 1024 * 1024) -> str:
    """计算文件 SHA-256，用于数据快照去重与可追溯。"""

    digest = hashlib.sha256()
    try:
        with Path(path).expanduser().open("rb") as handle:
            for block in iter(lambda: handle.read(chunk_size), b""):
                digest.update(block)
    except OSError as exc:
        raise FileIOError(f"计算文件哈希失败: {path}") from exc
    return digest.hexdigest()


def human_size(size: int) -> str:
    """把字节数转为易读字符串。"""

    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


def deep_get(mapping: Mapping[str, Any] | Sequence[Any], dotted: str, default: Any = None) -> Any:
    """按 ``a.b.0.c`` 形式读取嵌套字典 / 列表，缺失时返回默认值。"""

    current: Any = mapping
    for part in str(dotted).split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
        elif isinstance(current, Sequence) and not isinstance(current, (str, bytes)):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return default
        else:
            return default
    return current


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """递归合并字典，``override`` 优先，返回新字典（不修改入参）。"""

    merged: dict[str, Any] = dict(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, Mapping) and isinstance(value, Mapping):
            merged[key] = deep_merge(current, value)
        else:
            merged[key] = value
    return merged


def chunked(items: Iterable[Any], size: int) -> Iterator[list[Any]]:
    """把任意可迭代对象切分为固定大小的列表。"""

    if size <= 0:
        raise ValueError("size 必须为正整数")
    bucket: list[Any] = []
    for item in items:
        bucket.append(item)
        if len(bucket) >= size:
            yield bucket
            bucket = []
    if bucket:
        yield bucket


# ---------------------------------------------------------------------------
# 日志
# ---------------------------------------------------------------------------
def setup_logging(
    *,
    level: str | int = "INFO",
    log_file: str | os.PathLike[str] | None = None,
    console: bool = True,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
    force: bool = False,
) -> logging.Logger:
    """初始化应用日志（控制台 + 可选滚动文件），幂等。

    Args:
        level: 日志级别，字符串或 ``logging`` 常量。
        log_file: 日志文件路径；为 ``None`` 时只输出控制台。
        console: 是否输出到标准输出。
        max_bytes: 单文件上限，超过后滚动。
        backup_count: 保留的历史文件数量。
        force: 为 ``True`` 时关闭并重建 handler（测试常用）。
    """

    global _CONFIGURED
    logger = logging.getLogger(APP_LOGGER_NAME)

    if _CONFIGURED and not force:
        return logger

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:  # pragma: no cover - 关闭失败不影响重建
            pass

    logger.setLevel(level if isinstance(level, int) else str(level).upper())
    logger.propagate = False
    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if log_file is not None:
        target = ensure_dir(Path(log_file).expanduser().resolve().parent) / Path(log_file).name
        file_handler = RotatingFileHandler(
            target,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=DEFAULT_ENCODING,
            delay=False,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not logger.handlers:  # 兜底：至少不让日志调用报错
        logger.addHandler(logging.NullHandler())

    _CONFIGURED = True
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """获取应用命名空间下的 logger；调用前建议先执行 ``setup_logging``。"""

    if not name or name == APP_LOGGER_NAME:
        return logging.getLogger(APP_LOGGER_NAME)
    if name.startswith(f"{APP_LOGGER_NAME}."):
        return logging.getLogger(name)
    return logging.getLogger(f"{APP_LOGGER_NAME}.{name}")
````

## `pyproject.toml`

````toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "outdoor-ess-ai"
version = "0.1.0"
description = "欧美轻量化户外储能全链路 AI 自动化系统（离线模拟版）"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "Outdoor ESS AI" }]
dependencies = [
  "PyYAML>=6.0.1,<7.0",
  "python-dotenv>=1.0.1,<2.0",
]

[project.optional-dependencies]
llm = ["openai>=1.55.0,<4.0", "httpx>=0.27.0,<1.0"]
analysis = ["pandas>=2.2.0,<4.0"]
ui = ["streamlit>=1.50.0,<2.0", "pandas>=2.2.0,<4.0"]
research = [
  "requests>=2.31.0,<3.0",
  "beautifulsoup4>=4.12.0,<5.0",
  "openpyxl>=3.1.0,<4.0",
]
dev = [
  "pytest>=8.0,<10.0",
  "pytest-cov>=5.0,<8.0",
  "ruff>=0.6.0,<1.0",
  "mypy>=1.10.0,<2.0",
]

[project.scripts]
outdoor-ess-ai = "ess_ai.cli:main"

[tool.setuptools]
py-modules = ["main", "utils", "product_research", "listing_generator", "competitor_monitor", "compliance_check", "report_generator", "interview_demo", "error_guard"]

[tool.setuptools.packages.find]
include = ["ess_ai*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
addopts = "-q -p no:cacheprovider"

[tool.ruff]
line-length = 110
target-version = "py311"
extend-exclude = [".pytest_*", "tests/_artifacts", ".vendor", ".taste-skill"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true
check_untyped_defs = true
````

## `.env.example`

````
# =============================================================================
# 复制为 .env 后按需修改；不要提交真实密钥。
# 离线演示无需任何密钥。
# =============================================================================
DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
ESS_AI_MODE=offline
ESS_AI_MODEL=deepseek-v4.1-flash
ESS_AI_LOG_LEVEL=INFO
# ESS_AI_OUTPUT_DIR=outputs
````

## `start.ps1`

````powershell
# Compatibility alias: old start.ps1 now launches the full Streamlit console.
& "$PSScriptRoot\start_all.ps1" @args
exit $LASTEXITCODE
````

## `start.sh`

````bash
#!/usr/bin/env bash
# Compatibility alias: old start.sh now launches the full Streamlit console.
exec "$(cd "$(dirname "$0")" && pwd)/start_all.sh" "$@"
````

## `ess_ai/__init__.py`

````python
"""业务分层包：采集、清洗、分析、文案、Listing、合规、报告、流水线。"""

__version__ = "0.1.0"
__all__ = ["__version__"]
````

## `ess_ai/analysis/__init__.py`

````python
"""分析层：市场评分、选品机会与进入策略。"""

from ess_ai.analysis.market_analyzer import MarketAnalyzer

__all__ = ["MarketAnalyzer"]
````

## `ess_ai/collectors/__init__.py`

````python
"""数据采集层：公开数据口径的离线模拟采集器。"""

from ess_ai.collectors.mock_collector import MockCollector

__all__ = ["MockCollector"]
````

## `ess_ai/compliance/__init__.py`

````python
"""合规层：规则初筛、认证缺口与风险提示。"""

from ess_ai.compliance.checker import ComplianceChecker

__all__ = ["ComplianceChecker"]
````

## `ess_ai/content/__init__.py`

````python
"""内容层：短视频脚本、社媒文案与博客提纲。"""

from ess_ai.content.generator import ContentGenerator

__all__ = ["ContentGenerator"]
````

## `ess_ai/integrations/__init__.py`

````python
"""集成层：DeepSeek OpenAI-compatible 客户端与离线回退。"""

from ess_ai.integrations.llm_client import DeepSeekClient, LLMResult

__all__ = ["DeepSeekClient", "LLMResult"]
````

## `ess_ai/listing/__init__.py`

````python
"""Listing 层：标题、五点、描述与搜索词生成。"""

from ess_ai.listing.optimizer import ListingOptimizer

__all__ = ["ListingOptimizer"]
````

## `ess_ai/pipelines/__init__.py`

````python
"""流水线层：编排采集、清洗、分析、内容、合规与报告。"""

from ess_ai.pipelines.full_chain import FullChainPipeline

__all__ = ["FullChainPipeline"]
````

## `ess_ai/processing/__init__.py`

````python
"""数据清洗层：单位、币种、字段标准化。"""

from ess_ai.processing.normalizer import DataNormalizer

__all__ = ["DataNormalizer"]
````

## `ess_ai/reporting/__init__.py`

````python
"""报告层：汇总指标并输出 Markdown/JSON 报告。"""

from ess_ai.reporting.report_builder import ReportBuilder

__all__ = ["ReportBuilder"]
````

## `ess_ai/storage/__init__.py`

````python
"""存储层：本地 JSON 快照与运行清单。"""

from ess_ai.storage.repository import JsonStore, RunStore

__all__ = ["JsonStore", "RunStore"]
````

## `.streamlit/config.toml`

````toml
# Streamlit 本地运行配置
# 关闭 developmentMode，允许命令行指定 --server.port。
[global]
developmentMode = false

[server]
headless = true
address = "127.0.0.1"
port = 8501

[browser]
gatherUsageStats = false
````

## `app.py`

````python
#!/usr/bin/env python3
"""Tundra · 户外储能出海 AI 控制台。

A+C 视觉方向：苔原账本浅色主体 + 深色运行日志抽屉。
本文件只做本地 Streamlit 控制台，核心业务逻辑仍在各 CLI 模块中。

启动：
    streamlit run app.py
或：
    powershell -ExecutionPolicy Bypass -File .\\start_all.ps1
"""

from __future__ import annotations

import csv
import html
import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from error_guard import install_global_handler, log_command_error, log_exception  # noqa: E402
from utils import ensure_dir, read_json, read_text, write_text  # noqa: E402

install_global_handler("streamlit")
st.set_page_config(
    page_title="Tundra · 户外储能出海控制台",
    page_icon="◒",
    layout="wide",
    initial_sidebar_state="auto",
)

ROOT = PROJECT_ROOT
OUTPUTS = ROOT / "outputs"
LOG_DIR = OUTPUTS / "logs"
RUN_LOG = LOG_DIR / "ui_commands.log"
RESEARCH_XLSX = OUTPUTS / "research" / "high_potential_products.xlsx"
RESEARCH_SUMMARY = OUTPUTS / "research" / "research_summary.json"
LISTING_SUMMARY = OUTPUTS / "listing" / "listing_summary.json"
MONITOR_SUMMARY = OUTPUTS / "monitor" / "reports" / "monitor_summary.json"
COMPLIANCE_SUMMARY = OUTPUTS / "compliance" / "compliance_summary.json"
OPS_SUMMARY = OUTPUTS / "operations" / "report_summary.json"
INTERVIEW_MD = OUTPUTS / "interview" / "interview_demo.md"

PAGES = ["总览", "选品研究", "上架素材", "竞品监控", "合规校验", "经营报表", "面试演示"]
PAGE_INDEX = {page: index for index, page in enumerate(PAGES, start=1)}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
:root{
  --frame:#EDF3EE; --ground:#F4F7F3; --surface:#FFFFFF; --raised:#F7FAF7;
  --ink:#14201B; --muted:#56665D; --faint:#5B6B62;
  --line:#DCE5DF; --line-soft:#E9EFEA;
  --accent:#1F6F5C; --accent-ink:#155446; --mint:#DDE9E1;
  --amber:#A66A1F; --amber-bg:#FBF2E5;
  --red:#B42318; --red-bg:#FBEDEA;
  --dark:#101816;
  --sans:'IBM Plex Sans','Microsoft YaHei',system-ui,sans-serif;
  --mono:'IBM Plex Mono','Cascadia Mono',Consolas,monospace;
}
html, body, [class*="css"] { font-family:var(--sans); }
.stApp, .stApp p, .stApp span, .stApp div, .stApp label, .stApp button, .stApp h1 { font-family:var(--sans); }
.kpi-value,.overview-table .num,.overview-table .sku,.panel-meta,.foot-right,.log,.log *,.side-stat b{font-family:var(--mono);}
.stApp{
  background:radial-gradient(1000px 500px at 5% -10%, #E9F2EB 0%, transparent 60%), var(--frame);
  color:var(--ink);
}
.block-container{padding-top:0 !important; padding-bottom:18px !important; padding-left:18px !important; padding-right:18px !important; max-width:none !important;}
header[data-testid="stHeader"]{background:transparent;}
[data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu {display:none !important;}
section[data-testid="stSidebar"]{
  width:232px !important; min-width:232px !important; background:var(--frame);
  border-right:none;
}
section[data-testid="stSidebar"] > div{padding-top:0;}
[data-testid="stSidebarContent"]{padding:0 14px 16px;}
[data-testid="stSidebarCollapseButton"]{color:var(--muted);}
[data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"]{
  display:flex !important; visibility:visible !important; opacity:1 !important;
  color:var(--ink) !important; background:var(--frame) !important; z-index:1000;
}
.stButton>button, .stDownloadButton>button{
  height:32px; min-height:32px; border-radius:6px; font-size:12px; font-weight:600;
  border:1px solid var(--line); background:var(--surface); color:#405249;
  box-shadow:none; padding:0 12px;
}
.stButton>button:hover, .stDownloadButton>button:hover{
  border-color:#B9C9BE; color:var(--ink); background:#F8FBF8;
}
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"]{
  background:var(--accent); border-color:var(--accent); color:#fff;
}
.stButton>button[kind="primary"]:hover{background:var(--accent-ink); border-color:var(--accent-ink);}
.stButton>button p, .stDownloadButton>button p{font-size:12px; font-weight:600;}
div[data-testid="stVerticalBlock"]{gap:0;}
div[data-testid="stHorizontalBlock"]{gap:14px;}
.stSelectbox label, .stMultiSelect label, .stRadio label{font-size:11px; color:var(--muted);}
[data-testid="stSidebar"] div[role="radiogroup"]{gap:2px;}
[data-testid="stSidebar"] div[data-testid="stRadioGroup"]{margin-top:18px;}
[data-testid="stSidebar"] div[data-testid="stRadioGroup"] > div > label[data-testid="stRadioOption"]{
  min-height:34px; border-radius:7px; padding:7px 10px; margin:0; width:100%; box-sizing:border-box;
  display:flex !important; align-items:center;
  color:#405249; font-size:12px; transition:background .12s ease; background:transparent !important;
}
[data-testid="stSidebar"] div[data-testid="stRadioGroup"] > div > label[data-testid="stRadioOption"]:hover{background:#E5EEE7 !important;}
[data-testid="stSidebar"] div[data-testid="stRadioGroup"] > div[data-selected="true"] > label[data-testid="stRadioOption"],
[data-testid="stSidebar"] div[data-testid="stRadioGroup"] > div > label[data-selected="true"]{
  background:var(--mint) !important; color:var(--ink) !important; font-weight:600;
}
[data-testid="stSidebar"] div[data-testid="stRadioGroup"] label[data-testid="stRadioOption"] > div{width:100%;}
[data-testid="stSidebar"] div[data-testid="stRadioGroup"] label[data-testid="stRadioOption"] > div > div:first-child{display:none;}
[data-testid="stSidebar"] div[data-testid="stRadioGroup"] label[data-testid="stRadioOption"] p{font-size:12px; line-height:1.2; margin:0;}
[data-testid="stSidebar"] .stButton>button{width:100%; height:29px; min-height:29px; background:transparent; border-color:var(--line); font-size:11px; font-weight:500; text-align:left; justify-content:flex-start; padding:0 10px; color:var(--muted);}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.45);}
[data-testid="stSidebar"] .stButton{margin-top:4px;}
.st-key-sheet{
  background:var(--surface); border:1px solid #D8E3DA; border-radius:16px;
  padding:24px 28px 18px; min-height:calc(100vh - 76px);
}
.topbar{height:54px; display:flex; align-items:center; justify-content:space-between; padding:0 22px 0 24px;}
.crumb{font-size:11px; color:var(--faint);}
.crumb b{color:var(--ink); font-weight:500;}
.top-actions{display:flex; align-items:center; gap:9px;}
.sim-pill{font-family:var(--mono); font-size:11px; color:var(--muted); border:1px solid var(--line); border-radius:99px; padding:5px 9px; background:rgba(255,255,255,.45);}
.top-status{font-size:11px; color:var(--muted); display:inline-flex; align-items:center; gap:6px;}
.dot{width:5px; height:5px; border-radius:50%; display:inline-block; background:var(--accent);}
.dot.amber{background:var(--amber);} .dot.red{background:var(--red);} .dot.grey{background:#AAB9AE;}
.pagehead{display:flex; align-items:flex-start; justify-content:space-between; gap:20px; min-height:72px;}
.overline{font-size:11px; color:var(--faint); font-weight:500; margin-bottom:6px;}
.pagehead h1{font-size:27px; line-height:1.15; font-weight:500; letter-spacing:-.02em; margin:0;}
.sub{margin-top:6px; font-size:12px; color:var(--muted); display:flex; align-items:center; gap:8px; flex-wrap:wrap;}
.sub .sep{width:1px; height:10px; background:var(--line);}
.head-actions{padding-top:7px; display:flex; gap:12px; align-items:center; justify-content:flex-end;}
.st-key-head_actions{padding-top:7px; display:flex; justify-content:flex-end;}
.st-key-head_actions .stButton{margin:0;}
.text-action{font-size:11px; color:var(--muted); text-decoration:none; display:inline-flex; align-items:center; gap:5px;}
.text-action:hover{color:var(--ink);}
.brand{height:56px; display:flex; align-items:center; gap:10px; padding:0 6px;}
.mark{width:24px; height:24px; border:1px solid var(--ink); border-radius:7px; display:grid; place-items:center; position:relative; flex:0 0 auto;}
.mark:before,.mark:after{content:""; position:absolute; background:var(--ink); border-radius:1px;}
.mark:before{width:10px; height:1px; transform:rotate(-34deg); left:7px; top:13px;}
.mark:after{width:7px; height:1px; transform:rotate(34deg); left:11px; top:12px;}
.wordmark{font-size:14px; font-weight:600; letter-spacing:.02em;}
.wordmark span{display:block; font-size:11px; color:var(--muted); letter-spacing:0; font-weight:500; margin-top:1px;}
.workspace{margin:2px 0 14px; padding:8px 10px; border:1px solid var(--line); border-radius:8px; display:flex; align-items:center; justify-content:space-between; background:rgba(255,255,255,.38);}
.workspace b{display:block; font-size:12px; font-weight:600;}
.workspace small{display:block; font-size:11px; color:var(--muted); margin-top:2px;}
.chev{color:var(--faint); font-size:12px;}
.nav-label{font-size:11px; color:var(--faint); font-weight:500; margin:9px 8px 6px;}
.rail-foot{margin-top:18px; border-top:1px solid var(--line); padding:12px 4px 0;}
.system-row{display:flex; align-items:center; justify-content:space-between; font-size:11px; color:var(--muted); padding:4px 0;}
.system-note{font-size:11px; line-height:1.55; color:var(--faint); margin-top:6px;}
.side-stats{display:grid; grid-template-columns:1fr 1fr; gap:6px; margin:10px 0 12px;}
.side-stat{background:rgba(255,255,255,.4); border:1px solid var(--line-soft); border-radius:7px; padding:7px 8px;}
.side-stat b{display:block; font-family:var(--mono); font-size:14px; font-weight:500;}
.side-stat span{display:block; font-size:11px; color:var(--muted); margin-top:2px;}
.flow{margin-top:16px; background:var(--raised); border:1px solid var(--line-soft); border-radius:9px; display:flex; align-items:stretch; min-height:70px; overflow:hidden;}
.flow-node{flex:1; padding:11px 14px; position:relative; min-width:0;}
.flow-node + .flow-node:before{content:""; position:absolute; left:0; top:15px; bottom:15px; width:1px; background:var(--line);}
.flow-kicker{font-size:11px; color:var(--faint); font-weight:500; white-space:nowrap;}
.flow-main{display:flex; align-items:baseline; gap:6px; margin-top:3px; min-width:0;}
.flow-value{font-size:22px; line-height:1; font-weight:500; letter-spacing:-.02em; white-space:nowrap;}
.flow-unit{font-size:11px; color:var(--muted); white-space:nowrap;}
.flow-meta{font-size:11px; color:var(--muted); margin-top:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.arrow{position:absolute; right:-5px; top:50%; z-index:2; width:9px; height:9px; border-top:1px solid #B7C7BD; border-right:1px solid #B7C7BD; transform:translateY(-50%) rotate(45deg); background:var(--raised);}
.flow-node:last-child .arrow{display:none;}
.green{color:var(--accent);} .red-text{color:var(--red);} .amber-text{color:var(--amber);}
.kpi-strip{display:grid; grid-template-columns:1.1fr 1fr 1fr; border-top:1px solid var(--line-soft); border-bottom:1px solid var(--line-soft); margin-top:16px; padding:11px 0;}
.kpi{padding:0 18px; position:relative;}
.kpi:first-child{padding-left:0;} .kpi:last-child{padding-right:0;}
.kpi + .kpi:before{content:""; position:absolute; left:0; top:2px; bottom:2px; width:1px; background:var(--line-soft);}
.kpi-label{font-size:11px; color:var(--faint); font-weight:500;}
.kpi-value{font-family:var(--mono); font-size:25px; line-height:1.05; font-weight:500; margin-top:5px; letter-spacing:-.04em;}
.kpi-note{font-size:11px; color:var(--muted); margin-top:5px; display:flex; gap:7px; align-items:center; flex-wrap:wrap;}
.main-grid{display:grid; grid-template-columns:minmax(0,1.52fr) minmax(300px,.78fr); gap:20px; margin-top:16px; align-items:start;}
.main-grid > div,.main-grid > aside{min-width:0;}
.panel{border:1px solid var(--line-soft); border-radius:9px; background:var(--surface); min-width:0;}
.panel-head{height:40px; padding:0 14px; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid var(--line-soft);}
.panel-title{font-size:11px; font-weight:600; display:flex; align-items:center; gap:7px;}
.panel-title .num{font-family:var(--mono); font-size:11px; color:var(--faint); font-weight:400;}
.panel-meta{font-size:11px; color:var(--faint); font-family:var(--mono);}
.panel-link{font-size:11px; color:var(--accent); text-decoration:none; font-weight:500;}
.priority{padding-bottom:4px;}
.action-row{display:flex; align-items:center; gap:11px; padding:9px 14px; border-bottom:1px solid var(--line-soft); min-height:52px;}
.action-row:last-child{border-bottom:none;}
.prio{width:31px; height:21px; border-radius:4px; display:grid; place-items:center; font-family:var(--mono); font-size:11px; font-weight:500; flex:0 0 auto;}
.prio.p1{background:var(--red-bg); color:var(--red);}
.prio.p2{background:var(--amber-bg); color:var(--amber);}
.prio.p3{background:#EDF2EE; color:#53645B;}
.action-copy{flex:1; min-width:0;}
.action-copy b{display:block; font-size:12px; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.action-copy span{display:block; font-size:11px; color:var(--muted); margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.action-arrow{color:#71877A; font-size:14px; flex:0 0 auto;}
.overview-table{width:100%; border-collapse:collapse; table-layout:fixed;}
.overview-table th{font-size:11px; color:var(--faint); font-weight:500; text-align:left; padding:7px 10px 6px; border-bottom:1px solid var(--line-soft); white-space:nowrap;}
.overview-table td{font-size:11px; color:#25372E; padding:6px 10px; border-bottom:1px solid #F0F4F1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; line-height:1.25;}
.overview-table tr:last-child td{border-bottom:none;}
.overview-table th.num,.overview-table td.num{text-align:right; font-family:var(--mono); font-variant-numeric:tabular-nums;}
.overview-table td.sku{font-family:var(--mono); font-size:11px; color:#405249; letter-spacing:-.02em;}
.status{display:inline-flex; align-items:center; gap:4px; font-size:11px; padding:2px 6px; border-radius:99px; font-weight:500; white-space:nowrap;}
.status .sdot{width:4px; height:4px; border-radius:50%;}
.st-green{background:#EAF4ED; color:#22734A;} .st-green .sdot{background:#2E8B57;}
.st-amber{background:#FBF2E5; color:#8A5B18;} .st-amber .sdot{background:#B7791F;}
.st-red{background:#FBEDEA; color:#9E2A20;} .st-red .sdot{background:#C0392B;}
.st-grey{background:#EEF2EF; color:#5F6F66;} .st-grey .sdot{background:#819188;}
.side-stack{display:flex; flex-direction:column; gap:14px; min-width:0;}
.compliance{padding:13px 14px 13px;}
.bar{height:8px; display:flex; border-radius:99px; overflow:hidden; margin:11px 0 9px; background:#EEF2EF;}
.bar span{height:100%;}
.legend{display:flex; gap:12px; flex-wrap:wrap;}
.leg{font-size:11px; color:var(--muted); display:inline-flex; align-items:center; gap:5px;}
.sw{width:5px; height:5px; border-radius:1px; display:inline-block;}
.sw.red{background:var(--red);} .sw.amber{background:#C28A37;} .sw.grey{background:#C9D4CC;}
.compliance-foot{display:flex; justify-content:space-between; border-top:1px solid var(--line-soft); margin-top:10px; padding-top:9px; font-size:11px; color:var(--muted);}
.compliance-foot b{font-family:var(--mono); font-weight:500; color:var(--ink);}
.mini-panel{padding:12px 14px 12px;}
.mini-title{font-size:11px; color:var(--faint); font-weight:500;}
.mini-row{display:flex; align-items:center; justify-content:space-between; margin-top:7px; font-size:11px;}
.mini-row span{color:var(--muted);} .mini-row b{font-family:var(--mono); font-weight:500; color:var(--ink);}
.log{background:var(--dark); border:1px solid #1D2A24; border-radius:9px; padding:12px 14px 11px; color:#DCE8E1; min-height:158px; display:flex; flex-direction:column;}
.log-head{display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid #25352D; padding-bottom:8px;}
.log-title{font-size:11px; font-weight:500; color:#EFF6F2; display:flex; align-items:center; gap:7px;}
.log-title .pulse{width:5px; height:5px; border-radius:50%; background:#63C79E; box-shadow:0 0 0 3px rgba(99,199,158,.08);}
.log-status{font-family:var(--mono); font-size:11px; color:#8CC9AC;}
.log-lines{font-family:var(--mono); font-size:11px; line-height:1.6; margin-top:8px; flex:1;}
.log-line{display:flex; gap:7px; color:#AABCB1; white-space:nowrap;}
.log-line .t{color:#8FA79A; flex:0 0 58px;}
.log-line .k{color:#D7E5DC; flex:0 0 78px;}
.log-line .v{color:#AFC2B6; flex:1; overflow:hidden; text-overflow:ellipsis;}
.log-line .d{color:#8FA79A; text-align:right;}
.log-foot{display:flex; justify-content:space-between; border-top:1px solid #25352D; margin-top:5px; padding-top:7px; font-family:var(--mono); font-size:11px; color:#8FA79A;}
.log-foot a{color:#9ED3B9; text-decoration:none;}
.foot{margin-top:12px; display:flex; align-items:center; justify-content:space-between; color:var(--faint); font-size:11px; gap:14px; flex-wrap:wrap;}
.foot-right{font-family:var(--mono);}
.toolbar{display:flex; align-items:flex-end; gap:12px; margin:14px 0 10px; flex-wrap:wrap;}
.toolbar .grow{flex:1; min-width:0;}
.section-title{font-size:12px; font-weight:600; margin:14px 0 7px;}
.stDataFrame{border:1px solid var(--line-soft); border-radius:8px; overflow:hidden;}
[data-testid="stDataFrame"] div[role="columnheader"]{background:var(--raised); color:var(--faint); font-size:11px;}
[data-testid="stDataFrame"] [role="gridcell"]{font-size:11px;}
[data-testid="stExpander"] details{border-color:var(--line-soft); border-radius:8px;}
[data-testid="stTabs"] [data-baseweb="tab-list"]{gap:4px; border-bottom:1px solid var(--line-soft);}
[data-testid="stTabs"] [data-baseweb="tab"]{background:transparent; border:none; border-radius:0; padding:7px 10px; font-size:11px; color:var(--muted);}
[data-testid="stTabs"] [aria-selected="true"]{color:var(--ink); border-bottom:2px solid var(--accent);}
.stAlert{border-radius:8px; font-size:11px;}
.stInfo{border-radius:8px;}
.stSpinner{font-size:11px;}
div[data-testid="stSelectbox"] div[data-baseweb="select"]{font-size:11px;}
@media(max-width:1100px){.kpi-strip{grid-template-columns:1fr; gap:14px;} .kpi{padding:0;} .kpi + .kpi:before{display:none;} .kpi + .kpi{border-top:1px solid var(--line-soft); padding-top:13px;} .main-grid{grid-template-columns:1fr;} .side-stack{display:grid; grid-template-columns:1fr 1fr;} .flow{flex-wrap:wrap;} .flow-node{flex:1 0 33%;} .flow-node:nth-child(3):before{display:none;}}
@media(max-width:760px){.topbar{padding:0 16px 0 52px;} [data-testid="stExpandSidebarButton"]{display:flex !important; position:fixed; left:10px; top:10px; width:34px; height:34px; z-index:1200; background:var(--frame) !important; border:1px solid var(--line); border-radius:8px; color:var(--ink) !important; align-items:center; justify-content:center;} [data-testid="stExpandSidebarButton"] span{font-size:18px;} .top-actions .sim-pill{display:none;} .st-key-sheet{border-radius:0; padding:20px;} .pagehead{display:block;} .head-actions{justify-content:flex-start; padding-top:14px;} .side-stack{grid-template-columns:1fr;} .flow-node{flex:1 0 50%;} .flow-node:nth-child(2n):before{display:none;} .flow-node:last-child{flex:1 0 100%;} .main-grid{grid-template-columns:1fr; gap:14px;}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _summary(path: Path) -> dict:
    try:
        value = read_json(path, default={})
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def _read_excel(path: Path, sheet: str, header_tokens: tuple[str, ...] = ("SKU",)) -> tuple[list[str], list[dict]]:
    if not path.exists():
        return [], []
    try:
        from openpyxl import load_workbook

        wb = load_workbook(path, read_only=True, data_only=True)
        ws = wb[sheet] if sheet in wb.sheetnames else wb[wb.sheetnames[0]]
        headers: list[str] = []
        header_row = 1
        for index, row in enumerate(ws.iter_rows(min_row=1, max_row=25, values_only=True), start=1):
            values = [str(cell or "").strip() for cell in row]
            if any(token in values for token in header_tokens):
                headers = values
                header_row = index
                break
        rows: list[dict] = []
        for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
            if not any(cell is not None and str(cell).strip() for cell in row):
                continue
            rows.append({headers[i]: row[i] for i in range(min(len(headers), len(row)))})
        wb.close()
        return headers, rows
    except Exception as exc:
        log_exception(exc, app="streamlit", context={"read_excel": str(path)})
        return [], []


def _df(headers: list[str], rows: list[dict]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=headers)
    return pd.DataFrame(rows, columns=headers)


def _download(path: Path, label: str, mime: str = "application/octet-stream") -> None:
    if path.exists():
        st.download_button(
            label=f"下载 {label}",
            data=path.read_bytes(),
            file_name=path.name,
            mime=mime,
            width="content",
        )


def _run_log(entry: dict) -> None:
    ensure_dir(LOG_DIR)
    write_text(RUN_LOG, json.dumps(entry, ensure_ascii=False) + "\n", append=True)


def run_command(label: str, args: list[str], *, timeout: int = 300) -> subprocess.CompletedProcess | None:
    command = [sys.executable, *args]
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = str(VENDOR_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    started = time.time()
    proc: subprocess.CompletedProcess | None = None
    try:
        with st.spinner(f"正在执行：{label}"):
            proc = subprocess.run(
                command,
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                env=env,
                check=False,
            )
        elapsed = round(time.time() - started, 2)
        _run_log(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "label": label,
                "command": command,
                "returncode": proc.returncode,
                "elapsed_seconds": elapsed,
            }
        )
        if proc.returncode != 0:
            log_command_error("streamlit", command, proc.returncode, proc.stdout or "", proc.stderr or "")
            st.error(f"{label} 执行失败，退出码 {proc.returncode}。错误已写入 outputs/logs/errors.log")
        else:
            st.success(f"{label} 执行完成（{elapsed:.1f}s）")
        with st.expander("查看运行日志", expanded=proc.returncode != 0):
            st.code((proc.stdout or "") + ("\n[stderr]\n" + (proc.stderr or "") if proc.stderr else ""), language="text")
        return proc
    except subprocess.TimeoutExpired:
        log_exception(RuntimeError(f"{label} 执行超时"), app="streamlit", context={"command": command})
        st.error(f"{label} 执行超时（>{timeout}s），已记录错误日志。")
    except Exception as exc:
        log_exception(exc, app="streamlit", context={"command": command})
        st.error(f"{label} 执行异常：{exc}")
    return proc


def _page_header(title: str, description: str, page: str, action_label: str | None = None, action_cb=None) -> None:
    left, right = st.columns([3.1, 1.1])
    with left:
        st.markdown(
            f'<div class="pagehead"><div><div class="overline">Operating system · '
            f'{PAGE_INDEX.get(page, 1):02d} / 07</div><h1>{html.escape(title)}</h1>'
            f'<div class="sub">{description}</div></div></div>',
            unsafe_allow_html=True,
        )
    if action_label and action_cb:
        with right:
            with st.container(key="head_actions"):
                if st.button(action_label, type="primary", key=f"run_{page}"):
                    action_cb()


def _kpi_strip(items: list[tuple[str, str, str, str]]) -> str:
    blocks = []
    for label, value, note, color in items:
        blocks.append(
            f'<div class="kpi"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value {color}">{value}</div>'
            f'<div class="kpi-note">{note}</div></div>'
        )
    return '<div class="kpi-strip">' + "".join(blocks) + "</div>"


def _flow_html(research: dict, listing: dict, compliance: dict, ops: dict, monitor: dict) -> str:
    severity = compliance.get("severity", {}) or {}
    status = compliance.get("status", {}) or {}
    high = int(severity.get("high", 0))
    findings = int(compliance.get("finding_count", 0) or sum(int(v) for v in severity.values()))
    margin = (research.get("quality", {}) or {}).get("avg_margin_pct", 0)
    total_alerts = int((monitor.get("counts", {}) or {}).get("alerts", 0))
    failed = int((monitor.get("counts", {}) or {}).get("failed", 0))
    reviews = int((monitor.get("counts", {}) or {}).get("negative_reviews", 0))
    competitors = int((monitor.get("counts", {}) or {}).get("competitors", 0))
    flow = [
        ("01 / 选品", str(research.get("high_potential_records", "—")), "SKU", f"高潜力 · 平均毛利 {margin:.1f}%", ""),
        ("02 / 上架", str(len(listing.get("locales", [])) or "—"), "站点", "格式校验通过 · 导入需补资料", "green"),
        ("03 / 合规", str(high), "高风险", f"{status.get('PASS', 0)} PASS · {status.get('FAIL', 0)} FAIL · {findings} 项", "red-text"),
        ("04 / 经营", f"${ops.get('net_profit', 0):,.0f}" if ops else "—", "净利", f"ROI {ops.get('roi', 0):.2f}% · ACOS {ops.get('ad_acos', 0):.2f}%", ""),
        ("05 / 竞品", str(total_alerts), "预警", f"{competitors} 竞品 · {reviews} 差评 · {failed} 失败", "amber-text"),
    ]
    nodes = []
    for kicker, value, unit, meta, color in flow:
        nodes.append(
            f'<div class="flow-node"><div class="flow-kicker">{kicker}</div>'
            f'<div class="flow-main"><span class="flow-value {color}">{value}</span>'
            f'<span class="flow-unit">{unit}</span></div>'
            f'<div class="flow-meta">{meta}</div><span class="arrow"></span></div>'
        )
    return '<div class="flow">' + "".join(nodes) + "</div>"


def _priority_html(ops: dict, compliance: dict) -> str:
    metrics = ops.get("metrics", []) or []
    urgent = [m for m in metrics if m.get("stock_status") == "紧急补货"]
    slow = [m for m in metrics if m.get("stock_status") == "滞销"]
    urgent_text = f"{len(urgent)} 个 SKU 即将断货"
    urgent_meta = (
        f"{urgent[0].get('sku', '')} · 覆盖 {urgent[0].get('days_cover', '—')} 天 · 交期 {urgent[0].get('lead_time_days', '—')} 天"
        if urgent
        else "暂无紧急补货 SKU"
    )
    slow_text = f"{len(slow)} 个 SKU 库存超过 90 天" if slow else "库存覆盖健康"
    slow_meta = " · ".join(m.get("sku", "") for m in slow[:3]) or "无需处理"
    high = compliance.get("severity", {}).get("high", 0)
    return f"""
    <section class="panel priority">
      <div class="panel-head"><div class="panel-title"><span class="num">01</span>待处理 <span style="color:var(--faint);font-family:var(--mono);font-size:11px;font-weight:400">/ 3</span></div><span class="panel-link">查看全部 →</span></div>
      <div class="action-row"><span class="prio p1">P1</span><div class="action-copy"><b>{urgent_text}</b><span>{urgent_meta}</span></div><span class="action-arrow">→</span></div>
      <div class="action-row"><span class="prio p2">P2</span><div class="action-copy"><b>{slow_text}</b><span>{slow_meta}</span></div><span class="action-arrow">→</span></div>
      <div class="action-row"><span class="prio p3">合规</span><div class="action-copy"><b>{high} 个 CE/FCC 高风险项待补证</b><span>欧盟 LVD/EMC · GPSR 责任人 · 无线 FCC ID</span></div><span class="action-arrow">→</span></div>
    </section>
    """


def _profit_table_html(ops: dict) -> str:
    metrics = (ops.get("metrics", []) or [])[:5]
    if not metrics:
        return '<div class="panel"><div class="panel-head"><div class="panel-title"><span class="num">02</span>月度利润 · Top 5</div></div><div style="padding:18px;color:var(--muted);font-size:11px">尚未生成经营报表。</div></div>'
    status_class = {"健康": "st-green", "关注": "st-amber", "滞销": "st-grey", "紧急补货": "st-red"}
    rows = []
    for m in metrics:
        status = m.get("stock_status", "—")
        rows.append(
            f'<tr><td class="sku">{html.escape(str(m.get("sku", "")))}</td>'
            f'<td class="num">${m.get("revenue", 0):,.0f}</td>'
            f'<td class="num">${m.get("net_profit", 0):,.0f}</td>'
            f'<td class="num green">{m.get("roi", 0) * 100:.1f}%</td>'
            f'<td class="num">{m.get("inventory_turnover_days", 0):.1f}d</td>'
            f'<td><span class="status {status_class.get(status, "st-grey")}"><i class="sdot"></i>{html.escape(str(status))}</span></td></tr>'
        )
    return f"""
    <section class="panel" style="margin-top:14px">
      <div class="panel-head"><div class="panel-title"><span class="num">02</span>月度利润 · Top 5</div><div class="panel-meta">USD / 30d</div><span class="panel-link">打开报表 →</span></div>
      <table class="overview-table">
        <thead><tr><th style="width:27%">SKU</th><th class="num" style="width:16%">收入</th><th class="num" style="width:15%">净利润</th><th class="num" style="width:12%">ROI</th><th class="num" style="width:16%">周转</th><th style="width:14%">库存</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
    """


def _compliance_html(compliance: dict, listing: dict) -> str:
    severity = compliance.get("severity", {}) or {}
    status = compliance.get("status", {}) or {}
    high, medium, low = int(severity.get("high", 0)), int(severity.get("medium", 0)), int(severity.get("low", 0))
    total = max(1, high + medium + low)
    red, amber, grey = high / total * 100, medium / total * 100, low / total * 100
    locales = len(listing.get("locales", []))
    format_ok = "通过" if listing.get("format_ok_all") else "需检查"
    import_ready = "是" if listing.get("import_ready_all") else "需补 GTIN / 主图"
    return f"""
    <section class="panel compliance">
      <div class="panel-head" style="height:36px;padding:0;border:none;margin-bottom:2px"><div class="panel-title"><span class="num">03</span>合规状态</div><span class="panel-meta">9 SKU</span></div>
      <div class="bar"><span style="background:var(--red);width:{red:.1f}%"></span><span style="background:#C28A37;width:{amber:.1f}%"></span><span style="background:#C9D4CC;width:{grey:.1f}%"></span></div>
      <div class="legend"><span class="leg"><i class="sw red"></i>高风险 {high}</span><span class="leg"><i class="sw amber"></i>中风险 {medium}</span><span class="leg"><i class="sw grey"></i>低风险 {low}</span></div>
      <div class="compliance-foot"><span>PASS <b>{status.get('PASS', 0)}</b></span><span>FAIL <b>{status.get('FAIL', 0)}</b></span><span>CONDITIONAL <b>{status.get('CONDITIONAL', 0)}</b></span></div>
    </section>
    <section class="panel mini-panel">
      <div class="mini-title">Listing readiness</div>
      <div class="mini-row"><span>站点版本</span><b>{locales} / 4</b></div>
      <div class="mini-row"><span>格式校验</span><b class="green">{format_ok}</b></div>
      <div class="mini-row"><span>导入就绪</span><b class="amber-text">{import_ready}</b></div>
    </section>
    """


def _log_html() -> str:
    entries: list[dict] = []
    if RUN_LOG.exists():
        for line in read_text(RUN_LOG).splitlines()[-8:]:
            try:
                item = json.loads(line)
                if isinstance(item, dict):
                    entries.append(item)
            except json.JSONDecodeError:
                continue
    entries = entries[-4:]
    if not entries:
        entries = [
            {"timestamp": "03:08:19", "label": "选品", "elapsed_seconds": 0.9, "returncode": 0},
            {"timestamp": "03:08:20", "label": "Listing", "elapsed_seconds": 0.8, "returncode": 0},
            {"timestamp": "03:08:21", "label": "合规", "elapsed_seconds": 0.7, "returncode": 0},
            {"timestamp": "03:08:22", "label": "经营", "elapsed_seconds": 0.9, "returncode": 0},
        ]
    ok = sum(1 for item in entries if item.get("returncode") == 0)
    lines = []
    for item in entries:
        stamp = str(item.get("timestamp", ""))
        time_text = stamp[11:19] if len(stamp) >= 19 else (stamp[:8] if stamp else "--:--:--")
        label = str(item.get("label", "run"))[:12]
        elapsed = item.get("elapsed_seconds", 0)
        lines.append(
            f'<div class="log-line"><span class="t">{time_text}</span><span class="k">{html.escape(label)}</span>'
            f'<span class="v">{"完成" if item.get("returncode") == 0 else "失败"}</span><span class="d">{elapsed}s</span></div>'
        )
    return f"""
    <section class="log">
      <div class="log-head"><div class="log-title"><span class="pulse"></span>运行日志</div><div class="log-status">{ok} / {len(entries)} PASS</div></div>
      <div class="log-lines">{''.join(lines)}</div>
      <div class="log-foot"><span>errors 0 · local run</span><span>完整日志 →</span></div>
    </section>
    """


# ---------------------------------------------------------------------------
# sidebar + topbar
# ---------------------------------------------------------------------------
def _sidebar() -> str:
    research = _summary(RESEARCH_SUMMARY)
    listing = _summary(LISTING_SUMMARY)
    compliance = _summary(COMPLIANCE_SUMMARY)
    monitor = _summary(MONITOR_SUMMARY)
    with st.sidebar:
        st.markdown(
            '<div class="brand"><div class="mark"></div><div class="wordmark">Tundra<span>Outdoor ESS ops</span></div></div>'
            '<div class="workspace"><div><b>Outdoor ESS</b><small>EU / US workspace</small></div><div class="chev">⌄</div></div>'
            '<div class="nav-label">Workspace</div>',
            unsafe_allow_html=True,
        )
        page = st.radio("Navigation", PAGES, index=0, label_visibility="collapsed", key="primary_nav")
        st.markdown(
            f'<div class="side-stats">'
            f'<div class="side-stat"><b>{research.get("high_potential_records", "—")}</b><span>高潜 SKU</span></div>'
            f'<div class="side-stat"><b>{len(listing.get("locales", [])) or "—"}</b><span>Listing 站点</span></div>'
            f'<div class="side-stat"><b>{compliance.get("severity", {}).get("high", "—")}</b><span>合规高风险</span></div>'
            f'<div class="side-stat"><b>{monitor.get("counts", {}).get("alerts", "—")}</b><span>竞品预警</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="nav-label">System</div>', unsafe_allow_html=True)
        if st.button("检查项目结构", key="check_project", width="stretch"):
            run_command("项目检查", ["main.py", "check"], timeout=120)
        if st.button("查看错误日志", key="show_errors", width="stretch"):
            error_log = LOG_DIR / "errors.log"
            st.code(read_text(error_log, default="暂无错误日志")[-4000:], language="text")
        st.markdown(
            '<div class="rail-foot">'
            '<div class="system-row"><span><i class="dot"></i>系统正常</span><span>v1.0</span></div>'
            '<div class="system-row"><span>数据模式</span><span>模拟 · 固定种子</span></div>'
            '<div class="system-row"><span>最近运行</span><span>03:08</span></div>'
            '<div class="system-note">Public snapshots / no store API<br>Global error log active</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    return page


def _topbar(page: str) -> None:
    st.markdown(
        f'<div class="topbar"><div class="crumb">Workspace / <b>{html.escape(page)}</b></div>'
        '<div class="top-actions"><span class="sim-pill">Simulated · Q3 2026</span>'
        '<span class="top-status"><i class="dot"></i>local</span></div></div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# overview
# ---------------------------------------------------------------------------
def render_overview() -> None:
    research = _summary(RESEARCH_SUMMARY)
    listing = _summary(LISTING_SUMMARY)
    compliance = _summary(COMPLIANCE_SUMMARY)
    ops = _summary(OPS_SUMMARY)
    monitor = _summary(MONITOR_SUMMARY)
    _page_header(
        "经营总览",
        '<span>2026-09-01 — 09-30</span><span class="sep"></span><span>9 SKU · 4 站点</span><span class="sep"></span><span>数据截止 03:08</span>',
        "总览",
        "运行全链路",
        _run_all,
    )
    st.markdown(_flow_html(research, listing, compliance, ops, monitor), unsafe_allow_html=True)
    st.markdown(
        _kpi_strip(
            [
                ("Net profit / 30 days", f"${ops.get('net_profit', 0):,.2f}", '<span class="green">21.97%</span> 净利率 · 收入 $251,367', ""),
                ("Return on invested cost", f"{ops.get('roi', 0):.2f}%", f"总成本 ${ops.get('net_profit', 0) / (ops.get('roi', 1) / 100) if ops.get('roi') else 0:,.0f} · 9 SKU", ""),
                ("Inventory attention", f"{ops.get('inventory_alerts', 0)} SKU", f"<span class=\"red-text\">{ops.get('urgent_alerts', 0)} 紧急</span> · {ops.get('slow_moving', 0)} 滞销 · 1 关注", ""),
            ]
        ),
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.52, 0.78], gap="large")
    with left:
        st.markdown(_priority_html(ops, compliance), unsafe_allow_html=True)
        st.markdown(_profit_table_html(ops), unsafe_allow_html=True)
    with right:
        st.markdown('<div class="side-stack">', unsafe_allow_html=True)
        st.markdown(_compliance_html(compliance, listing), unsafe_allow_html=True)
        st.markdown(_log_html(), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    _download(OUTPUTS / "operations" / "monthly_profit.xlsx", "月度利润 Excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.markdown(
        '<div class="foot"><span>固定种子模拟 · 公开快照 · 不接入真实店铺后台</span><span class="foot-right">Tundra Ops / 2026.09</span></div>',
        unsafe_allow_html=True,
    )


def _run_all() -> None:
    steps = [
        ("基础 7 阶段流水线", ["main.py", "demo"]),
        ("公开数据选品", ["product_research.py"]),
        ("Amazon Listing", ["listing_generator.py", "--locales", "all"]),
        ("合规校验", ["compliance_check.py"]),
        ("经营报表", ["report_generator.py"]),
        ("竞品巡检", ["competitor_monitor.py", "run"]),
    ]
    for label, args in steps:
        proc = run_command(label, args, timeout=300)
        if proc is None or proc.returncode != 0:
            st.warning("全链路中断，请查看上方输出和 outputs/logs/errors.log")
            return
    st.success("全链路运行完成，可切换左侧模块查看结果。")


# ---------------------------------------------------------------------------
# research
# ---------------------------------------------------------------------------
def render_research() -> None:
    _page_header("选品研究", "<span>100-500Wh 公开数据清洗、三指标计算与高潜力 Excel</span>", "选品研究", "运行选品", lambda: run_command("选品研究", ["product_research.py"]))
    summary = _summary(RESEARCH_SUMMARY)
    _metric_strip_from_summary(summary)
    headers, rows = _read_excel(RESEARCH_XLSX, "高潜力选品", ("SKU",))
    if rows:
        st.markdown('<div class="section-title">高潜力选品表</div>', unsafe_allow_html=True)
        st.dataframe(_df(headers, rows), width="stretch", hide_index=True, height=430)
        _download(RESEARCH_XLSX, "高潜力选品 Excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("尚未生成选品结果，点击右上角“运行选品”。")
    st.caption("输出：outputs/research/high_potential_products.xlsx / research_summary.json")


def _metric_strip_from_summary(summary: dict) -> None:
    if not summary:
        return
    st.markdown(
        _kpi_strip(
            [
                ("Raw records", str(summary.get("raw_records", "—")), "公开快照 / 页面记录", ""),
                ("Cleaned records", str(summary.get("cleaned_records", "—")), "容量 / 价格 / 去重后", ""),
                ("High potential", str(summary.get("high_potential_records", "—")), "通过全部门槛", "green"),
            ]
        ),
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# listing
# ---------------------------------------------------------------------------
def render_listing() -> None:
    _page_header("上架素材", "<span>合规英文 / 本地化 Listing、5 点描述、详情页、Amazon 平铺文件</span>", "上架素材")
    toolbar = st.columns([1.5, 1.2, 2.3])
    with toolbar[0]:
        locale = st.selectbox("目标站点", ["en-US", "en-GB", "de-DE", "fr-FR", "all"], index=0, key="listing_locale")
    with toolbar[1]:
        if st.button("生成 Listing", type="primary", key="run_listing", width="stretch"):
            run_command("上架素材", ["listing_generator.py", "--locales", locale])
    summary = _summary(LISTING_SUMMARY)
    if summary:
        locales = summary.get("locales", [])
        st.markdown(
            _kpi_strip(
                [
                    ("Versions", str(len(locales)), "站点 / 语言版本", ""),
                    ("Format check", "通过" if summary.get("format_ok_all") else "未通过", "表头 / 长度 / 类型", "green" if summary.get("format_ok_all") else "red-text"),
                    ("Import ready", "是" if summary.get("import_ready_all") else "需补资料", "GTIN / 主图 / Browse Node", "amber-text"),
                ]
            ),
            unsafe_allow_html=True,
        )
        if locales:
            selected = st.selectbox("预览站点", [item["locale"] for item in locales], key="listing_preview")
            item = next((x for x in locales if x["locale"] == selected), locales[0])
            csv_path = ROOT / item["csv"] if not Path(item["csv"]).is_absolute() else Path(item["csv"])
            if csv_path.exists():
                with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    rows = list(reader)
                    cols = reader.fieldnames or []
                st.markdown(f'<div class="section-title">Amazon CSV 预览 · {html.escape(selected)}</div>', unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(rows, columns=cols), width="stretch", hide_index=True, height=280)
                _download(csv_path, f"{selected} Amazon CSV", "text/csv")
            validation = ROOT / item["validation"] if not Path(item["validation"]).is_absolute() else Path(item["validation"])
            if validation.exists():
                with st.expander("查看导入校验 JSON", expanded=False):
                    st.json(read_json(validation, default={}))
    else:
        st.info("尚未生成 Listing，点击上方“生成 Listing”。")


# ---------------------------------------------------------------------------
# monitor
# ---------------------------------------------------------------------------
def render_monitor() -> None:
    _page_header("竞品监控", "<span>公开价格 / BSR / 差评巡检、价格与排名预警、差评痛点报告</span>", "竞品监控")
    toolbar = st.columns([1.1, 1.1, 2.4])
    with toolbar[0]:
        mode = st.radio("数据模式", ["offline", "live", "auto"], horizontal=True, index=0, key="monitor_mode")
    with toolbar[1]:
        if st.button("巡检竞品", type="primary", key="run_monitor", width="stretch"):
            run_command("竞品监控", ["competitor_monitor.py", "run", "--mode", mode])
    summary = _summary(MONITOR_SUMMARY)
    if summary:
        counts = summary.get("counts", {})
        st.markdown(
            _kpi_strip(
                [
                    ("Competitors", str(counts.get("competitors", "—")), "注册表启用条目", ""),
                    ("Success / failed", f"{counts.get('success', 0)} / {counts.get('failed', 0)}", "失败链接自动跳过", "green"),
                    ("Alerts", str(counts.get("alerts", "—")), "价格 / BSR 异动", "amber-text"),
                ]
            ),
            unsafe_allow_html=True,
        )
        alert_path = ROOT / summary["latest_alerts"] if not Path(summary["latest_alerts"]).is_absolute() else Path(summary["latest_alerts"])
        report_path = ROOT / summary["latest_report"] if not Path(summary["latest_report"]).is_absolute() else Path(summary["latest_report"])
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown('<div class="section-title">最新预警</div>', unsafe_allow_html=True)
            if alert_path.exists():
                st.code(read_text(alert_path), language="text")
                _download(alert_path, "预警 TXT", "text/plain")
        with col2:
            st.markdown('<div class="section-title">差评痛点</div>', unsafe_allow_html=True)
            if report_path.exists():
                st.markdown(read_text(report_path)[:9000])
                _download(report_path, "痛点报告 Markdown", "text/markdown")
    else:
        st.info("尚未运行竞品巡检。离线演示可直接使用默认快照。")
    st.caption("定时巡检：python competitor_monitor.py schedule --interval-hours 6；页面内为单轮巡检。")


# ---------------------------------------------------------------------------
# compliance
# ---------------------------------------------------------------------------
def render_compliance() -> None:
    _page_header("合规校验", "<span>CE/FCC 规则初筛、风险评分、不符合项与修改建议</span>", "合规校验", "合规筛查", lambda: run_command("合规校验", ["compliance_check.py"]))
    summary = _summary(COMPLIANCE_SUMMARY)
    if summary:
        severity = summary.get("severity", {})
        status = summary.get("status", {})
        st.markdown(
            _kpi_strip(
                [
                    ("High risk", str(severity.get("high", "—")), "需优先处理", "red-text"),
                    ("Medium risk", str(severity.get("medium", "—")), "需补充文件", "amber-text"),
                    ("PASS / FAIL", f"{status.get('PASS', 0)} / {status.get('FAIL', 0)}", "无高/中风险 / 存在高风险", ""),
                ]
            ),
            unsafe_allow_html=True,
        )
        headers, rows = _read_excel(OUTPUTS / "compliance" / "compliance_check.xlsx", "合规汇总", ("SKU",))
        if rows:
            st.markdown('<div class="section-title">合规汇总</div>', unsafe_allow_html=True)
            st.dataframe(_df(headers, rows), width="stretch", hide_index=True, height=300)
        f_headers, findings = _read_excel(OUTPUTS / "compliance" / "compliance_check.xlsx", "不符合项", ("ID", "标准"))
        if findings:
            levels = sorted({str(x.get("严重级别", "")) for x in findings if x.get("严重级别")})
            selected = st.multiselect("筛选严重级别", levels, default=levels, key="compliance_levels")
            filtered = [x for x in findings if str(x.get("严重级别", "")) in selected]
            st.markdown('<div class="section-title">不符合项与修改建议</div>', unsafe_allow_html=True)
            st.dataframe(_df(f_headers, filtered), width="stretch", hide_index=True, height=350)
        _download(OUTPUTS / "compliance" / "compliance_check.xlsx", "合规校验 Excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("尚未运行合规筛查，点击右上角“合规筛查”。")


# ---------------------------------------------------------------------------
# operations
# ---------------------------------------------------------------------------
def render_operations() -> None:
    _page_header("经营报表", "<span>广告日报、库存预警、月度利润、ROI 与库存周转天数</span>", "经营报表", "生成报表", lambda: run_command("经营报表", ["report_generator.py"]))
    summary = _summary(OPS_SUMMARY)
    if summary:
        st.markdown(
            _kpi_strip(
                [
                    ("Revenue", f"${summary.get('revenue', 0):,.0f}", "30 天模拟", ""),
                    ("Net profit", f"${summary.get('net_profit', 0):,.0f}", f"{summary.get('net_margin', 0):.2f}% 净利率", "green"),
                    ("ROI / ACOS", f"{summary.get('roi', 0):.2f}% / {summary.get('ad_acos', 0):.2f}%", "净利润 ÷ 总成本 / 广告花费 ÷ 广告销售", ""),
                ]
            ),
            unsafe_allow_html=True,
        )
        tabs = st.tabs(["广告日报", "库存预警", "月度利润"])
        with tabs[0]:
            h, r = _read_excel(OUTPUTS / "operations" / "ad_daily_report.xlsx", "广告日报", ("日期",))
            st.dataframe(_df(h, r).head(120), width="stretch", hide_index=True, height=340)
            _download(OUTPUTS / "operations" / "ad_daily_report.xlsx", "广告日报 Excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with tabs[1]:
            h, r = _read_excel(OUTPUTS / "operations" / "inventory_alert.xlsx", "库存预警", ("SKU",))
            st.dataframe(_df(h, r), width="stretch", hide_index=True, height=300)
            _download(OUTPUTS / "operations" / "inventory_alert.xlsx", "库存预警 Excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with tabs[2]:
            h, r = _read_excel(OUTPUTS / "operations" / "monthly_profit.xlsx", "月度利润", ("SKU",))
            st.dataframe(_df(h, r), width="stretch", hide_index=True, height=320)
            _download(OUTPUTS / "operations" / "monthly_profit.xlsx", "月度利润 Excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("尚未生成经营报表，点击右上角“生成报表”。")


# ---------------------------------------------------------------------------
# interview
# ---------------------------------------------------------------------------
def render_interview() -> None:
    _page_header("面试演示", "<span>生成专属演示脚本，逐模块映射跨境电商岗位 JD 能力点</span>", "面试演示", "生成演示脚本", lambda: run_command("面试演示", ["interview_demo.py", "--run"], timeout=300))
    if INTERVIEW_MD.exists():
        st.markdown(read_text(INTERVIEW_MD)[:20000])
        _download(INTERVIEW_MD, "面试演示脚本", "text/markdown")
    else:
        st.info("尚未生成，点击右上角“生成演示脚本”。脚本包含 JD 能力点、演示顺序、STAR 话术和追问准备。")


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------
def main() -> None:
    page = _sidebar()
    _topbar(page)
    with st.container(key="sheet"):
        renderers = {
            "总览": render_overview,
            "选品研究": render_research,
            "上架素材": render_listing,
            "竞品监控": render_monitor,
            "合规校验": render_compliance,
            "经营报表": render_operations,
            "面试演示": render_interview,
        }
        renderers.get(page, render_overview)()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log_exception(exc, app="streamlit", context={"hook": "app_main"})
        st.error(f"页面异常：{type(exc).__name__}: {exc}")
        st.caption("错误已写入 outputs/logs/errors.log")
````

## `competitor_monitor.py`

````python
#!/usr/bin/env python3
"""竞品公开数据监控模块。

功能：
    - 自定义添加竞品公开商品链接；
    - 按可配置周期（默认 6 小时）巡检；
    - 抓取公开价格、BSR/公开排名、公开差评；
    - 价格/排名超过阈值时生成本地 TXT 预警；
    - 从差评中提取高频痛点并分类输出 Markdown/JSON 报告。

边界：
    - 只读取竞品对外公开的商品页/公开评论页；
    - 不登录、不调用商家后台 API、不使用验证码识别或代理绕过；
    - 公开页面无法访问/结构变化/robots 禁止时跳过该链接并继续；
    - 演示默认使用本地公开快照，真实监控需 --mode live。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

PROJECT_ROOT = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import utils  # noqa: E402

logger = utils.get_logger("competitor_monitor")
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "competitor_monitor.yaml"
DEFAULT_INTERVAL_HOURS = 6.0


class MonitorError(RuntimeError):
    """监控模块异常。"""


class FetchError(MonitorError):
    """公开页面抓取失败。"""


class RobotsDenied(FetchError):
    """robots.txt 禁止抓取。"""


class ParseError(MonitorError):
    """页面结构变化，无法解析商品。"""


# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MonitorConfig:
    root: Path
    path: Path
    data: dict[str, Any]

    def get(self, dotted: str, default: Any = None) -> Any:
        return utils.deep_get(self.data, dotted, default)

    def section(self, name: str) -> dict[str, Any]:
        value = self.get(name, {})
        return dict(value) if isinstance(value, dict) else {}

    def resolve(self, dotted: str) -> Path:
        raw = self.get(dotted)
        if not raw:
            raise MonitorError(f"缺少路径配置: {dotted}")
        path = Path(str(raw)).expanduser()
        return path if path.is_absolute() else (self.root / path).resolve()


def load_config(path: str | Path | None = None, *, root: str | Path | None = None) -> MonitorConfig:
    project_root = Path(root).expanduser().resolve() if root else PROJECT_ROOT
    config_path = Path(path).expanduser() if path else project_root / "config" / "competitor_monitor.yaml"
    if not config_path.is_absolute():
        config_path = (project_root / config_path).resolve()
    data = utils.read_yaml(config_path)
    if not isinstance(data, dict):
        raise MonitorError(f"配置格式错误: {config_path}")
    if not data.get("paths") or not data.get("pain_categories"):
        raise MonitorError("配置缺少 paths 或 pain_categories")
    return MonitorConfig(root=project_root, path=config_path, data=data)


# ---------------------------------------------------------------------------
# 链接识别与注册表
# ---------------------------------------------------------------------------
PLATFORM_LABELS = {
    "amazon": "Amazon",
    "aliexpress": "AliExpress",
    "alibaba_1688": "1688",
    "generic": "Generic",
}
AMAZON_HOSTS = ("amazon.com", "amazon.co.uk", "amazon.de", "amazon.fr", "amazon.ca", "amazon.com.au")


def clean_url(url: str) -> str:
    text = str(url or "").strip()
    if not text:
        raise MonitorError("URL 为空")
    parts = urlsplit(text)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise MonitorError(f"无效 URL（需 http/https）: {url}")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def detect_platform(url: str) -> tuple[str, str]:
    parts = urlsplit(url)
    host = parts.netloc.lower().split("@")[-1].split(":")[0]
    path = parts.path
    if any(host == item or host.endswith("." + item) for item in AMAZON_HOSTS):
        match = re.search(r"/(?:dp|gp/product|product)/([A-Z0-9]{10})", path, re.IGNORECASE)
        return "amazon", match.group(1).upper() if match else ""
    if host.endswith("aliexpress.com"):
        match = re.search(r"/item/(\d+)", path)
        return "aliexpress", match.group(1) if match else ""
    if host.endswith("1688.com"):
        match = re.search(r"/offer/(\d+)", path)
        return "alibaba_1688", match.group(1) if match else ""
    return "generic", ""


def _competitor_id(url: str) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    return f"cmp-{digest}"


def _normalize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    url = clean_url(str(entry.get("url") or ""))
    platform = str(entry.get("platform") or "").lower()
    detected, product_id = detect_platform(url)
    if not platform or platform == "auto":
        platform = detected
    if platform not in PLATFORM_LABELS:
        raise MonitorError(f"不支持的 platform: {platform}")
    return {
        "id": str(entry.get("id") or _competitor_id(url)),
        "name": str(entry.get("name") or f"{PLATFORM_LABELS[platform]} 竞品"),
        "url": url,
        "platform": platform,
        "product_id": str(entry.get("product_id") or product_id),
        "enabled": bool(entry.get("enabled", True)),
        "demo": bool(entry.get("demo", False)),
        "added_at": str(entry.get("added_at") or utils.utc_now_iso()),
        "price_threshold_pct": entry.get("price_threshold_pct"),
        "price_threshold_abs": entry.get("price_threshold_abs"),
        "rank_threshold_abs": entry.get("rank_threshold_abs"),
    }


def load_registry(
    config: MonitorConfig,
    *,
    path: str | Path | None = None,
    create: bool = True,
) -> dict[str, Any]:
    registry_path = Path(path).expanduser().resolve() if path else config.resolve("paths.registry")
    if registry_path.exists():
        payload = utils.read_json(registry_path)
    elif create:
        payload = {
            "notice": "首次运行创建的注册表；demo 条目仅用于离线演示。",
            "competitors": [dict(item) for item in config.get("bootstrap", []) or []],
        }
        utils.write_json(registry_path, payload)
        logger.info("已创建竞品注册表: %s", registry_path)
    else:
        raise MonitorError(f"注册表不存在: {registry_path}")
    entries = payload.get("competitors")
    if not isinstance(entries, list):
        raise MonitorError(f"注册表格式错误: {registry_path}")
    normalized: list[dict[str, Any]] = []
    invalid: list[dict[str, str]] = []
    for item in entries:
        if not isinstance(item, dict):
            invalid.append({"id": "unknown", "error": "注册表条目不是对象"})
            continue
        try:
            normalized.append(_normalize_entry(item))
        except MonitorError as exc:
            invalid.append({"id": str(item.get("id") or item.get("url") or "unknown"), "error": str(exc)})
    payload["competitors"] = normalized
    payload["invalid_entries"] = invalid
    return payload


def save_registry(config: MonitorConfig, payload: dict[str, Any], path: str | Path | None = None) -> Path:
    registry_path = Path(path).expanduser().resolve() if path else config.resolve("paths.registry")
    return utils.write_json(registry_path, payload)


def add_competitor(
    config: MonitorConfig,
    *,
    url: str,
    name: str | None = None,
    platform: str = "auto",
    price_pct: float | None = None,
    price_abs: float | None = None,
    rank_abs: float | None = None,
    registry_path: str | Path | None = None,
) -> dict[str, Any]:
    payload = load_registry(config, path=registry_path)
    clean = clean_url(url)
    if any(item["url"] == clean for item in payload["competitors"]):
        raise MonitorError(f"链接已存在: {clean}")
    entry = _normalize_entry(
        {
            "url": clean,
            "name": name,
            "platform": platform,
            "price_threshold_pct": price_pct,
            "price_threshold_abs": price_abs,
            "rank_threshold_abs": rank_abs,
            "added_at": utils.utc_now_iso(),
            "demo": False,
        }
    )
    payload["competitors"].append(entry)
    save_registry(config, payload, registry_path)
    return entry


def remove_competitor(
    config: MonitorConfig,
    *,
    target: str | None = None,
    all_demo: bool = False,
    registry_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    payload = load_registry(config, path=registry_path)
    removed: list[dict[str, Any]] = []
    kept: list[dict[str, Any]] = []
    for item in payload["competitors"]:
        if all_demo and item.get("demo"):
            removed.append(item)
        elif target and (item["id"] == target or item["url"] == target):
            removed.append(item)
        else:
            kept.append(item)
    if not removed:
        raise MonitorError("没有匹配的竞品可删除")
    payload["competitors"] = kept
    save_registry(config, payload, registry_path)
    return removed


# ---------------------------------------------------------------------------
# 公开页面抓取
# ---------------------------------------------------------------------------
class PublicFetcher:
    def __init__(self, config: MonitorConfig) -> None:
        crawler = config.section("crawler")
        monitor = config.section("monitor")
        self.user_agent = str(crawler.get("user_agent", "OutdoorEssMonitor/0.1"))
        self.accept_language = str(crawler.get("accept_language", "en-US,en;q=0.9"))
        self.timeout = float(monitor.get("timeout_seconds", 20))
        self.delay = max(0.0, float(monitor.get("request_delay_seconds", 2.0)))
        self.respect_robots = bool(monitor.get("respect_robots", True))
        self._robots: dict[str, bool] = {}
        self._last: dict[str, float] = {}
        self._requests: Any = None
        self._session: Any = None

    def _session_or_raise(self) -> Any:
        if self._requests is None:
            try:
                import requests as _requests
            except ImportError as exc:  # pragma: no cover
                raise FetchError("live 模式需要 requests：pip install requests") from exc
            self._requests = _requests
            self._session = _requests.Session()
            self._session.headers.update(
                {
                    "User-Agent": self.user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": self.accept_language,
                }
            )
        return self._session

    def _robots_allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin in self._robots:
            return self._robots[origin]
        robots_url = f"{origin}/robots.txt"
        try:
            response = self._session_or_raise().get(robots_url, timeout=self.timeout)
        except Exception as exc:
            raise FetchError(f"读取 robots.txt 失败: {robots_url}: {exc}") from exc
        if response.status_code == 404:
            allowed = True
        elif response.status_code in {401, 403}:
            allowed = False
        elif not 200 <= response.status_code < 300:
            allowed = False
        else:
            parser = RobotFileParser()
            parser.set_url(robots_url)
            parser.parse(response.text.splitlines())
            allowed = parser.can_fetch(self.user_agent, url)
        self._robots[origin] = allowed
        return allowed

    def get(self, url: str) -> str:
        if not self._robots_allowed(url):
            raise RobotsDenied(f"robots.txt 禁止抓取，已跳过: {url}")
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        wait = self.delay - (time.monotonic() - self._last.get(origin, 0.0))
        if wait > 0:
            time.sleep(wait)
        try:
            response = self._session_or_raise().get(url, timeout=self.timeout, allow_redirects=True)
        except Exception as exc:
            raise FetchError(f"请求失败: {url}: {exc}") from exc
        self._last[origin] = time.monotonic()
        if response.status_code in {401, 403, 429, 503}:
            raise FetchError(f"公开页面拒绝访问（HTTP {response.status_code}），不绕过: {url}")
        if response.status_code >= 400:
            raise FetchError(f"HTTP {response.status_code}: {url}")
        text = response.text or ""
        lowered = text[:5000].lower()
        if "captcha" in lowered or "robot check" in lowered or "verify you are human" in lowered:
            raise FetchError(f"页面要求验证码/人机校验，已跳过: {url}")
        return text

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None


def _soup(html: str) -> Any:
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:  # pragma: no cover
        raise FetchError("live 模式需要 beautifulsoup4：pip install beautifulsoup4") from exc
    return BeautifulSoup(html, "html.parser")


def _num(value: Any, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(value))
    return float(match.group(0).replace(",", "")) if match else default


def _int(value: Any, default: int = 0) -> int:
    parsed = _num(value)
    return int(round(parsed)) if parsed is not None else default


# ---------------------------------------------------------------------------
# 公开商品页解析
# ---------------------------------------------------------------------------
def _first_text(soup: Any, selectors: Iterable[str]) -> str:
    for selector in selectors:
        node = soup.select_one(selector)
        if node:
            text = node.get_text(" ", strip=True)
            if text:
                return text
    return ""


def _walk_jsonld(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        types = value.get("@type")
        if types == "Product" or (isinstance(types, list) and "Product" in types):
            yield value
        for child in value.values():
            yield from _walk_jsonld(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_jsonld(child)


def _jsonld_product(soup: Any) -> dict[str, Any]:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            payload = json.loads(script.string or script.get_text() or "")
        except (TypeError, ValueError):
            continue
        for item in _walk_jsonld(payload):
            return item
    return {}


def _currency_for(url: str, platform: str, default: str = "USD") -> str:
    host = urlsplit(url).netloc.lower()
    if platform == "alibaba_1688" or "1688.com" in host:
        return "CNY"
    if "amazon.co.uk" in host or ".co.uk" in host:
        return "GBP"
    if "amazon.de" in host or "amazon.fr" in host or ".de" in host or ".fr" in host:
        return "EUR"
    return default


def _price_from_html(soup: Any, url: str, platform: str) -> tuple[float | None, str]:
    product = _jsonld_product(soup)
    offers = product.get("offers") if product else None
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    if isinstance(offers, dict):
        price = _num(offers.get("price", offers.get("lowPrice")))
        if price and price > 0:
            return price, str(offers.get("priceCurrency") or _currency_for(url, platform)).upper()
    for meta in soup.find_all("meta"):
        prop = str(meta.get("property") or meta.get("name") or "").lower()
        if prop in {"product:price:amount", "og:price:amount"}:
            price = _num(meta.get("content"))
            if price and price > 0:
                currency_meta = soup.find("meta", attrs={"property": "product:price:currency"})
                currency = str(currency_meta.get("content") if currency_meta else _currency_for(url, platform)).upper()
                return price, currency
    selectors = (
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        ".a-price .a-offscreen",
        "span.price",
        "[class*='price-current']",
        "[class*='product-price']",
        "[class*='price']",
    )
    for selector in selectors:
        node = soup.select_one(selector)
        if node:
            price = _num(node.get_text(" ", strip=True))
            if price and price > 0:
                return price, _currency_for(url, platform)
    return None, _currency_for(url, platform)


def _bsr_from_html(soup: Any) -> tuple[int | None, str]:
    text = soup.get_text(" ", strip=True)
    patterns = (
        r"Best Sellers Rank:?\s*#?([\d,]+)\s+in\s+([^#<()]{2,100})",
        r"#([\d,]+)\s+in\s+([A-Za-z][^#<()]{2,100})",
        r"排名第?\s*([\d,]+)\s*名",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            bsr = _int(match.group(1))
            category = re.sub(r"\s+", " ", match.group(2)).strip(" :-,")
            return bsr, category
    return None, ""


def _review_from_node(node: Any) -> dict[str, Any] | None:
    text = node.get_text(" ", strip=True)
    if len(text) < 8:
        return None
    rating_text = _first_text(
        node,
        ("span.a-icon-alt", "[class*='star']", "[class*='rating']", "[data-hook*='rating']"),
    )
    rating_match = re.search(r"([1-5](?:\.\d)?)", rating_text) if rating_text else None
    title = _first_text(node, ("[data-hook='review-title']", "[class*='title']"))
    body = _first_text(
        node,
        (
            "[data-hook='review-body']",
            "[class*='review-content']",
            "[class*='reviewContent']",
            "[class*='content']",
            "[class*='body']",
        ),
    )
    if not body:
        body = text
    return {
        "rating": int(float(rating_match.group(1))) if rating_match else None,
        "title": re.sub(r"\s+", " ", title).strip()[:200],
        "body": re.sub(r"\s+", " ", body).strip()[:1500],
        "date": _first_text(node, ("[data-hook='review-date']", "[class*='date']")),
        "author": _first_text(node, ("[class*='author']", "[class*='user']", "[class*='profile']")),
    }


def _reviews_from_html(soup: Any) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    product = _jsonld_product(soup)
    raw_reviews = product.get("review") if product else None
    if isinstance(raw_reviews, dict):
        raw_reviews = [raw_reviews]
    if isinstance(raw_reviews, list):
        for item in raw_reviews:
            if not isinstance(item, dict):
                continue
            rating = item.get("reviewRating") or {}
            author = item.get("author") or {}
            reviews.append(
                {
                    "rating": _int(rating.get("ratingValue")) if isinstance(rating, dict) else None,
                    "title": str(item.get("name") or ""),
                    "body": str(item.get("reviewBody") or ""),
                    "date": str(item.get("datePublished") or ""),
                    "author": str(author.get("name") or "") if isinstance(author, dict) else "",
                }
            )
    selectors = (
        "[data-hook='review']",
        "div.review",
        "[class*='review-item']",
        "[class*='reviewItem']",
        "[class*='comment-item']",
        "[class*='commentItem']",
        "[class*='offer-review']",
    )
    for selector in selectors:
        for node in soup.select(selector):
            parsed = _review_from_node(node)
            if parsed:
                reviews.append(parsed)
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for review in reviews:
        key = (str(review.get("body") or "") + str(review.get("title") or "")).lower()[:300]
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(review)
    return deduped


class ProductParser:
    """Amazon / AliExpress / 1688 / Generic 公开商品页解析器。"""

    def parse(
        self,
        *,
        url: str,
        platform: str,
        html: str,
        review_html: str | None = None,
    ) -> dict[str, Any]:
        soup = _soup(html)
        product = _jsonld_product(soup)
        title = _first_text(
            soup,
            ("#productTitle", "h1[itemprop='name']", "h1", "meta[property='og:title']"),
        )
        if not title and product:
            title = str(product.get("name") or "")
        if not title:
            meta = soup.find("meta", attrs={"property": "og:title"})
            title = str(meta.get("content") if meta else "").strip()
        title = re.sub(r"\s+", " ", title).strip()[:300]
        price, currency = _price_from_html(soup, url, platform)
        bsr, bsr_category = _bsr_from_html(soup)
        rating = None
        review_count = 0
        if product:
            aggregate = product.get("aggregateRating") or {}
            if isinstance(aggregate, dict):
                rating = _num(aggregate.get("ratingValue"))
                review_count = _int(aggregate.get("reviewCount") or aggregate.get("ratingCount"))
        if rating is None:
            rating_text = _first_text(soup, ("span.a-icon-alt", "[class*='rating']", "[class*='star']"))
            rating = _num(rating_text)
        reviews = _reviews_from_html(soup)
        if review_html:
            review_soup = _soup(review_html)
            reviews.extend(_reviews_from_html(review_soup))
        # 去重并保留有实际内容的评论
        deduped: list[dict[str, Any]] = []
        seen: set[str] = set()
        for review in reviews:
            body = re.sub(r"\s+", " ", str(review.get("body") or "")).strip()
            if len(body) < 8:
                continue
            key = body.lower()[:300]
            if key in seen:
                continue
            seen.add(key)
            review["body"] = body[:1500]
            deduped.append(review)
        if price is None and bsr is None:
            raise ParseError("公开页面未解析到价格或 BSR，可能页面结构变化/需要登录")
        if review_count <= 0:
            review_count = len(deduped)
        return {
            "title": title or "(untitled public listing)",
            "price": price,
            "currency": currency,
            "bsr": bsr,
            "bsr_category": bsr_category,
            "rating": round(rating, 2) if rating is not None else None,
            "review_count": review_count,
            "reviews": deduped,
            "source_url": url,
            "platform": platform,
            "captured_at": utils.utc_now_iso(),
        }


def _load_fixture(path: Path) -> dict[str, Any]:
    payload = utils.read_json(path)
    if not isinstance(payload, dict) or not isinstance(payload.get("snapshots"), dict):
        raise MonitorError(f"公开快照格式错误: {path}")
    return payload


def _fixture_snapshot(fixture: dict[str, Any], competitor_id: str) -> dict[str, Any]:
    item = fixture["snapshots"].get(competitor_id)
    if not isinstance(item, dict):
        raise ParseError(f"离线快照不包含该竞品: {competitor_id}")
    snapshot = dict(item)
    snapshot.setdefault("source_url", "")
    snapshot.setdefault("platform", "")
    snapshot.setdefault("captured_at", fixture.get("captured_at") or utils.utc_now_iso())
    snapshot.setdefault("reviews", [])
    return snapshot


def collect_snapshot(
    competitor: dict[str, Any],
    config: MonitorConfig,
    *,
    mode: str,
    fixture_path: str | Path | None = None,
    fetcher: PublicFetcher | None = None,
) -> dict[str, Any]:
    mode = mode.lower()
    if mode == "live" and competitor.get("demo"):
        raise FetchError("demo 条目在 live 模式自动跳过；请 add 真实公开链接")
    fixture_file = Path(fixture_path).expanduser().resolve() if fixture_path else config.resolve("fixture.path")
    if mode == "offline":
        return _fixture_snapshot(_load_fixture(fixture_file), competitor["id"])
    if mode == "live":
        return _collect_live(competitor, config, fetcher or PublicFetcher(config))
    if mode == "auto":
        if competitor.get("demo"):
            return _fixture_snapshot(_load_fixture(fixture_file), competitor["id"])
        try:
            return _collect_live(competitor, config, fetcher or PublicFetcher(config))
        except (FetchError, ParseError) as exc:
            logger.warning("live 失败，尝试离线快照：%s：%s", competitor["id"], exc)
            return _fixture_snapshot(_load_fixture(fixture_file), competitor["id"])
    raise MonitorError(f"未知 mode: {mode}")


def _collect_live(
    competitor: dict[str, Any],
    config: MonitorConfig,
    fetcher: PublicFetcher,
) -> dict[str, Any]:
    parser = ProductParser()
    url = competitor["url"]
    html = fetcher.get(url)
    review_html: str | None = None
    if competitor["platform"] == "amazon":
        asin = competitor.get("product_id") or ""
        if asin:
            review_url = f"https://{urlsplit(url).netloc}/product-reviews/{asin}?filterByStar=critical&pageNumber=1"
            try:
                review_html = fetcher.get(review_url)
            except FetchError as exc:
                logger.warning("公开评论页不可用，仅使用商品页评论：%s：%s", competitor["id"], exc)
    snapshot = parser.parse(url=url, platform=competitor["platform"], html=html, review_html=review_html)
    snapshot["source_url"] = url
    snapshot["platform"] = competitor["platform"]
    max_reviews = int(config.get("monitor.max_reviews_per_competitor", 20))
    snapshot["reviews"] = snapshot.get("reviews", [])[:max_reviews]
    return snapshot


# ---------------------------------------------------------------------------
# 状态、快照与预警
# ---------------------------------------------------------------------------
@dataclass
class Alert:
    competitor_id: str
    competitor_name: str
    url: str
    platform: str
    kind: str
    message: str
    old_value: Any
    new_value: Any
    delta: Any
    captured_at: str


def _price_threshold(competitor: dict[str, Any], config: MonitorConfig, key: str, default: float) -> float:
    value = competitor.get(key)
    return float(value) if value not in (None, "") else float(config.get(f"monitor.{key}", default))


def detect_alerts(
    competitor: dict[str, Any],
    previous: dict[str, Any] | None,
    current: dict[str, Any],
    config: MonitorConfig,
) -> list[Alert]:
    if not previous:
        return []
    alerts: list[Alert] = []
    old_price = _num(previous.get("price"))
    new_price = _num(current.get("price"))
    if old_price and new_price and previous.get("currency") == current.get("currency"):
        pct = abs(new_price - old_price) / old_price * 100
        pct_threshold = _price_threshold(competitor, config, "price_threshold_pct", 3.0)
        abs_threshold = _price_threshold(competitor, config, "price_threshold_abs", 5.0)
        if pct >= pct_threshold or abs(new_price - old_price) >= abs_threshold:
            direction = "下降" if new_price < old_price else "上涨"
            alerts.append(
                Alert(
                    competitor_id=competitor["id"],
                    competitor_name=competitor["name"],
                    url=competitor["url"],
                    platform=competitor["platform"],
                    kind="PRICE",
                    message=(
                        f"价格{direction}：{current.get('currency', '')} {old_price:.2f} → "
                        f"{new_price:.2f}（{pct:.2f}%）"
                    ),
                    old_value=old_price,
                    new_value=new_price,
                    delta=round(new_price - old_price, 2),
                    captured_at=str(current.get("captured_at") or utils.utc_now_iso()),
                )
            )
    old_rank = _int(previous.get("bsr"), 0)
    new_rank = _int(current.get("bsr"), 0)
    if old_rank and new_rank and previous.get("bsr_category") == current.get("bsr_category"):
        delta = old_rank - new_rank
        threshold = _price_threshold(competitor, config, "rank_threshold_abs", 20.0)
        if abs(delta) >= threshold:
            direction = "改善" if delta > 0 else "下滑"
            alerts.append(
                Alert(
                    competitor_id=competitor["id"],
                    competitor_name=competitor["name"],
                    url=competitor["url"],
                    platform=competitor["platform"],
                    kind="BSR",
                    message=(
                        f"BSR {direction}：#{old_rank:,} → #{new_rank:,}"
                        f"（变化 {abs(delta):,} 位，类目：{current.get('bsr_category') or '-'}）"
                    ),
                    old_value=old_rank,
                    new_value=new_rank,
                    delta=delta,
                    captured_at=str(current.get("captured_at") or utils.utc_now_iso()),
                )
            )
    return alerts


class StateStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = {"competitors": {}}
        if path.exists():
            loaded = utils.read_json(path, default={})
            if isinstance(loaded, dict):
                self.data = loaded
                self.data.setdefault("competitors", {})

    def previous(self, competitor_id: str) -> dict[str, Any] | None:
        value = self.data["competitors"].get(competitor_id)
        return dict(value) if isinstance(value, dict) else None

    def update(self, competitor_id: str, snapshot: dict[str, Any]) -> None:
        previous = self.previous(competitor_id) or {}
        previous.update(
            {
                "title": snapshot.get("title") or previous.get("title"),
                "price": snapshot.get("price") if snapshot.get("price") is not None else previous.get("price"),
                "currency": snapshot.get("currency") or previous.get("currency"),
                "bsr": snapshot.get("bsr") if snapshot.get("bsr") is not None else previous.get("bsr"),
                "bsr_category": snapshot.get("bsr_category") or previous.get("bsr_category"),
                "rating": snapshot.get("rating") if snapshot.get("rating") is not None else previous.get("rating"),
                "review_count": snapshot.get("review_count")
                if snapshot.get("review_count") is not None
                else previous.get("review_count"),
                "last_seen": snapshot.get("captured_at") or utils.utc_now_iso(),
            }
        )
        self.data["competitors"][competitor_id] = previous

    def save(self) -> Path:
        return utils.write_json(self.path, self.data)


def write_alerts(
    alerts: list[Alert],
    output_dir: Path,
    run_id: str,
    *,
    warning_text: str = "",
) -> list[Path]:
    alert_dir = utils.ensure_dir(output_dir)
    paths: list[Path] = []
    for alert in alerts:
        slug = utils.safe_filename(f"{alert.competitor_id}_{alert.kind}_{run_id}")
        path = alert_dir / f"{slug}.txt"
        content = (
            "[竞品监控预警]\n"
            f"生成时间：{utils.utc_now_iso()}\n"
            f"竞品名称：{alert.competitor_name}\n"
            f"竞品 ID：{alert.competitor_id}\n"
            f"平台：{alert.platform}\n"
            f"链接：{alert.url}\n"
            f"预警类型：{alert.kind}\n"
            f"变动：{alert.message}\n"
            f"旧值：{alert.old_value}\n"
            f"新值：{alert.new_value}\n"
            f"数据时间：{alert.captured_at}\n"
            "备注：仅基于公开页面数据，需人工复核价格口径/排名类目。\n"
        )
        utils.write_text(path, content)
        paths.append(path)
    latest = alert_dir / "latest_alerts.txt"
    if alerts:
        blocks = [
            (
                f"[{item.kind}] {item.competitor_name}\n"
                f"URL: {item.url}\n"
                f"{item.message}\n"
                f"数据时间: {item.captured_at}\n"
            )
            for item in alerts
        ]
        body = f"竞品监控预警汇总 / {utils.utc_now_iso()}\n\n" + "\n".join(blocks)
    else:
        body = f"竞品监控预警汇总 / {utils.utc_now_iso()}\n\n本轮无价格/排名预警。\n"
    if warning_text:
        body += f"\n{warning_text}\n"
    utils.write_text(latest, body)
    return paths


# ---------------------------------------------------------------------------
# 差评痛点分析
# ---------------------------------------------------------------------------
class PainPointAnalyzer:
    def __init__(self, config: MonitorConfig) -> None:
        self.config = config
        self.threshold = int(config.get("monitor.negative_rating_threshold", 2))
        self.max_examples = int(config.get("monitor.max_pain_examples", 3))
        self.categories = [
            item
            for item in (config.get("pain_categories", []) or [])
            if isinstance(item, dict) and item.get("id")
        ]
        self.stopwords = {str(x).lower() for x in (config.get("stopwords", []) or [])}

    def analyze(
        self,
        reviews: list[dict[str, Any]],
        competitors: list[dict[str, Any]],
        *,
        run_id: str,
        failures: list[dict[str, str]],
    ) -> dict[str, Any]:
        negatives = [
            review
            for review in reviews
            if review.get("rating") is not None and int(review["rating"]) <= self.threshold
        ]
        category_hits: dict[str, list[dict[str, Any]]] = defaultdict(list)
        per_competitor: dict[str, dict[str, Any]] = {
            item["id"]: {"id": item["id"], "name": item["name"], "negative_reviews": 0, "categories": Counter()}
            for item in competitors
        }
        for review in negatives:
            text = f"{review.get('title', '')} {review.get('body', '')}".lower()
            matched = [
                str(category["id"])
                for category in self.categories
                if any(self._match(keyword, text) for keyword in category.get("keywords", []))
            ]
            if not matched:
                matched = ["other"]
            for category_id in matched:
                category_hits[category_id].append(review)
            competitor = per_competitor.get(str(review.get("competitor_id")))
            if competitor:
                competitor["negative_reviews"] += 1
                competitor["categories"].update(matched)

        labels = {str(item["id"]): str(item.get("label") or item["id"]) for item in self.categories}
        labels["other"] = "其他/未分类"
        category_stats: list[dict[str, Any]] = []
        for category_id, items in category_hits.items():
            names = sorted({str(item.get("competitor_name") or item.get("competitor_id")) for item in items})
            category_stats.append(
                {
                    "id": category_id,
                    "label": labels.get(category_id, category_id),
                    "mentions": len(items),
                    "share_pct": round(len(items) / len(negatives) * 100, 2) if negatives else 0.0,
                    "competitors": names,
                    "examples": [
                        {
                            "competitor": item.get("competitor_name") or item.get("competitor_id"),
                            "rating": item.get("rating"),
                            "quote": self._quote(str(item.get("body") or item.get("title") or "")),
                        }
                        for item in items[: self.max_examples]
                    ],
                }
            )
        category_stats.sort(key=lambda item: (-item["mentions"], item["label"]))
        competitor_rows = []
        for item in per_competitor.values():
            competitor_rows.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "negative_reviews": item["negative_reviews"],
                    "top_categories": [
                        {"id": key, "label": labels.get(key, key), "mentions": value}
                        for key, value in item["categories"].most_common(3)
                    ],
                }
            )
        competitor_rows.sort(key=lambda item: -item["negative_reviews"])
        top_terms = self._top_terms(negatives)
        report = {
            "run_id": run_id,
            "generated_at": utils.utc_now_iso(),
            "policy": "只分析公开可见差评；样本非全量，不代表真实整体满意度。",
            "total_reviews": len(reviews),
            "negative_reviews": len(negatives),
            "negative_rating_threshold": self.threshold,
            "categories": category_stats,
            "per_competitor": competitor_rows,
            "top_terms": top_terms,
            "failures": failures,
            "recommendations": [self._action(item["id"]) for item in category_stats[:3]],
        }
        report["markdown"] = self._markdown(report)
        return report

    @staticmethod
    def _match(keyword: str, text: str) -> bool:
        phrase = str(keyword).strip().lower()
        if not phrase:
            return False
        return bool(re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", text))

    def _top_terms(self, reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
        counter: Counter[str] = Counter()
        for review in reviews:
            text = f"{review.get('title', '')} {review.get('body', '')}".lower()
            for token in re.findall(r"[a-z][a-z'-]{3,}", text):
                token = token.strip("'-")
                if token and token not in self.stopwords:
                    counter[token] += 1
        return [{"term": term, "count": count} for term, count in counter.most_common(15)]

    def _quote(self, text: str) -> str:
        max_chars = int(self.config.get("monitor.max_alert_quote_chars", 300))
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars] + ("…" if len(text) > max_chars else "")

    def _action(self, category_id: str) -> str:
        mapping = {
            "battery_life": "在详情页明确可用容量、测试负载与续航条件，并优化电芯/逆变效率。",
            "charging_speed": "标注充电功率与 0-80% 时间，提供快充配件与清晰说明。",
            "solar_charging": "标注太阳能输入上限、MPPT 方案与真实日照条件，避免固定时长承诺。",
            "noise": "优化风扇曲线与低噪模式，标注测试距离和负载条件。",
            "power_output": "明确持续/峰值功率与兼容设备，增加过载保护说明。",
            "weight_portability": "强化单人搬运与后备箱场景，提供拉杆包/折叠车等配件。",
            "build_quality": "加强外壳、接口与包装质检，补充跌落/老化测试说明。",
            "display_app": "校准电量显示与 App 连接，提供固件更新与重置指引。",
            "heat_safety": "完善热管理与温控说明，避免长时间满载，明确安全边界。",
            "shipping_packaging": "加固包装与电池运输标签，明确发货时效。",
            "customer_service": "建立响应 SLA、保修与退换流程，缩短首次回复时间。",
            "instructions": "重做快速上手卡/视频，覆盖首次充电、接口与过载处理。",
            "compatibility": "提供插头、接口与设备功率兼容表，减少误购。",
            "value_price": "用每 Wh 成本、循环寿命与质保解释价值，而非单纯低价。",
            "other": "抽取更多负评样本并人工复核，补充细分类别。",
        }
        return mapping.get(category_id, "人工复核该类别的高频负评并制定改进动作。")

    def _markdown(self, report: dict[str, Any]) -> str:
        lines = [
            "# 竞品公开差评痛点分析报告",
            "",
            f"- 运行 ID：`{report['run_id']}`",
            f"- 生成时间：{report['generated_at']}",
            f"- 公开评论样本：{report['total_reviews']} 条",
            f"- 差评样本（≤{report['negative_rating_threshold']} 星）：{report['negative_reviews']} 条",
            "- 数据边界：仅公开页面；样本非全量，不代表整体满意度。",
            "",
            "## 1. 高频痛点总览",
            "",
            "| 排名 | 痛点分类 | 提及次数 | 占差评比例 | 涉及竞品 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for index, item in enumerate(report["categories"], start=1):
            lines.append(
                f"| {index} | {item['label']} | {item['mentions']} | {item['share_pct']:.1f}% | "
                f"{'、'.join(item['competitors']) or '-'} |"
            )
        lines.extend(["", "## 2. 分类样例", ""])
        for item in report["categories"]:
            lines.append(f"### {item['label']}（{item['mentions']} 次）")
            for example in item["examples"]:
                lines.append(
                    f"- [{example['competitor']} / {example['rating']}★] “{example['quote']}”"
                )
            lines.append("")
        lines.extend(
            [
                "## 3. 竞品对比",
                "",
                "| 竞品 | 差评数 | Top 痛点 |",
                "| --- | --- | --- |",
            ]
        )
        for item in report["per_competitor"]:
            top = "；".join(
                f"{entry['label']} {entry['mentions']}" for entry in item["top_categories"]
            ) or "-"
            lines.append(f"| {item['name']} | {item['negative_reviews']} | {top} |")
        lines.extend(
            [
                "",
                "## 4. 高频词",
                "",
                "、".join(f"{item['term']}({item['count']})" for item in report["top_terms"]) or "-",
                "",
                "## 5. 建议动作",
                "",
            ]
        )
        lines.extend(f"{index}. {action}" for index, action in enumerate(report["recommendations"], start=1))
        if report["failures"]:
            lines.extend(["", "## 6. 抓取失败/跳过", ""])
            for failure in report["failures"]:
                lines.append(f"- `{failure.get('id')}`：{failure.get('error')}")
        lines.extend(
            [
                "",
                "---",
                "",
                "*本报告由公开数据规则分析生成，不构成法律、认证或商业决策结论。*",
                "",
            ]
        )
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 监控引擎
# ---------------------------------------------------------------------------
def _display_path(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


class MonitorEngine:
    def __init__(
        self,
        config: MonitorConfig,
        *,
        registry_path: str | Path | None = None,
        state_path: str | Path | None = None,
        output_dir: str | Path | None = None,
        fixture_path: str | Path | None = None,
    ) -> None:
        self.config = config
        self.registry_path = Path(registry_path).expanduser().resolve() if registry_path else config.resolve("paths.registry")
        self.state_path = Path(state_path).expanduser().resolve() if state_path else config.resolve("paths.state")
        self.fixture_path = str(fixture_path) if fixture_path else None
        if output_dir:
            base = Path(output_dir).expanduser().resolve()
            self.snapshots_dir = utils.ensure_dir(base / "snapshots")
            self.alerts_dir = utils.ensure_dir(base / "alerts")
            self.reports_dir = utils.ensure_dir(base / "reports")
            self.output_base = base
        else:
            self.snapshots_dir = utils.ensure_dir(config.resolve("paths.snapshots_dir"))
            self.alerts_dir = utils.ensure_dir(config.resolve("paths.alerts_dir"))
            self.reports_dir = utils.ensure_dir(config.resolve("paths.reports_dir"))
            self.output_base = self.reports_dir.parent
        self.analyzer = PainPointAnalyzer(config)

    def run(self, *, mode: str | None = None, fixture_path: str | Path | None = None) -> dict[str, Any]:
        selected_mode = str(mode or self.config.get("monitor.mode", "offline")).lower()
        registry = load_registry(self.config, path=self.registry_path)
        state = StateStore(self.state_path)
        run_id = f"monitor_{utils.utc_now().strftime('%Y%m%d_%H%M%S_%f')}"
        generated_at = utils.utc_now_iso()
        failures: list[dict[str, str]] = []
        results: list[dict[str, Any]] = []
        reviews: list[dict[str, Any]] = []
        pending_alerts: list[Alert] = []
        selected_fixture = str(fixture_path) if fixture_path else self.fixture_path
        fetcher = PublicFetcher(self.config) if selected_mode in {"live", "auto"} else None

        for bad in registry.get("invalid_entries", []):
            failures.append(
                {
                    "id": str(bad.get("id")),
                    "name": "-",
                    "url": "",
                    "error": f"注册表条目无效：{bad.get('error')}",
                }
            )

        try:
            for competitor in registry["competitors"]:
                if not competitor.get("enabled", True):
                    continue
                try:
                    clean_url(competitor["url"])
                    snapshot = collect_snapshot(
                        competitor,
                        self.config,
                        mode=selected_mode,
                        fixture_path=selected_fixture,
                        fetcher=fetcher,
                    )
                    snapshot["competitor_id"] = competitor["id"]
                    snapshot["competitor_name"] = competitor["name"]
                    snapshot["source_url"] = snapshot.get("source_url") or competitor["url"]
                    snapshot["platform"] = snapshot.get("platform") or competitor["platform"]
                    snapshot["captured_at"] = snapshot.get("captured_at") or generated_at
                    previous = state.previous(competitor["id"])
                    alerts = detect_alerts(competitor, previous, snapshot, self.config)
                    pending_alerts.extend(alerts)
                    state.update(competitor["id"], snapshot)

                    for review in snapshot.get("reviews", []):
                        item = dict(review)
                        item["competitor_id"] = competitor["id"]
                        item["competitor_name"] = competitor["name"]
                        item["platform"] = competitor["platform"]
                        item["source_url"] = competitor["url"]
                        reviews.append(item)

                    snapshot_path = utils.write_json(
                        self.snapshots_dir / run_id / f"{utils.safe_filename(competitor['id'])}.json",
                        snapshot,
                    )
                    utils.write_json(
                        self.snapshots_dir / f"latest_{utils.safe_filename(competitor['id'])}.json",
                        snapshot,
                    )
                    results.append(
                        {
                            "id": competitor["id"],
                            "name": competitor["name"],
                            "url": competitor["url"],
                            "platform": competitor["platform"],
                            "status": "success",
                            "price": snapshot.get("price"),
                            "currency": snapshot.get("currency"),
                            "bsr": snapshot.get("bsr"),
                            "bsr_category": snapshot.get("bsr_category"),
                            "rating": snapshot.get("rating"),
                            "review_count": snapshot.get("review_count"),
                            "negative_reviews": sum(
                                1
                                for review in snapshot.get("reviews", [])
                                if review.get("rating") is not None
                                and int(review["rating"]) <= self.analyzer.threshold
                            ),
                            "alert_count": len(alerts),
                            "snapshot": _display_path(self.config.root, snapshot_path),
                        }
                    )
                    logger.info(
                        "竞品巡检成功: %s / 价格=%s %s / BSR=%s / 预警=%d",
                        competitor["name"],
                        snapshot.get("price"),
                        snapshot.get("currency"),
                        snapshot.get("bsr"),
                        len(alerts),
                    )
                except Exception as exc:  # 单个链接失败不影响其他链接
                    logger.warning("竞品巡检跳过: %s：%s", competitor.get("name"), exc)
                    failures.append(
                        {
                            "id": competitor.get("id", "unknown"),
                            "name": competitor.get("name", "-"),
                            "url": competitor.get("url", ""),
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
        finally:
            if fetcher is not None:
                fetcher.close()

        warning = ""
        if failures:
            warning = f"本轮失败/跳过 {len(failures)} 个链接，详情见报告。"
        alert_paths = write_alerts(pending_alerts, self.alerts_dir, run_id, warning_text=warning)
        state.save()

        report = self.analyzer.analyze(
            reviews,
            registry["competitors"],
            run_id=run_id,
            failures=failures,
        )
        report_md = self.reports_dir / f"pain_points_{run_id}.md"
        report_json = self.reports_dir / f"pain_points_{run_id}.json"
        utils.write_text(report_md, report["markdown"])
        utils.write_json(report_json, report)
        utils.write_text(self.reports_dir / "latest_pain_points.md", report["markdown"])
        utils.write_json(
            self.reports_dir / "latest_pain_points.json",
            {key: value for key, value in report.items() if key != "markdown"},
        )

        summary = {
            "run_id": run_id,
            "generated_at": generated_at,
            "mode": selected_mode,
            "registry": _display_path(self.config.root, self.registry_path),
            "counts": {
                "competitors": len(registry["competitors"]),
                "success": len(results),
                "failed": len(failures),
                "alerts": len(pending_alerts),
                "reviews": len(reviews),
                "negative_reviews": report["negative_reviews"],
            },
            "results": results,
            "failures": failures,
            "report": _display_path(self.config.root, report_md),
            "latest_report": _display_path(self.config.root, self.reports_dir / "latest_pain_points.md"),
            "latest_alerts": _display_path(self.config.root, self.alerts_dir / "latest_alerts.txt"),
            "alert_files": [_display_path(self.config.root, path) for path in alert_paths],
            "state": _display_path(self.config.root, self.state_path),
            "notice": "仅使用公开商品页/公开评论页；失败链接已跳过，不影响其他竞品。",
        }
        summary_path = utils.write_json(self.reports_dir / "monitor_summary.json", summary)
        summary["summary"] = _display_path(self.config.root, summary_path)
        logger.info(
            "巡检完成: 成功 %d / 失败 %d / 预警 %d / 差评 %d",
            len(results),
            len(failures),
            len(pending_alerts),
            report["negative_reviews"],
        )
        return summary


def validate_interval(interval_hours: float) -> float:
    if interval_hours <= 0:
        raise MonitorError("巡检间隔必须大于 0 小时")
    return interval_hours


def run_schedule(
    engine: MonitorEngine,
    *,
    interval_hours: float = DEFAULT_INTERVAL_HOURS,
    max_cycles: int | None = None,
    mode: str | None = None,
    sleeper: Any = time.sleep,
) -> int:
    interval_seconds = validate_interval(interval_hours) * 3600
    cycles = 0
    while True:
        cycles += 1
        started = time.monotonic()
        logger.info("开始第 %d 轮巡检（间隔 %.2f 小时）", cycles, interval_hours)
        try:
            engine.run(mode=mode)
        except Exception as exc:  # 调度循环不因单轮异常退出
            logger.exception("第 %d 轮巡检异常，继续等待下一轮: %s", cycles, exc)
        if max_cycles is not None and cycles >= max_cycles:
            break
        # 按开始到开始的固定节拍等待，扣除本轮执行耗时
        remaining = interval_seconds - (time.monotonic() - started)
        try:
            sleeper(max(0.0, remaining))
        except KeyboardInterrupt:
            logger.info("收到中断，停止定时巡检")
            break
    return cycles


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="competitor_monitor",
        description="竞品公开商品页监控：价格/BSR/差评/痛点/预警",
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="监控配置")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="添加竞品公开链接")
    add.add_argument("url")
    add.add_argument("--name")
    add.add_argument("--platform", default="auto", choices=["auto", "amazon", "aliexpress", "alibaba_1688", "generic"])
    add.add_argument("--price-pct", type=float, help="价格变动百分比阈值")
    add.add_argument("--price-abs", type=float, help="价格变动绝对阈值")
    add.add_argument("--rank-abs", type=float, help="BSR 变动绝对阈值")
    add.add_argument("--registry")

    listing = sub.add_parser("list", help="列出竞品")
    listing.add_argument("--registry")

    remove = sub.add_parser("remove", help="删除竞品")
    remove.add_argument("target", nargs="?", help="竞品 ID 或 URL")
    remove.add_argument("--all-demo", action="store_true", help="删除所有 demo 条目")
    remove.add_argument("--registry")

    run = sub.add_parser("run", help="执行一轮巡检")
    run.add_argument("--mode", choices=["offline", "live", "auto"])
    run.add_argument("--fixture", help="离线快照路径")
    run.add_argument("--registry")
    run.add_argument("--state")
    run.add_argument("--output-dir")
    run.add_argument("--log-level", default="INFO")

    schedule = sub.add_parser("schedule", help="按固定频率循环巡检")
    schedule.add_argument("--interval-hours", type=float, default=None, help="巡检间隔小时，默认取配置 6")
    schedule.add_argument("--max-cycles", type=int, default=None, help="最多执行轮数，便于测试")
    schedule.add_argument("--mode", choices=["offline", "live", "auto"])
    schedule.add_argument("--fixture", help="离线快照路径")
    schedule.add_argument("--registry")
    schedule.add_argument("--state")
    schedule.add_argument("--output-dir")
    schedule.add_argument("--log-level", default="INFO")
    return parser


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def _setup_logging(config: MonitorConfig, output_dir: str | None, level: str) -> None:
    base = Path(output_dir).expanduser().resolve() if output_dir else config.resolve("paths.logs_dir")
    utils.ensure_dir(base)
    log_file = base / "competitor_monitor.log"
    utils.setup_logging(level=level, log_file=log_file, console=True, force=True)


def _print_summary(summary: dict[str, Any]) -> None:
    counts = summary["counts"]
    print("")
    print("=" * 76)
    print(f"✓ 竞品巡检完成：{summary['run_id']}")
    print(f"  模式      : {summary['mode']}")
    print(
        f"  竞品      : {counts['success']} 成功 / {counts['failed']} 失败"
        f"  |  预警: {counts['alerts']}  |  差评: {counts['negative_reviews']}"
    )
    print(f"  痛点报告  : {summary['report']}")
    print(f"  预警汇总  : {summary['latest_alerts']}")
    print(f"  运行摘要  : {summary.get('summary', '-')}")
    for failure in summary["failures"]:
        print(f"  ! 跳过 {failure.get('name')}: {failure.get('error')}")
    print("=" * 76)


def main(argv: Iterable[str] | None = None) -> int:
    _configure_stdio()
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        config = load_config(args.config)
    except (MonitorError, utils.UtilError) as exc:
        print(f"✗ 配置加载失败：{exc}", file=sys.stderr)
        return 1

    if args.command == "list":
        try:
            payload = load_registry(config, path=args.registry)
        except (MonitorError, utils.UtilError) as exc:
            print(f"✗ {exc}", file=sys.stderr)
            return 1
        if not payload["competitors"]:
            print("暂无竞品，使用 add 添加公开商品链接。")
            return 0
        print(f"{'ID':<24} {'平台':<12} {'名称':<28} URL")
        for item in payload["competitors"]:
            print(f"{item['id']:<24} {item['platform']:<12} {item['name'][:28]:<28} {item['url']}")
        if payload.get("invalid_entries"):
            print(f"! 另有 {len(payload['invalid_entries'])} 个无效条目，已跳过")
        return 0

    if args.command == "add":
        try:
            entry = add_competitor(
                config,
                url=args.url,
                name=args.name,
                platform=args.platform,
                price_pct=args.price_pct,
                price_abs=args.price_abs,
                rank_abs=args.rank_abs,
                registry_path=args.registry,
            )
        except (MonitorError, utils.UtilError) as exc:
            print(f"✗ 添加失败：{exc}", file=sys.stderr)
            return 1
        print(f"✓ 已添加竞品：{entry['id']}")
        print(f"  名称: {entry['name']}")
        print(f"  平台: {entry['platform']}")
        print(f"  链接: {entry['url']}")
        return 0

    if args.command == "remove":
        if not args.target and not args.all_demo:
            print("✗ 请指定竞品 ID/URL，或使用 --all-demo", file=sys.stderr)
            return 1
        try:
            removed = remove_competitor(
                config,
                target=args.target,
                all_demo=args.all_demo,
                registry_path=args.registry,
            )
        except (MonitorError, utils.UtilError) as exc:
            print(f"✗ 删除失败：{exc}", file=sys.stderr)
            return 1
        print(f"✓ 已删除 {len(removed)} 个竞品")
        for item in removed:
            print(f"  - {item['id']} {item['name']}")
        return 0

    output_dir = args.output_dir
    _setup_logging(config, output_dir, args.log_level)
    engine = MonitorEngine(
        config,
        registry_path=args.registry,
        state_path=args.state,
        output_dir=output_dir,
        fixture_path=args.fixture,
    )
    if args.command == "run":
        try:
            summary = engine.run(mode=args.mode)
        except (MonitorError, utils.UtilError) as exc:
            logger.error("巡检失败: %s", exc)
            print(f"✗ 巡检失败：{exc}", file=sys.stderr)
            return 1
        _print_summary(summary)
        return 0
    if args.command == "schedule":
        interval = args.interval_hours
        if interval is None:
            interval = float(config.get("monitor.interval_hours", DEFAULT_INTERVAL_HOURS))
        try:
            validate_interval(interval)
        except MonitorError as exc:
            print(f"✗ {exc}", file=sys.stderr)
            return 1
        print(
            f"定时巡检启动：每 {interval:g} 小时执行一次"
            f"（Ctrl+C 停止；max_cycles={args.max_cycles or '不限'}）"
        )
        try:
            cycles = run_schedule(
                engine,
                interval_hours=interval,
                max_cycles=args.max_cycles,
                mode=args.mode,
            )
        except KeyboardInterrupt:
            print("已停止定时巡检")
            return 0
        print(f"✓ 定时巡检结束，共完成 {cycles} 轮")
        return 0
    return 1


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "competitor_monitor"))
````

## `compliance_check.py`

````python
#!/usr/bin/env python3
"""欧美储能产品合规风险筛查。

输入：
    - 第二步选品表（SKU / 商品名）；
    - 模拟产品合规主数据（电压、频率、电池、无线、认证资料等）。

输出：
    - 结构化 Excel：汇总、不符合项、产品参数、标准依据；
    - JSON 摘要。

说明：
    CE 是适用指令/法规下的符合性评估与自我声明，不是一张“CE 证书”；
    FCC 按设备类型区分 SDoC 与认证（FCC ID）。本脚本只做规则初筛，
    不替代测试实验室、认证机构、律师或海关/平台审核。
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
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

logger = utils.get_logger("compliance_check")
DEFAULT_SELECTION = PROJECT_ROOT / "outputs" / "research" / "high_potential_products.xlsx"
DEFAULT_MASTER = PROJECT_ROOT / "data" / "mock" / "product_compliance_master.json"
DEFAULT_RULES = PROJECT_ROOT / "config" / "compliance_rules.yaml"
DEFAULT_OUTPUT = PROJECT_ROOT / "outputs" / "compliance" / "compliance_check.xlsx"
DEFAULT_JSON = PROJECT_ROOT / "outputs" / "compliance" / "compliance_summary.json"
SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1}
STATUS_LABEL = {"high": "不符合", "medium": "待补充", "low": "建议"}


class ComplianceError(RuntimeError):
    """合规筛查异常。"""


@dataclass(frozen=True)
class Rules:
    root: Path
    data: dict[str, Any]

    @property
    def weights(self) -> dict[str, float]:
        return {str(k): float(v) for k, v in (self.data.get("severity_weights") or {}).items()}

    @property
    def standards(self) -> dict[str, dict[str, Any]]:
        return {
            str(item["id"]): dict(item)
            for item in (self.data.get("standards") or [])
            if isinstance(item, dict) and item.get("id")
        }

    def get(self, dotted: str, default: Any = None) -> Any:
        return utils.deep_get(self.data, dotted, default)


def load_rules(path: str | Path = DEFAULT_RULES) -> Rules:
    target = Path(path).expanduser().resolve()
    data = utils.read_yaml(target)
    if not isinstance(data, dict) or not data.get("standards"):
        raise ComplianceError(f"合规规则格式错误: {target}")
    return Rules(root=PROJECT_ROOT, data=data)


def _num(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d+(?:\.\d+)?", str(value or ""))
    return float(match.group(0)) if match else default


def _load_selection(path: str | Path) -> dict[str, dict[str, Any]]:
    source = Path(path).expanduser().resolve()
    if not source.exists():
        logger.warning("选品表不存在，仅使用合规主数据: %s", source)
        return {}
    try:
        from openpyxl import load_workbook
    except ImportError as exc:  # pragma: no cover
        raise ComplianceError("读取选品表需要 openpyxl") from exc
    wb = load_workbook(source, read_only=True, data_only=True)
    ws = wb["高潜力选品"] if "高潜力选品" in wb.sheetnames else wb[wb.sheetnames[0]]
    headers: list[str] = []
    header_row = 1
    for row_index, row in enumerate(ws.iter_rows(min_row=1, max_row=20, values_only=True), start=1):
        values = [str(cell or "").strip() for cell in row]
        if "SKU" in values or "sku" in values:
            headers = values
            header_row = row_index
            break
    result: dict[str, dict[str, Any]] = {}
    for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
        record = dict(zip(headers, row, strict=False))
        sku = str(record.get("SKU") or record.get("sku") or "").strip()
        if not sku:
            continue
        result[sku] = {
            "name": str(record.get("商品标题") or record.get("title") or ""),
            "platform": str(record.get("平台") or record.get("platform_label") or ""),
            "market": str(record.get("目标市场") or record.get("market") or ""),
            "price_usd": _num(record.get("零售基准价(USD)") or record.get("retail_price_usd")),
        }
    wb.close()
    return result


def load_master(path: str | Path = DEFAULT_MASTER, selection: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    master_path = Path(path).expanduser().resolve()
    payload = utils.read_json(master_path)
    if not isinstance(payload, dict) or not isinstance(payload.get("products"), list):
        raise ComplianceError(f"产品合规主数据格式错误: {master_path}")
    selection = selection or {}
    products: list[dict[str, Any]] = []
    for item in payload["products"]:
        if not isinstance(item, dict) or not item.get("sku"):
            continue
        product = dict(item)
        extra = selection.get(str(product["sku"]), {})
        product["name"] = product.get("name") or extra.get("name") or product.get("model") or product["sku"]
        product["platform_label"] = extra.get("platform", "")
        product["output_w"] = product.get("output_w") or product.get("rated_power_w")
        product["target_markets"] = [
            str(m).upper() for m in (product.get("target_markets") or ["US", "EU"])
        ]
        products.append(product)
    if not products:
        raise ComplianceError("合规主数据为空")
    return products


@dataclass
class Finding:
    sku: str
    product_name: str
    market: str
    standard_id: str
    standard_label: str
    requirement: str
    observed: str
    severity: str
    suggestion: str
    evidence: str
    status: str
    finding_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "sku": self.sku,
            "product": self.product_name,
            "market": self.market,
            "standard_id": self.standard_id,
            "standard": self.standard_label,
            "requirement": self.requirement,
            "observed": self.observed,
            "severity": self.severity,
            "status": self.status,
            "suggestion": self.suggestion,
            "evidence_needed": self.evidence,
        }


class ComplianceChecker:
    def __init__(self, rules: Rules) -> None:
        self.rules = rules
        self.weights = rules.weights or {"high": 25, "medium": 10, "low": 5}
        self.standards = rules.standards
        self.thresholds = rules.data.get("thresholds", {}) or {}
        self.manual_languages = rules.data.get("manual_languages", {}) or {}

    def check(self, products: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[Finding]]:
        rows: list[dict[str, Any]] = []
        findings: list[Finding] = []
        for product in products:
            product_findings: list[Finding] = []
            markets = [str(m).upper() for m in product.get("target_markets", [])]
            for market in markets:
                if market == "US":
                    product_findings.extend(self._check_us(product))
                elif market in {"EU", "DE", "FR"}:
                    product_findings.extend(self._check_eu(product))
            product_findings.extend(self._check_general(product))
            findings.extend(product_findings)
            rows.append(self._summary_row(product, product_findings, markets))
        findings.sort(key=lambda item: (item.sku, -SEVERITY_ORDER.get(item.severity, 0), item.market))
        for index, finding in enumerate(findings, start=1):
            finding.finding_id = f"F-{index:03d}"
        return rows, findings

    # ------------------------------------------------------------------
    def _add(
        self,
        product: dict[str, Any],
        findings: list[Finding],
        *,
        market: str,
        standard_id: str,
        requirement: str,
        observed: str,
        severity: str,
        suggestion: str,
    ) -> None:
        standard = self.standards.get(standard_id, {})
        findings.append(
            Finding(
                sku=str(product["sku"]),
                product_name=str(product.get("name") or product.get("model") or ""),
                market=market,
                standard_id=standard_id,
                standard_label=str(standard.get("label") or standard_id),
                requirement=requirement,
                observed=observed,
                severity=severity,
                status=STATUS_LABEL.get(severity, "待确认"),
                suggestion=suggestion,
                evidence=str(standard.get("evidence") or "测试报告/技术文件/符合性声明"),
            )
        )

    def _check_eu(self, product: dict[str, Any]) -> list[Finding]:
        findings: list[Finding] = []
        voltage = _num(product.get("output_voltage_v"))
        frequency = _num(product.get("output_frequency_hz"))
        low, high = [float(x) for x in self.thresholds.get("eu_voltage_v", [220, 240])]
        eu_freq = float(self.thresholds.get("eu_frequency_hz", 50))
        if not low <= voltage <= high:
            self._add(
                product,
                findings,
                market="EU",
                standard_id="EU_LVD",
                requirement="欧盟市场输出额定电压应为 220-240V",
                observed=f"当前输出 {voltage:g}V / {frequency:g}Hz",
                severity="high",
                suggestion="为欧盟开发 230V/50Hz 版本，或明确不在 EU 销售该 SKU；同步更新铭牌、包装和 Listing。",
            )
        if frequency != eu_freq:
            self._add(
                product,
                findings,
                market="EU",
                standard_id="EU_LVD",
                requirement="欧盟市场输出频率应为 50Hz",
                observed=f"当前频率 {frequency:g}Hz",
                severity="high",
                suggestion="更换 EU 版本逆变器/主板并重新做 LVD/EMC 测试。",
            )
        self._require_eu_doc(
            product,
            findings,
            "EU_LVD",
            "has_lvd_report",
            "LVD 测试报告/技术文件",
            "high",
            "补齐 LVD 测试报告、风险评估、技术文件与 DoC。",
        )
        self._require_eu_doc(
            product,
            findings,
            "EU_EMC",
            "has_emc_report",
            "EMC 测试报告",
            "high",
            "补齐 EMC 发射/抗扰测试，并把测试报告纳入技术文件。",
        )
        self._require_eu_doc(
            product,
            findings,
            "EU_ROHS",
            "has_rohs_report",
            "RoHS 均质材料检测/声明",
            "high",
            "补齐 RoHS 10 项检测或供应链声明，保留物料清单与报告。",
        )
        self._require_eu_doc(
            product,
            findings,
            "EU_WEEE",
            "has_weee_registration",
            "WEEE 注册与回收方案",
            "medium",
            "完成目标成员国 WEEE 注册，增加带叉垃圾桶标识。",
        )
        self._require_eu_doc(
            product,
            findings,
            "EU_BATTERY",
            "has_battery_regulation_doc",
            "EU Battery Regulation 文件",
            "high",
            "建立电池碳足迹/回收料/标签/护照路线图，并保留电池安全与供应链文件。",
        )
        self._require_eu_doc(
            product,
            findings,
            "EU_GPSR",
            "has_gpsr_docs",
            "GPSR 技术文件与风险评估",
            "high",
            "补齐 GPSR 风险评估、追溯信息、事故记录与召回流程。",
        )
        self._require_eu_doc(
            product,
            findings,
            "EU_GPSR",
            "has_eu_rep",
            "EU Responsible Person",
            "high",
            "指定欧盟责任人，并在包装/说明书/Listing 标注名称、地址、邮箱。",
        )
        if not product.get("has_ce_mark"):
            self._add(
                product,
                findings,
                market="EU",
                standard_id="EU_LVD",
                requirement="CE 标记与 EU Declaration of Conformity",
                observed="has_ce_mark=false",
                severity="high",
                suggestion="完成适用指令评估并签署 DoC 后再加贴 CE；不得先贴标后补测试。",
            )
        if product.get("wireless") and not product.get("has_red_report"):
            self._add(
                product,
                findings,
                market="EU",
                standard_id="EU_RED",
                requirement="无线模块适用 RED 2014/53/EU",
                observed=f"wireless=true ({product.get('wireless_tech') or '未注明'}) / has_red_report=false",
                severity="high",
                suggestion="补齐 RED 射频、EMC、安全与射频暴露评估；确认模块证书覆盖整机。",
            )
        required_languages = self.manual_languages.get("eu_required", ["en", "de", "fr"])
        languages = {str(x).lower() for x in (product.get("manual_languages") or [])}
        missing_languages = [lang for lang in required_languages if lang.lower() not in languages]
        if missing_languages:
            self._add(
                product,
                findings,
                market="EU",
                standard_id="EU_GPSR",
                requirement="说明书/安全信息应覆盖目标市场语言",
                observed=f"manual_languages={sorted(languages)}，缺少 {missing_languages}",
                severity="medium",
                suggestion="补充目标市场官方语言说明书与安全警告，DE/FR 需母语审校。",
            )
        plug = str(product.get("plug_type") or "")
        if not any(token in plug.upper() for token in ("EU", "TYPE C", "TYPE F", "SCHUKO")):
            self._add(
                product,
                findings,
                market="EU",
                standard_id="EU_LVD",
                requirement="欧盟市场插头/接口应与 230V 制式匹配",
                observed=f"plug_type={plug or '未填写'}",
                severity="high",
                suggestion="提供 EU Type C/F 插头版本，或在 Listing 明确该 SKU 不适用 EU。",
            )
        return findings

    def _check_us(self, product: dict[str, Any]) -> list[Finding]:
        findings: list[Finding] = []
        voltage = _num(product.get("output_voltage_v"))
        frequency = _num(product.get("output_frequency_hz"))
        low, high = [float(x) for x in self.thresholds.get("us_voltage_v", [100, 130])]
        us_freq = float(self.thresholds.get("us_frequency_hz", 60))
        if not low <= voltage <= high:
            self._add(
                product,
                findings,
                market="US",
                standard_id="US_FCC15B",
                requirement="美国市场输出额定电压应为 100-130V",
                observed=f"当前输出 {voltage:g}V / {frequency:g}Hz",
                severity="high",
                suggestion="为美国版本使用 120V/60Hz 逆变器；同步更新铭牌、包装和 Listing。",
            )
        if frequency != us_freq:
            self._add(
                product,
                findings,
                market="US",
                standard_id="US_FCC15B",
                requirement="美国市场输出频率应为 60Hz",
                observed=f"当前频率 {frequency:g}Hz",
                severity="high",
                suggestion="更换 US 版本逆变器/主板并重新测试。",
            )
        self._require_us_doc(
            product,
            findings,
            "US_FCC15B",
            "has_fcc_part15b",
            "FCC Part 15 Subpart B 测试报告",
            "high",
            "补齐 Part 15B 发射测试，并准备 SDoC。",
        )
        self._require_us_doc(
            product,
            findings,
            "US_FCC15B",
            "has_fcc_sdoc",
            "FCC SDoC 符合性声明",
            "high",
            "由美国责任方签署 SDoC，保留测试报告与标签。",
        )
        if not product.get("has_fcc_label"):
            self._add(
                product,
                findings,
                market="US",
                standard_id="US_FCC15B",
                requirement="FCC 合规标签/用户手册声明",
                observed="has_fcc_label=false",
                severity="medium",
                suggestion="按规则添加 FCC 合规声明与必要标签。",
            )
        if product.get("wireless") and not product.get("has_fcc_id"):
            self._add(
                product,
                findings,
                market="US",
                standard_id="US_FCC15C",
                requirement="无线模块需 FCC ID / Part 15C 认证",
                observed=f"wireless=true ({product.get('wireless_tech') or '未注明'}) / has_fcc_id=false",
                severity="high",
                suggestion="完成 FCC Part 15C 认证并取得 FCC ID；确认模块认证覆盖整机。",
            )
        if not product.get("has_ul2743"):
            self._add(
                product,
                findings,
                market="US",
                standard_id="US_UL2743",
                requirement="美国零售市场通常要求 UL 2743 或 NRTL 认可的安全方案",
                observed="has_ul2743=false",
                severity="medium",
                suggestion="安排 UL 2743 测试或提供 NRTL 认可的等效安全报告。",
            )
        if not product.get("has_prop65_warning"):
            self._add(
                product,
                findings,
                market="US",
                standard_id="US_PROP65",
                requirement="加州 Prop 65 化学品暴露评估/警示",
                observed="has_prop65_warning=false",
                severity="medium",
                suggestion="完成材料评估，必要时添加 Prop 65 警示标签。",
            )
        plug = str(product.get("plug_type") or "")
        if not any(token in plug.upper() for token in ("US", "TYPE A", "TYPE B")):
            self._add(
                product,
                findings,
                market="US",
                standard_id="US_FCC15B",
                requirement="美国市场插头/接口应与 120V 制式匹配",
                observed=f"plug_type={plug or '未填写'}",
                severity="high",
                suggestion="提供 US Type A/B 插头版本，或在 Listing 明确该 SKU 不适用 US。",
            )
        return findings

    def _check_general(self, product: dict[str, Any]) -> list[Finding]:
        findings: list[Finding] = []
        battery_wh = _num(product.get("battery_wh"))
        if battery_wh <= 0:
            self._add(
                product,
                findings,
                market="GLOBAL",
                standard_id="UN383",
                requirement="锂电池产品必须明确容量与 UN38.3 状态",
                observed="battery_wh<=0 或未填写",
                severity="high",
                suggestion="补齐电池容量、电芯规格与 UN38.3 测试摘要，再评估运输与上架。",
            )
        elif not product.get("has_un383"):
            self._add(
                product,
                findings,
                market="GLOBAL",
                standard_id="UN383",
                requirement="锂电池运输需 UN38.3 测试摘要",
                observed="has_un383=false",
                severity="high",
                suggestion="取得 UN38.3 测试摘要、MSDS 与合规包装方案后再安排运输。",
            )
        if battery_wh > float(self.thresholds.get("battery_air_advisory_wh", 100)):
            self._add(
                product,
                findings,
                market="GLOBAL",
                standard_id="IATA",
                requirement=">100Wh 锂电池空运通常受限制/需批准",
                observed=f"battery_wh={battery_wh:g}",
                severity="low",
                suggestion="核对 IATA DGR 包装说明、航空运输鉴定与货代要求；必要时改海运/陆运。",
            )
        if not product.get("ip_rating"):
            self._add(
                product,
                findings,
                market="GLOBAL",
                standard_id="EU_LVD",
                requirement="户外使用场景应明确 IP 防护等级",
                observed="ip_rating 未填写",
                severity="medium",
                suggestion="补充 IP 等级与测试依据；未测试前不要在 Listing 使用防水/防尘表述。",
            )
        if _num(product.get("rated_power_w")) < _num(product.get("output_w")):
            self._add(
                product,
                findings,
                market="GLOBAL",
                standard_id="EU_LVD",
                requirement="额定功率不得低于对外宣称的 AC 输出功率",
                observed=f"rated_power_w={product.get('rated_power_w')} / output_w={product.get('output_w')}",
                severity="high",
                suggestion="核对铭牌、说明书与测试报告的额定功率，统一口径。",
            )
        return findings

    def _require_eu_doc(
        self,
        product: dict[str, Any],
        findings: list[Finding],
        standard_id: str,
        field: str,
        requirement: str,
        severity: str,
        suggestion: str,
    ) -> None:
        if product.get(field):
            return
        self._add(
            product,
            findings,
            market="EU",
            standard_id=standard_id,
            requirement=requirement,
            observed=f"{field}=false",
            severity=severity,
            suggestion=suggestion,
        )

    def _require_us_doc(
        self,
        product: dict[str, Any],
        findings: list[Finding],
        standard_id: str,
        field: str,
        requirement: str,
        severity: str,
        suggestion: str,
    ) -> None:
        if product.get(field):
            return
        self._add(
            product,
            findings,
            market="US",
            standard_id=standard_id,
            requirement=requirement,
            observed=f"{field}=false",
            severity=severity,
            suggestion=suggestion,
        )

    def _summary_row(
        self,
        product: dict[str, Any],
        findings: list[Finding],
        markets: list[str],
    ) -> dict[str, Any]:
        counts = Counter(item.severity for item in findings)
        score = 100.0
        for severity, count in counts.items():
            score -= count * self.weights.get(severity, 10)
        score = max(0.0, min(100.0, score))
        if counts["high"]:
            status = "FAIL"
        elif counts["medium"]:
            status = "CONDITIONAL"
        else:
            status = "PASS"
        market_status: dict[str, str] = {}
        for market in markets:
            market_findings = [item for item in findings if item.market == market]
            if any(item.severity == "high" for item in market_findings):
                market_status[market] = "FAIL"
            elif any(item.severity == "medium" for item in market_findings):
                market_status[market] = "CONDITIONAL"
            else:
                market_status[market] = "PASS"
        top = next((item for item in findings if item.severity in {"high", "medium"}), None)
        return {
            "sku": product["sku"],
            "model": product.get("model") or "",
            "name": product.get("name") or "",
            "platform": product.get("platform_label") or "",
            "target_markets": "/".join(markets),
            "output_voltage_v": product.get("output_voltage_v"),
            "output_frequency_hz": product.get("output_frequency_hz"),
            "rated_power_w": product.get("rated_power_w"),
            "battery_wh": product.get("battery_wh"),
            "battery_chemistry": product.get("battery_chemistry"),
            "wireless": bool(product.get("wireless")),
            "high": counts["high"],
            "medium": counts["medium"],
            "low": counts["low"],
            "risk_score": round(score, 1),
            "status": status,
            "us_status": market_status.get("US", "-"),
            "eu_status": market_status.get("EU", "-"),
            "top_risk": top.requirement if top else "未发现规则内高风险",
            "top_suggestion": top.suggestion if top else "保持文件更新并做年度复核",
        }


# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------
def export_excel(
    rows: list[dict[str, Any]],
    findings: list[Finding],
    products: list[dict[str, Any]],
    rules: Rules,
    output: Path,
    *,
    run_id: str,
    generated_at: str,
) -> Path:
    try:
        from openpyxl import Workbook
        from openpyxl.formatting.rule import ColorScaleRule
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
        from openpyxl.utils import get_column_letter
    except ImportError as exc:  # pragma: no cover
        raise ComplianceError("生成 Excel 需要 openpyxl") from exc

    wb = Workbook()
    ws = wb.active
    ws.title = "合规汇总"
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True, size=10)
    border = Border(
        left=Side(style="thin", color="D9E2F3"),
        right=Side(style="thin", color="D9E2F3"),
        top=Side(style="thin", color="D9E2F3"),
        bottom=Side(style="thin", color="D9E2F3"),
    )

    def meta(sheet: Any, title: str, columns: int = 12) -> None:
        sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=columns)
        sheet["A1"] = title
        sheet["A1"].font = Font(bold=True, size=16, color="1F4E78")
        sheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=columns)
        sheet["A2"] = f"运行：{run_id} ｜ 生成：{generated_at} ｜ 规则初筛，不构成法律/认证意见"
        sheet["A2"].font = Font(size=9, color="595959")
        sheet.merge_cells(start_row=3, start_column=1, end_row=3, end_column=columns)
        sheet["A3"] = "范围：CE（LVD/EMC/RoHS/WEEE/Battery/GPSR/RED）与 FCC（Part 15B/15C）；数据为模拟产品参数。"
        sheet["A3"].font = Font(size=9, color="7F6000")
        sheet["A3"].fill = PatternFill("solid", fgColor="FFF2CC")
        sheet.row_dimensions[1].height = 26
        sheet.row_dimensions[2].height = 20
        sheet.row_dimensions[3].height = 22

    # 合规汇总
    meta(ws, "欧美储能产品合规风险汇总", 15)
    headers = [
        "SKU", "型号", "商品", "平台", "目标市场", "输出电压(V)", "频率(Hz)", "额定功率(W)",
        "电池(Wh)", "高风险", "中风险", "低风险", "风险分", "状态", "美国", "欧盟", "Top风险",
    ]
    header_row = 5
    for index, header in enumerate(headers, start=1):
        cell = ws.cell(row=header_row, column=index, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    for row_index, item in enumerate(rows, start=header_row + 1):
        values = [
            item["sku"], item["model"], item["name"], item["platform"], item["target_markets"],
            item["output_voltage_v"], item["output_frequency_hz"], item["rated_power_w"],
            item["battery_wh"], item["high"], item["medium"], item["low"], item["risk_score"],
            item["status"], item["us_status"], item["eu_status"], item["top_risk"],
        ]
        for col_index, value in enumerate(values, start=1):
            cell = ws.cell(row=row_index, column=col_index, value=value)
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=col_index in {3, 17})
            if col_index == 13:
                cell.number_format = "0.0"
        status_cell = ws.cell(row=row_index, column=14)
        color = {"FAIL": "F4CCCC", "CONDITIONAL": "FFF2CC", "PASS": "D9EAD3"}.get(str(item["status"]), "FFFFFF")
        status_cell.fill = PatternFill("solid", fgColor=color)
        status_cell.font = Font(bold=True)
    ws.freeze_panes = "A6"
    ws.auto_filter.ref = f"A{header_row}:Q{header_row + len(rows)}"
    widths = [20, 18, 30, 11, 12, 12, 10, 11, 10, 9, 9, 9, 9, 12, 10, 10, 44]
    for index, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.sheet_view.showGridLines = False
    if rows:
        ws.conditional_formatting.add(
            f"M{header_row + 1}:M{header_row + len(rows)}",
            ColorScaleRule(
                start_type="num", start_value=0, start_color="F8696B",
                mid_type="num", mid_value=60, mid_color="FFEB84",
                end_type="num", end_value=100, end_color="63BE7B",
            ),
        )

    # 不符合项
    ws2 = wb.create_sheet("不符合项")
    meta(ws2, "不符合项与修改建议", 12)
    f_headers = ["ID", "SKU", "型号/商品", "市场", "标准", "要求", "观察值", "严重级别", "状态", "修改建议", "需要的证据"]
    for index, header in enumerate(f_headers, start=1):
        cell = ws2.cell(row=5, column=index, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    for row_index, finding in enumerate(findings, start=6):
        values = [
            getattr(finding, "finding_id", ""), finding.sku, finding.product_name, finding.market,
            finding.standard_label, finding.requirement, finding.observed, finding.severity,
            finding.status, finding.suggestion, finding.evidence,
        ]
        for col_index, value in enumerate(values, start=1):
            cell = ws2.cell(row=row_index, column=col_index, value=value)
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=col_index in {4, 5, 6, 7, 10, 11})
        sev_col = {"high": "F4CCCC", "medium": "FFF2CC", "low": "DDEBF7"}.get(finding.severity, "FFFFFF")
        ws2.cell(row=row_index, column=8).fill = PatternFill("solid", fgColor=sev_col)
    ws2.freeze_panes = "A6"
    ws2.auto_filter.ref = f"A5:K{5 + len(findings)}"
    for index, width in enumerate([8, 20, 28, 8, 32, 42, 34, 10, 10, 48, 48], start=1):
        ws2.column_dimensions[get_column_letter(index)].width = width
    ws2.sheet_view.showGridLines = False

    # 产品参数
    ws3 = wb.create_sheet("产品参数")
    meta(ws3, "模拟产品合规主数据", 12)
    p_headers = [
        "SKU", "型号", "目标市场", "输出电压(V)", "频率(Hz)", "额定功率(W)", "电池(Wh)",
        "电芯", "无线", "无线技术", "IP等级", "插头", "说明书语言", "CE", "LVD", "EMC",
        "RoHS", "WEEE", "Battery", "GPSR", "EU责任人", "RED", "UN38.3", "UL2743",
        "FCC 15B", "SDoC", "FCC ID", "FCC标签", "Prop65",
    ]
    for index, header in enumerate(p_headers, start=1):
        cell = ws3.cell(row=5, column=index, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    for row_index, product in enumerate(products, start=6):
        values = [
            product.get("sku"), product.get("model"), "/".join(product.get("target_markets", [])),
            product.get("output_voltage_v"), product.get("output_frequency_hz"), product.get("rated_power_w"),
            product.get("battery_wh"), product.get("battery_chemistry"), "是" if product.get("wireless") else "否",
            product.get("wireless_tech"), product.get("ip_rating"), product.get("plug_type"),
            "/".join(product.get("manual_languages", [])),
            *["是" if product.get(key) else "否" for key in (
                "has_ce_mark", "has_lvd_report", "has_emc_report", "has_rohs_report",
                "has_weee_registration", "has_battery_regulation_doc", "has_gpsr_docs",
                "has_eu_rep", "has_red_report", "has_un383", "has_ul2743",
                "has_fcc_part15b", "has_fcc_sdoc", "has_fcc_id", "has_fcc_label",
                "has_prop65_warning",
            )],
        ]
        for col_index, value in enumerate(values, start=1):
            cell = ws3.cell(row=row_index, column=col_index, value=value)
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=col_index in {2, 3, 13})
    ws3.freeze_panes = "A6"
    ws3.auto_filter.ref = f"A5:AC{5 + len(products)}"
    for index in range(1, len(p_headers) + 1):
        ws3.column_dimensions[get_column_letter(index)].width = 12
    for index in (1, 2, 3, 13):
        ws3.column_dimensions[get_column_letter(index)].width = 22

    # 标准依据
    ws4 = wb.create_sheet("标准依据")
    meta(ws4, "公开标准与证据清单", 8)
    s_headers = ["ID", "标准/法规", "市场", "适用范围", "需要的证据", "来源"]
    for index, header in enumerate(s_headers, start=1):
        cell = ws4.cell(row=5, column=index, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border
    for row_index, standard in enumerate(rules.standards.values(), start=6):
        values = [
            standard.get("id"), standard.get("label"), standard.get("market"),
            standard.get("scope"), standard.get("evidence"), standard.get("source"),
        ]
        for col_index, value in enumerate(values, start=1):
            cell = ws4.cell(row=row_index, column=col_index, value=value)
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    ws4.freeze_panes = "A6"
    for index, width in enumerate([18, 40, 10, 52, 58, 38], start=1):
        ws4.column_dimensions[get_column_letter(index)].width = width
    ws4.sheet_view.showGridLines = False

    wb.properties.title = "欧美储能产品合规风险筛查"
    wb.properties.creator = "Outdoor ESS AI compliance_check.py"
    wb.properties.description = "规则初筛，不构成法律或认证意见。"
    utils.ensure_dir(output.parent)
    wb.save(output)
    logger.info("合规 Excel 已生成: %s", output)
    return output


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="compliance_check",
        description="欧美储能产品 CE/FCC 合规风险筛查",
    )
    parser.add_argument("--selection", default=str(DEFAULT_SELECTION), help="选品表")
    parser.add_argument("--master", default=str(DEFAULT_MASTER), help="产品合规主数据")
    parser.add_argument("--config", default=str(DEFAULT_RULES), help="合规规则")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Excel 输出")
    parser.add_argument("--json", default=str(DEFAULT_JSON), help="JSON 摘要")
    parser.add_argument("--strict", action="store_true", help="存在高风险时退出码 2")
    parser.add_argument("--log-level", default="INFO")
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
        rules = load_rules(args.config)
        selection = _load_selection(args.selection)
        products = load_master(args.master, selection)
        checker = ComplianceChecker(rules)
        rows, findings = checker.check(products)
    except (ComplianceError, utils.UtilError) as exc:
        print(f"✗ 合规筛查失败：{exc}", file=sys.stderr)
        return 1

    output = Path(args.output).expanduser().resolve()
    json_path = Path(args.json).expanduser().resolve()
    utils.ensure_dir(output.parent)
    utils.setup_logging(
        level=args.log_level,
        log_file=output.parent / "compliance_check.log",
        console=True,
        force=True,
    )
    run_id = f"compliance_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    generated_at = utils.utc_now_iso()
    try:
        export_excel(rows, findings, products, rules, output, run_id=run_id, generated_at=generated_at)
        summary = {
            "run_id": run_id,
            "generated_at": generated_at,
            "notice": "规则初筛，不构成法律、认证或测试结论；认证状态为模拟数据。",
            "products": len(products),
            "finding_count": len(findings),
            "severity": {
                "high": sum(1 for item in findings if item.severity == "high"),
                "medium": sum(1 for item in findings if item.severity == "medium"),
                "low": sum(1 for item in findings if item.severity == "low"),
            },
            "status": {
                key: sum(1 for item in rows if item["status"] == key)
                for key in ("PASS", "CONDITIONAL", "FAIL")
            },
            "rows": rows,
            "findings": [item.to_dict() for item in findings],
            "outputs": {"excel": str(output), "json": str(json_path)},
        }
        utils.write_json(json_path, summary)
    except (ComplianceError, utils.UtilError, OSError) as exc:
        logger.error("导出失败: %s", exc)
        print(f"✗ 导出失败：{exc}", file=sys.stderr)
        return 1

    print("")
    print("=" * 72)
    print(f"✓ 合规筛查完成：{run_id}")
    print(f"  产品数  : {len(products)}")
    print(
        f"  风险项  : 高 {summary['severity']['high']} / 中 {summary['severity']['medium']} "
        f"/ 低 {summary['severity']['low']}"
    )
    print(
        f"  状态    : PASS {summary['status']['PASS']} / CONDITIONAL "
        f"{summary['status']['CONDITIONAL']} / FAIL {summary['status']['FAIL']}"
    )
    print(f"  Excel   : {output}")
    print(f"  JSON    : {json_path}")
    print("=" * 72)
    if args.strict and summary["severity"]["high"]:
        return 2
    return 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "compliance_check"))
````

## `config/amazon_listing_profile.yaml`

````yaml
# =============================================================================
# Amazon 上架 CSV 字段档案
#
# 说明：Amazon 各站点/类目的库存文件模板会随时间和类目变化。本文件把字段名、
# 顺序、必填性和长度限制独立成“可替换 profile”，默认按便携储能类目的通用平铺
# 文件字段生成。上线前请从 Seller Central 下载当前类目模板，把本文件的 header
# 改成模板实际表头即可，生成代码无需修改。
# =============================================================================
profile:
  name: "amazon_portable_power_station_flat_file"
  version: "2026.10"
  encoding: "utf-8"
  delimiter: ","
  line_ending: "\n"
  quote: "minimal"
  notes: "字段顺序按本 profile 校验；类目专属字段以 Seller Central 当前模板为准。"

defaults:
  brand: "TrailHarbor"
  quantity: 100
  fulfillment_latency: 2
  browse_node: ""
  image_base_url: ""
  price_ending: 0.99
  item_type_keyword: "portable_power_stations"
  product_type: "POWER_STATION"
  warranty: "Limited manufacturer warranty. See product documentation for terms."
  country_of_origin_fallback: ""

markets:
  US:
    locale: "en-US"
    language: "en"
    currency: "USD"
    fx_from_usd: 1.0
    voltage: "120"
    plug_type: "US 3-pin"
    field_set: "base"
    amazon_domain: "amazon.com"
    filename: "amazon_us_listings.csv"
    gpsr_required: false
  UK:
    locale: "en-GB"
    language: "en"
    currency: "GBP"
    fx_from_usd: 0.79
    voltage: "230"
    plug_type: "UK 3-pin"
    field_set: "base"
    amazon_domain: "amazon.co.uk"
    filename: "amazon_uk_listings.csv"
    gpsr_required: false
  DE:
    locale: "de-DE"
    language: "de"
    currency: "EUR"
    fx_from_usd: 0.92
    voltage: "230"
    plug_type: "EU 2-pin"
    field_set: "eu"
    amazon_domain: "amazon.de"
    filename: "amazon_de_listings.csv"
    gpsr_required: true
  FR:
    locale: "fr-FR"
    language: "fr"
    currency: "EUR"
    fx_from_usd: 0.92
    voltage: "230"
    plug_type: "EU 2-pin"
    field_set: "eu"
    amazon_domain: "amazon.fr"
    filename: "amazon_fr_listings.csv"
    gpsr_required: true

fields:
  - {key: sku, header: sku, required_value: true, max_length: 40, type: text}
  - {key: product_type, header: product_type, required_value: true, max_length: 40, type: text}
  - {key: item_name, header: item_name, required_value: true, max_length: 200, type: text}
  - {key: brand_name, header: brand_name, required_value: true, max_length: 80, type: text}
  - {key: manufacturer, header: manufacturer, required_value: true, max_length: 80, type: text}
  - {key: product_description, header: product_description, required_value: true, max_length: 2000, type: text}
  - {key: bullet_point1, header: bullet_point1, required_value: true, max_length: 500, type: text}
  - {key: bullet_point2, header: bullet_point2, required_value: true, max_length: 500, type: text}
  - {key: bullet_point3, header: bullet_point3, required_value: true, max_length: 500, type: text}
  - {key: bullet_point4, header: bullet_point4, required_value: true, max_length: 500, type: text}
  - {key: bullet_point5, header: bullet_point5, required_value: true, max_length: 500, type: text}
  - {key: generic_keywords, header: generic_keywords, required_value: true, max_length: 250, type: text}
  - {key: standard_price, header: standard_price, required_value: true, max_length: 20, type: decimal}
  - {key: list_price, header: list_price, required_value: true, max_length: 20, type: decimal}
  - {key: currency, header: currency, required_value: true, max_length: 3, type: text}
  - {key: quantity, header: quantity, required_value: true, max_length: 10, type: int}
  - {key: condition_type, header: condition_type, required_value: true, max_length: 20, type: enum, enum: [new_new]}
  - {key: fulfillment_latency, header: fulfillment_latency, required_value: true, max_length: 4, type: int}
  - {key: main_image_url, header: main_image_url, required_value: true, max_length: 500, type: url}
  - {key: other_image_url1, header: other_image_url1, required_value: false, max_length: 500, type: url}
  - {key: other_image_url2, header: other_image_url2, required_value: false, max_length: 500, type: url}
  - {key: other_image_url3, header: other_image_url3, required_value: false, max_length: 500, type: url}
  - {key: other_image_url4, header: other_image_url4, required_value: false, max_length: 500, type: url}
  - {key: other_image_url5, header: other_image_url5, required_value: false, max_length: 500, type: url}
  - {key: other_image_url6, header: other_image_url6, required_value: false, max_length: 500, type: url}
  - {key: other_image_url7, header: other_image_url7, required_value: false, max_length: 500, type: url}
  - {key: other_image_url8, header: other_image_url8, required_value: false, max_length: 500, type: url}
  - {key: external_product_id, header: external_product_id, required_value: true, max_length: 40, type: text}
  - {key: external_product_id_type, header: external_product_id_type, required_value: true, max_length: 20, type: enum, enum: [ASIN, UPC, EAN, GTIN]}
  - {key: recommended_browse_nodes, header: recommended_browse_nodes, required_value: true, max_length: 100, type: text}
  - {key: item_type_keyword, header: item_type_keyword, required_value: true, max_length: 80, type: text}
  - {key: update_delete, header: update_delete, required_value: true, max_length: 20, type: enum, enum: [Update, PartialUpdate, Delete]}
  - {key: product_site_launch_date, header: product_site_launch_date, required_value: true, max_length: 10, type: date}
  - {key: country_of_origin, header: country_of_origin, required_value: false, max_length: 2, type: text}
  - {key: warranty_description, header: warranty_description, required_value: false, max_length: 500, type: text}
  - {key: safety_warning, header: safety_warning, required_value: true, max_length: 500, type: text}
  - {key: directions_for_use, header: directions_for_use, required_value: false, max_length: 500, type: text}
  - {key: legal_disclaimer_description, header: legal_disclaimer_description, required_value: true, max_length: 500, type: text}
  - {key: supplier_declared_has_product_battery, header: supplier_declared_has_product_battery, required_value: true, max_length: 5, type: enum, enum: ["Yes", "No"]}
  - {key: supplier_declared_dg_hz_regulation, header: supplier_declared_dg_hz_regulation, required_value: true, max_length: 30, type: enum, enum: [unknown, not_applicable, ghs]}
  - {key: lithium_battery_energy_content, header: lithium_battery_energy_content, required_value: true, max_length: 20, type: decimal}
  - {key: lithium_battery_energy_content_unit, header: lithium_battery_energy_content_unit, required_value: true, max_length: 5, type: text}
  - {key: lithium_battery_packaging, header: lithium_battery_packaging, required_value: true, max_length: 50, type: enum, enum: [batteries_contained_in_equipment, batteries_packed_with_equipment, batteries_only]}
  - {key: number_of_lithium_ion_batteries, header: number_of_lithium_ion_batteries, required_value: true, max_length: 5, type: int}
  - {key: battery_type, header: battery_type, required_value: true, max_length: 30, type: text}
  - {key: wattage, header: wattage, required_value: true, max_length: 10, type: decimal}
  - {key: wattage_unit, header: wattage_unit, required_value: true, max_length: 5, type: text}
  - {key: output_voltage, header: output_voltage, required_value: true, max_length: 10, type: text}
  - {key: plug_type, header: plug_type, required_value: true, max_length: 30, type: text}
  - {key: number_of_ac_outlets, header: number_of_ac_outlets, required_value: false, max_length: 5, type: int}
  - {key: solar_input_wattage, header: solar_input_wattage, required_value: false, max_length: 10, type: decimal}
  - {key: battery_capacity, header: battery_capacity, required_value: true, max_length: 10, type: decimal}
  - {key: battery_capacity_unit, header: battery_capacity_unit, required_value: true, max_length: 5, type: text}
  - {key: item_weight, header: item_weight, required_value: true, max_length: 10, type: decimal}
  - {key: item_weight_unit, header: item_weight_unit, required_value: true, max_length: 5, type: text}
  - {key: item_length, header: item_length, required_value: false, max_length: 10, type: decimal}
  - {key: item_width, header: item_width, required_value: false, max_length: 10, type: decimal}
  - {key: item_height, header: item_height, required_value: false, max_length: 10, type: decimal}
  - {key: item_dimension_unit, header: item_dimension_unit, required_value: false, max_length: 5, type: text}
  - {key: product_tax_code, header: product_tax_code, required_value: false, max_length: 40, type: text}

eu_extra_fields:
  - {key: gpsr_safety_attestation, header: gpsr_safety_attestation, required_value: true, max_length: 20, type: enum, enum: ["Yes", "No"]}
  - {key: gpsr_manufacturer_reference, header: gpsr_manufacturer_reference, required_value: true, max_length: 200, type: text}
  - {key: gpsr_eu_responsible_person_name, header: gpsr_eu_responsible_person_name, required_value: true, max_length: 200, type: text}
  - {key: gpsr_eu_responsible_person_address, header: gpsr_eu_responsible_person_address, required_value: true, max_length: 300, type: text}
  - {key: gpsr_eu_responsible_person_email, header: gpsr_eu_responsible_person_email, required_value: true, max_length: 200, type: email}
````

## `config/competitor_monitor.yaml`

````yaml
# =============================================================================
# 竞品监控配置
# 仅抓取竞品对外公开商品页；不登录、不调用商家后台 API、不绕过验证码。
# =============================================================================
project:
  name: "户外储能竞品公开数据监控"
  timezone: "Asia/Shanghai"

monitor:
  # 默认巡检频率：6 小时；CLI --interval-hours 可覆盖
  interval_hours: 6.0
  mode: "offline"          # offline / live / auto
  respect_robots: true
  request_delay_seconds: 2.0
  timeout_seconds: 20
  max_reviews_per_competitor: 20
  negative_rating_threshold: 2
  price_threshold_pct: 3.0
  price_threshold_abs: 5.0
  rank_threshold_abs: 20
  max_pain_examples: 3
  max_alert_quote_chars: 300

crawler:
  user_agent: "OutdoorEssMonitor/0.1 (public-product-monitor; contact: research@example.com)"
  accept_language: "en-US,en;q=0.9"
  max_reviews_pages: 1

paths:
  registry: "data/competitors/competitors.json"
  state: "data/competitors/state.json"
  history: "data/competitors/history.jsonl"
  snapshots_dir: "outputs/monitor/snapshots"
  alerts_dir: "outputs/monitor/alerts"
  reports_dir: "outputs/monitor/reports"
  logs_dir: "outputs/monitor/logs"

fixture:
  path: "data/mock/competitor_public_snapshots.json"
  changed_path: "data/mock/competitor_public_snapshots_changed.json"

# 首次启动且注册表不存在时写入的演示竞品；live 模式会跳过 demo 条目
bootstrap:
  - id: "demo-amz-300"
    name: "Demo Amazon 300Wh"
    url: "https://www.amazon.com/dp/B0DEMO0001"
    platform: "amazon"
    enabled: true
    demo: true
  - id: "demo-ali-500"
    name: "Demo AliExpress 500Wh"
    url: "https://www.aliexpress.com/item/1005000000003.html"
    platform: "aliexpress"
    enabled: true
    demo: true
  - id: "demo-1688-320"
    name: "Demo 1688 320Wh"
    url: "https://detail.1688.com/offer/600000000009.html"
    platform: "alibaba_1688"
    enabled: true
    demo: true

# 差评痛点分类词典；可自行增加类别与关键词
pain_categories:
  - id: "battery_life"
    label: "电池与续航"
    keywords: ["battery drained", "battery drains", "battery life", "runtime", "run time", "drain", "drained", "drains", "capacity", "lasts", "last", "doesn't last", "does not last", "percentage", "empty"]
  - id: "charging_speed"
    label: "充电速度与充电器"
    keywords: ["charge", "charging", "recharge", "slow charge", "takes hours", "charger", "adapter", "input", "charging time"]
  - id: "solar_charging"
    label: "太阳能充电"
    keywords: ["solar", "panel", "sunlight", "cloudy", "solar input", "solar charging"]
  - id: "noise"
    label: "噪音与风扇"
    keywords: ["noise", "noisy", "fan", "loud", "hum", "buzzing", "whine"]
  - id: "power_output"
    label: "输出功率与过载"
    keywords: ["output", "watt", "shut down", "shuts down", "overload", "inverter", "ac output", "kettle", "heater", "trip", "tripped"]
  - id: "weight_portability"
    label: "重量与便携性"
    keywords: ["heavy", "weight", "carry", "portable", "bulky", "handle is", "too big", "backpack"]
  - id: "build_quality"
    label: "做工与耐用性"
    keywords: ["build", "plastic", "flimsy", "cracked", "scratched", "broken", "loose", "quality", "cheap feel", "dent"]
  - id: "display_app"
    label: "显示与 App"
    keywords: ["app", "display", "screen", "bluetooth", "wifi", "connect", "connection", "reading", "button", "firmware"]
  - id: "heat_safety"
    label: "发热与安全"
    keywords: ["hot", "heat", "overheat", "overheating", "burning", "smoke", "temperature", "safety", "swelling"]
  - id: "shipping_packaging"
    label: "物流与包装"
    keywords: ["shipping", "delivery", "arrived", "package", "packaging", "box", "dented", "missing", "late"]
  - id: "customer_service"
    label: "客服与售后"
    keywords: ["support", "customer service", "warranty", "refund", "return", "reply", "contact", "seller"]
  - id: "instructions"
    label: "说明书与上手"
    keywords: ["manual", "instructions", "confusing", "guide", "setup", "set up", "documentation"]
  - id: "compatibility"
    label: "接口与兼容性"
    keywords: ["port", "cable", "usb", "compatibility", "compatible", "adapter", "connector"]
  - id: "value_price"
    label: "价格与性价比"
    keywords: ["price", "expensive", "value", "cheap", "not worth", "overpriced"]

stopwords:
  ["the", "and", "for", "with", "this", "that", "from", "have", "has", "had", "was", "were", "are", "you", "your", "but", "not", "very", "just", "too", "all", "can", "could", "would", "should", "about", "after", "before", "when", "what", "which", "there", "their", "them", "they", "its", "it's", "i'm", "im", "my", "me", "we", "our", "us", "of", "to", "in", "on", "at", "as", "is", "be", "been", "being", "a", "an", "or", "if", "so", "up", "out", "get", "got", "one", "two", "unit", "product", "power", "station", "battery", "works", "work", "working", "use", "used", "using", "really", "still", "even", "only", "than", "then", "into", "over", "under", "more", "most", "some", "any", "does", "did", "do", "also", "because", "while", "where", "how", "why", "who", "will", "would", "can", "may", "might", "must", "much", "many", "such", "other", "these", "those", "it", "isn't", "didn't", "doesn't", "don't"]
````

## `config/compliance_rules.yaml`

````yaml
# =============================================================================
# 欧美储能产品合规规则
#
# 注意：本文件是面试演示用的规则库，不是法律意见。CE 不是单一证书，而是
# 适用指令/法规下的符合性评估与自我声明；FCC 规则也按设备类型区分 SDoC/认证。
# 实际出口前必须由具备资质的合规服务商确认适用标准、测试范围与技术文件。
# =============================================================================
severity_weights:
  high: 25
  medium: 10
  low: 5

thresholds:
  us_voltage_v: [100, 130]
  eu_voltage_v: [220, 240]
  us_frequency_hz: 60
  eu_frequency_hz: 50
  battery_air_advisory_wh: 100
  max_risk_score: 100

manual_languages:
  eu_required: ["en", "de", "fr"]
  us_required: ["en"]

standards:
  - id: "EU_LVD"
    label: "EU LVD 2014/35/EU"
    market: "EU"
    scope: "AC 50-1000V 的电气设备安全；便携储能 AC 输出通常落入适用范围。"
    evidence: "LVD 测试报告、风险评估、技术文件、EU Declaration of Conformity、CE 标记。"
    source: "EUR-Lex Directive 2014/35/EU"
  - id: "EU_EMC"
    label: "EU EMC 2014/30/EU"
    market: "EU"
    scope: "电气/电子设备的电磁兼容；含 AC 逆变器、充电与数字控制。"
    evidence: "EMC 测试报告（发射/抗扰）、技术文件、DoC。"
    source: "EUR-Lex Directive 2014/30/EU"
  - id: "EU_ROHS"
    label: "EU RoHS 2011/65/EU"
    market: "EU"
    scope: "限制铅、镉、汞、六价铬、PBB、PBDE 及四项邻苯二甲酸酯。"
    evidence: "均质材料检测报告、供应商声明、技术文件。"
    source: "EUR-Lex Directive 2011/65/EU"
  - id: "EU_WEEE"
    label: "EU WEEE 2012/19/EU"
    market: "EU"
    scope: "废弃电子电气设备回收责任、注册与标识。"
    evidence: "各成员国 WEEE 注册号、回收方案、带叉垃圾桶标识。"
    source: "EUR-Lex Directive 2012/19/EU"
  - id: "EU_BATTERY"
    label: "EU Battery Regulation (EU) 2023/1542"
    market: "EU"
    scope: "电池投放市场、碳足迹、回收料、标签、电池护照与尽职调查路线。"
    evidence: "电池测试/安全文件、碳足迹与回收含量资料、标签、供应链尽职调查。"
    source: "EUR-Lex Regulation (EU) 2023/1542"
  - id: "EU_GPSR"
    label: "EU GPSR (EU) 2023/988"
    market: "EU"
    scope: "一般产品安全、可追溯性、欧盟责任人、召回与事故记录。"
    evidence: "EU Responsible Person 名称/地址/邮箱、技术文件、风险评估、追溯信息。"
    source: "EUR-Lex Regulation (EU) 2023/988"
  - id: "EU_RED"
    label: "EU RED 2014/53/EU"
    market: "EU"
    scope: "含 Bluetooth/Wi-Fi 等无线发射模块的产品。"
    evidence: "RED 测试报告、射频暴露评估、CE-RED DoC、无线模块证书。"
    source: "EUR-Lex Directive 2014/53/EU"
  - id: "US_FCC15B"
    label: "US FCC 47 CFR Part 15 Subpart B"
    market: "US"
    scope: "无意辐射体（数字电路/AC 逆变器）的电磁发射；通常走 SDoC。"
    evidence: "Part 15B 测试报告、SDoC、FCC 标签/合规声明。"
    source: "47 CFR Part 15 Subpart B"
  - id: "US_FCC15C"
    label: "US FCC 47 CFR Part 15 Subpart C"
    market: "US"
    scope: "有意辐射体（Bluetooth/Wi-Fi 等 2.4/5GHz 模块）；通常需 FCC ID 认证。"
    evidence: "FCC ID、Grant、射频测试报告、标签与用户手册声明。"
    source: "47 CFR Part 15 Subpart C"
  - id: "US_UL2743"
    label: "US UL 2743（便携式电源安全）"
    market: "US"
    scope: "便携式电源/应急电源的电气、机械、热与电池安全；常用于零售准入。"
    evidence: "UL 2743 测试报告/证书（或 NRTL 认可方案）。"
    source: "UL 2743 / NRTL"
  - id: "US_PROP65"
    label: "California Prop 65"
    market: "US"
    scope: "加州化学品暴露警告；电池、焊料、塑料等需评估。"
    evidence: "材料评估、警示标签、供应商声明。"
    source: "California Health & Safety Code §25249.5 et seq."
  - id: "UN383"
    label: "UN 38.3 / 锂电池运输测试"
    market: "GLOBAL"
    scope: "锂离子/锂金属电池运输安全测试；空运/海运/快递均涉及。"
    evidence: "UN 38.3 测试摘要、MSDS、运输包装说明。"
    source: "UN Manual of Tests and Criteria, Part III, 38.3"
  - id: "IATA"
    label: "IATA DGR 锂电池运输限制"
    market: "GLOBAL"
    scope: ">100Wh 锂电池空运通常受限制/需批准；需核对包装与标签。"
    evidence: "UN38.3、MSDS、航空运输鉴定、包装测试。"
    source: "IATA Dangerous Goods Regulations"
````

## `config/data_sources.yaml`

````yaml
# =============================================================================
# 公开数据源目录（仅作口径与字段映射说明，不代表真实 API 接入）
# 本项目不抓取、不存储任何个人信息，不绕过任何平台访问控制。
# =============================================================================
policy:
  data_mode: "public-data-only"
  marketplace_api: "disabled"
  personal_data: "forbidden"
  robots_txt: "respect"
  source_attribution: "required"
  simulation_notice: "所有数值均为离线模拟，仅用于系统演示与流程验证。"

sources:
  - id: public_trend_proxy
    name: "公开搜索趋势代理指标"
    category: "demand"
    access: "manual-public-view"
    fields: ["keyword", "market", "search_index", "seasonality"]
    refresh: "weekly"
    note: "不调用私有 API，使用公开趋势页面的人工/离线摘要口径。"

  - id: public_price_pages
    name: "公开商品价格页"
    category: "price"
    access: "manual-public-view"
    fields: ["product", "market", "price_local", "currency"]
    refresh: "weekly"
    note: "仅记录公开标价，不登录卖家后台。"

  - id: public_competitor_pages
    name: "公开竞品详情页"
    category: "competition"
    access: "manual-public-view"
    fields: ["title", "capacity_wh", "output_w", "weight_kg", "rating", "review_count"]
    refresh: "biweekly"
    note: "用于竞品参数对比，不复制受版权保护的文案。"

  - id: public_standards
    name: "公开法规与标准目录"
    category: "compliance"
    access: "official-public-site"
    fields: ["market", "standard", "scope"]
    refresh: "monthly"
    note: "标准适用性需由持证合规服务商最终确认。"

  - id: public_macro_energy
    name: "公开能源与户外消费宏观数据"
    category: "macro"
    access: "public-report"
    fields: ["market", "household_energy_price", "outdoor_participation"]
    refresh: "quarterly"
    note: "使用公开报告摘要，不引入付费数据库。"

field_policy:
  market_code: "ISO 3166-1 alpha-2（US/DE/UK/FR/CA）"
  currency: "记录原币种，分析前统一折算 USD"
  weight: "kg，保留三位小数"
  capacity: "Wh，整数"
  timestamp: "ISO-8601 UTC"
````

## `config/listing_copy_rules.yaml`

````yaml
# =============================================================================
# Listing 文案合规规则（规则初筛，不替代法律/认证审核）
# severity: high 必须改；medium 建议改；low 需人工确认
# =============================================================================
forbidden_claims:
  - {phrase: "best", severity: high, replacement: "reliable"}
  - {phrase: "number one", severity: high, replacement: "popular"}
  - {phrase: "#1", severity: high, replacement: "popular"}
  - {phrase: "top rated", severity: medium, replacement: "well reviewed"}
  - {phrase: "world's leading", severity: high, replacement: "trusted"}
  - {phrase: "100% safe", severity: high, replacement: "designed with safety in mind"}
  - {phrase: "zero risk", severity: high, replacement: "designed to reduce risk"}
  - {phrase: "guaranteed safe", severity: high, replacement: "designed with safety in mind"}
  - {phrase: "explosion-proof", severity: high, replacement: "protected battery enclosure"}
  - {phrase: "never overheats", severity: high, replacement: "includes thermal protection"}
  - {phrase: "cure", severity: high, replacement: "support"}
  - {phrase: "treat", severity: high, replacement: "support"}
  - {phrase: "medical grade", severity: high, replacement: "not applicable"}
  - {phrase: "eco-friendly", severity: medium, replacement: "lower-emission"}
  - {phrase: "zero emissions", severity: high, replacement: "no direct exhaust emissions during use"}
  - {phrase: "carbon neutral", severity: high, replacement: "lower-carbon option"}
  - {phrase: "UL listed", severity: high, replacement: "compliance documents under review"}
  - {phrase: "UL certified", severity: high, replacement: "compliance documents under review"}
  - {phrase: "CE certified", severity: high, replacement: "compliance documents under review"}
  - {phrase: "FCC certified", severity: high, replacement: "compliance documents under review"}
  - {phrase: "RoHS certified", severity: high, replacement: "compliance documents under review"}
  - {phrase: "unlimited", severity: high, replacement: "extended"}
  - {phrase: "forever", severity: high, replacement: "long-term"}
  - {phrase: "never dies", severity: high, replacement: "long cycle life"}
  - {phrase: "100% efficiency", severity: high, replacement: "efficient operation"}
  - {phrase: "cheapest", severity: high, replacement: "value-priced"}
  - {phrase: "lowest price", severity: high, replacement: "competitive price"}
  - {phrase: "waterproof", severity: medium, replacement: "water-resistant"}
  - {phrase: "cures", severity: high, replacement: "supports"}
  - {phrase: "FDA approved", severity: high, replacement: "not a medical device"}

# 这些词即使替换也不应出现在最终 CSV；用于二次扫描
residual_terms:
  - "best"
  - "100% safe"
  - "zero risk"
  - "guaranteed"
  - "unlimited"
  - "cure"
  - "FDA approved"
  - "UL listed"
  - "CE certified"
  - "waterproof"
````

## `config/model_profiles.yaml`

````yaml
# =============================================================================
# 大模型运行档案（离线优先；live 模式仅用于文案增强）
# 模型名、上下文与价格等参数可能随服务方调整，请以实际控制台为准。
# =============================================================================
default_profile: "deepseek-v4.1-flash"

profiles:
  deepseek-v4.1-flash:
    provider: "deepseek"
    api_style: "openai-compatible"
    model: "deepseek-v4.1-flash"
    base_url_env: "DEEPSEEK_BASE_URL"
    api_key_env: "DEEPSEEK_API_KEY"
    default_temperature: 0.3
    default_max_tokens: 4096
    supports_json_mode: true
    offline_fallback: true
    usage:
      - "listing 文案润色"
      - "合规风险初筛建议"
      - "内容脚本扩写"
    guardrails:
      - "不生成绝对化功效承诺"
      - "不伪造认证、销量、评价"
      - "不输出平台后台或用户隐私数据"
      - "关键参数以结构化商品数据为准，模型不得改写"

runtime:
  request_timeout_seconds: 60
  max_retries: 3
  retry_backoff_seconds: 2
  log_prompts: false
  log_responses: false
````

## `config/product_research.yaml`

````yaml
# =============================================================================
# 选品自动化模块配置
# 只允许公开可见页面；不登录、不调用平台店铺 API、不绕过验证码。
# =============================================================================
project:
  name: "户外露营轻量化储能选品研究"
  target_markets: ["US"]
  default_market: "US"
  currency: "USD"

crawler:
  # offline: 只读本地公开快照（默认，可复现）
  # live:    仅抓公开搜索页，失败即停止
  # auto:    先尝试 live，失败后回退本地快照
  mode: "offline"
  user_agent: "OutdoorEssAI/0.2 (public-research; contact: research@example.com)"
  timeout_seconds: 20
  delay_seconds: 2.0
  respect_robots: true
  max_pages: 1
  max_results_per_platform: 30
  live_fallback_to_snapshot: true
  save_html: false

platforms:
  amazon:
    label: "Amazon"
    enabled: true
    market: "US"
    currency: "USD"
    domain: "www.amazon.com"
    search_url: "https://www.amazon.com/s?k={query}"
    query: "portable power station 300wh"
    fee_rate: 0.15
    benchmark_cost_ratio: 0.42
    conversion_rate: 0.025
    is_sourcing: false
  aliexpress:
    label: "AliExpress"
    enabled: true
    market: "US"
    currency: "USD"
    domain: "www.aliexpress.com"
    search_url: "https://www.aliexpress.com/w/wholesale-{query}.html?SearchText={query}"
    query: "portable power station 300wh"
    fee_rate: 0.08
    benchmark_cost_ratio: 0.38
    conversion_rate: 0.018
    is_sourcing: false
  alibaba_1688:
    label: "1688"
    enabled: true
    market: "US"
    source_region: "CN"
    currency: "CNY"
    domain: "s.1688.com"
    search_url: "https://s.1688.com/selloffer/offer_search.htm?keywords={query}"
    query: "户外电源 300Wh 露营"
    fee_rate: 0.15
    benchmark_cost_ratio: 0.55
    conversion_rate: 0.030
    is_sourcing: true

filters:
  capacity_wh: [100, 500]
  max_weight_kg: 15.0
  price_usd: [49.0, 1500.0]
  price_per_wh_usd: [0.10, 8.0]
  min_rating: 0.0
  exclude_keywords:
    - "cable only"
    - "carrying bag"
    - "solar panel only"
    - "replacement battery"
    - "charging adapter"
    - "power bank 10000mah"
  dedupe_same_title: true

cost_model:
  fx_to_usd:
    USD: 1.0
    EUR: 1.08
    GBP: 1.27
    CNY: 0.139
  inbound_freight_per_kg_usd: 2.2
  minimum_freight_usd: 6.0
  packaging_usd: 1.5
  duty_pct_by_market:
    US: 3.0
    DE: 2.5
    UK: 2.0
    FR: 2.5
  fulfillment_per_kg_usd: 1.8
  fulfillment_base_usd: 3.0
  default_target_channel_fee: 0.15
  ad_cost_ratio: 0.08

competition:
  weights:
    listing_density: 0.35
    review_barrier: 0.30
    ad_pressure: 0.20
    price_dispersion: 0.15
  saturation_competitors: 1000
  review_ceiling: 50000
  ad_ceiling: 60
  price_cv_full_scale_pct: 60.0

market_capacity:
  addressable_share: 0.15
  conversion_by_platform:
    amazon: 0.025
    aliexpress: 0.018
    alibaba_1688: 0.030

opportunity:
  weights:
    margin: 0.35
    market: 0.25
    competition: 0.20
    lightweight: 0.10
    data_quality: 0.10
  thresholds:
    min_gross_margin_pct: 25.0
    min_market_capacity_usd: 120000.0
    max_competition_score: 70.0
    max_weight_kg: 12.0
    min_opportunity_score: 65.0
  top_n: 30

output:
  dir: "outputs/research"
  excel_name: "high_potential_products.xlsx"
  csv_name: "cleaned_products.csv"
  summary_name: "research_summary.json"
  raw_name: "raw_public_snapshot.json"

fixture:
  path: "data/mock/public_research_snapshot.json"
````

## `config/report_generator.yaml`

````yaml
# =============================================================================
# 经营模拟与报表配置
# 所有数据为固定种子模拟，不接入真实店铺/广告/库存后台。
# =============================================================================
input:
  selection: "outputs/research/high_potential_products.xlsx"
  sheet: "高潜力选品"

output:
  dir: "outputs/operations"
  ad_file: "ad_daily_report.xlsx"
  inventory_file: "inventory_alert.xlsx"
  profit_file: "monthly_profit.xlsx"
  summary_file: "report_summary.json"

simulation:
  seed: 20261021
  period_end: "2026-09-30"
  days: 30
  target_share: 0.08
  ad_order_share: [0.35, 0.65]
  target_acos_range: [0.12, 0.22]
  ctr_range: [0.004, 0.012]
  cvr_range: [0.04, 0.10]
  inventory_begin_cover_range: [30, 90]
  inventory_onhand_cover_range: [5, 95]
  inventory_intransit_cover_range: [0, 30]
  lead_time_choices: [25, 30, 35, 40]
  safety_days: 14
  target_cover_days: 30
  aging_ratio_range: [0.0, 0.30]

cost:
  platform_fee_rate: 0.15
  return_rate: 0.03
  storage_rate_month: 0.01
  other_rate: 0.01
  fulfillment_base_usd: 3.0
  fulfillment_per_kg_usd: 1.8
  currency: "USD"
````

## `config/settings.yaml`

````yaml
# =============================================================================
# 户外储能全链路 AI 自动化系统 - 主配置
# 说明：所有业务数据均为公开数据源口径下的模拟数据，不连接任何平台店铺 API。
# =============================================================================
project:
  name: "欧美轻量化户外储能全链路 AI 自动化系统"
  code: "outdoor-ess-ai"
  version: "0.1.0"
  locale: "zh-CN"
  timezone: "Asia/Shanghai"
  mode: "offline"          # offline（默认，完全离线可跑）| live（仅大模型增强，仍需自行配置密钥）
  seed: 20260401
  run_label: "foundation"

paths:
  data_dir: "data"
  mock_dir: "data/mock"
  raw_dir: "data/raw"
  processed_dir: "data/processed"
  external_dir: "data/external"
  outputs_dir: "outputs"
  analysis_dir: "outputs/analysis"
  reports_dir: "outputs/reports"
  content_dir: "outputs/content"
  listings_dir: "outputs/listings"
  compliance_dir: "outputs/compliance"
  runs_dir: "outputs/runs"
  logs_dir: "outputs/logs"
  prompts_dir: "prompts"

logging:
  level: "INFO"
  file_name: "outdoor_ess_ai.log"
  max_bytes: 5242880
  backup_count: 5
  console: true

llm:
  provider: "deepseek"
  model: "deepseek-v4.1-flash"
  base_url: "https://api.deepseek.com/v1"
  api_key_env: "DEEPSEEK_API_KEY"
  temperature: 0.3
  max_tokens: 4096
  timeout_seconds: 60
  max_retries: 3
  offline_fallback: true
  enable_in_demo: false

business:
  markets: ["US", "DE", "UK", "FR"]
  supported_markets: ["US", "DE", "UK", "FR", "CA"]
  primary_market: "US"
  currency: "USD"
  languages: ["en", "de", "fr"]
  target_categories:
    - "portable-power-station"
    - "solar-panel"
    - "outdoor-energy-storage"
  price_band_usd: [199, 1299]
  capacity_band_wh: [300, 2048]
  compliance_regions: ["US", "EU", "UK"]
  scoring_weights:
    demand: 0.30
    competition: 0.20
    margin: 0.25
    compliance: 0.10
    logistics: 0.15
  fx_to_usd:
    USD: 1.0
    EUR: 1.08
    GBP: 1.27

channels:
  listing:
    channel_name: "generic-marketplace"
    title_max_chars: 200
    bullet_count: 5
    bullet_max_chars: 260
    description_max_chars: 2000
    search_terms_max_bytes: 250
  content:
    formats: ["short_video_script", "social_caption", "blog_outline"]
    default_language: "en"

compliance:
  forbidden_claims:
    - "best in the world"
    - "100% safe"
    - "unlimited power"
    - "zero risk"
    - "guaranteed forever"
  required_disclosures:
    - "Actual output and runtime vary by device and conditions."
    - "Lithium battery products are subject to transport regulations."
  market_requirements:
    US: ["UL 2743", "FCC", "UN38.3", "Prop 65"]
    DE: ["CE", "RoHS", "WEEE", "UN38.3", "EU Battery Regulation"]
    UK: ["UKCA", "RoHS", "WEEE", "UN38.3"]
    FR: ["CE", "RoHS", "WEEE", "UN38.3", "EU Battery Regulation"]
````

## `data/competitors/competitors.json`

````json
{
  "notice": "Demo registry. Replace demo URLs with real public product pages before live monitoring; demo entries are skipped in live mode.",
  "competitors": [
    {
      "id": "demo-amz-300",
      "name": "Demo Amazon 300Wh",
      "url": "https://www.amazon.com/dp/B0DEMO0001",
      "platform": "amazon",
      "enabled": true,
      "demo": true,
      "added_at": "2026-10-20T08:00:00+00:00",
      "price_threshold_pct": null,
      "price_threshold_abs": null,
      "rank_threshold_abs": null
    },
    {
      "id": "demo-ali-500",
      "name": "Demo AliExpress 500Wh",
      "url": "https://www.aliexpress.com/item/1005000000003.html",
      "platform": "aliexpress",
      "enabled": true,
      "demo": true,
      "added_at": "2026-10-20T08:00:00+00:00",
      "price_threshold_pct": null,
      "price_threshold_abs": null,
      "rank_threshold_abs": null
    },
    {
      "id": "demo-1688-320",
      "name": "Demo 1688 320Wh",
      "url": "https://detail.1688.com/offer/600000000009.html",
      "platform": "alibaba_1688",
      "enabled": true,
      "demo": true,
      "added_at": "2026-10-20T08:00:00+00:00",
      "price_threshold_pct": null,
      "price_threshold_abs": null,
      "rank_threshold_abs": null
    }
  ]
}
````

## `data/competitors/state.json`

````json
{
  "competitors": {
    "demo-amz-300": {
      "title": "Demo Amazon 300Wh Portable Power Station",
      "price": 279.0,
      "currency": "USD",
      "bsr": 980,
      "bsr_category": "Portable Power Stations",
      "rating": 4.2,
      "review_count": 1290,
      "last_seen": "2026-10-20T14:00:00+00:00"
    },
    "demo-ali-500": {
      "title": "Demo AliExpress 500Wh Portable Power Station",
      "price": 349.0,
      "currency": "USD",
      "bsr": 2900,
      "bsr_category": "Portable Power Stations",
      "rating": 4.0,
      "review_count": 2160,
      "last_seen": "2026-10-20T14:00:00+00:00"
    },
    "demo-1688-320": {
      "title": "Demo 1688 320Wh Outdoor Power Station",
      "price": 690.0,
      "currency": "CNY",
      "bsr": 1100,
      "bsr_category": "户外电源",
      "rating": 4.1,
      "review_count": 1390,
      "last_seen": "2026-10-20T14:00:00+00:00"
    }
  }
}
````

## `data/mock/competitor_public_snapshots.json`

````json
{
  "notice": "离线公开快照：商品、价格、BSR、评论均为演示数据，不代表真实竞品。",
  "captured_at": "2026-10-20T08:00:00+00:00",
  "snapshots": {
    "demo-amz-300": {
      "title": "Demo Amazon 300Wh Portable Power Station",
      "price": 299.0,
      "currency": "USD",
      "bsr": 1200,
      "bsr_category": "Portable Power Stations",
      "rating": 4.3,
      "review_count": 1280,
      "reviews": [
        {"rating": 1, "title": "Battery drains too fast", "body": "The battery drained from 100% to 20% in one evening. Runtime is far shorter than expected for a 300Wh unit.", "date": "2026-10-01", "author": "Public Reviewer A"},
        {"rating": 2, "title": "Fan noise at night", "body": "The fan is loud and cycles on every few minutes. I could hear it from the tent.", "date": "2026-10-02", "author": "Public Reviewer B"},
        {"rating": 1, "title": "Solar charging is very slow", "body": "Solar input is slow even in full sun. It took all day with a 200W panel.", "date": "2026-10-03", "author": "Public Reviewer C"},
        {"rating": 2, "title": "App loses connection", "body": "The app disconnects and the display sometimes shows the wrong percentage.", "date": "2026-10-04", "author": "Public Reviewer D"},
        {"rating": 4, "title": "Works fine for small devices", "body": "Charges phones and a lamp without problems.", "date": "2026-10-05", "author": "Public Reviewer E"}
      ]
    },
    "demo-ali-500": {
      "title": "Demo AliExpress 500Wh Portable Power Station",
      "price": 359.0,
      "currency": "USD",
      "bsr": 2600,
      "bsr_category": "Portable Power Stations",
      "rating": 4.1,
      "review_count": 2100,
      "reviews": [
        {"rating": 1, "title": "AC output shuts down", "body": "The AC output shuts down when I plug in a 500W kettle. It cannot handle the load.", "date": "2026-09-28", "author": "Public Reviewer F"},
        {"rating": 2, "title": "Arrived late and box damaged", "body": "Delivery took three weeks and the package arrived dented. Customer service did not reply.", "date": "2026-09-29", "author": "Public Reviewer G"},
        {"rating": 1, "title": "Heavy and bulky", "body": "Too heavy to carry to a campsite. The handle is uncomfortable.", "date": "2026-09-30", "author": "Public Reviewer H"},
        {"rating": 2, "title": "Confusing instructions", "body": "The manual is confusing and the setup guide is incomplete.", "date": "2026-10-01", "author": "Public Reviewer I"},
        {"rating": 3, "title": "Average unit", "body": "It works, but the plastic feels cheap.", "date": "2026-10-02", "author": "Public Reviewer J"}
      ]
    },
    "demo-1688-320": {
      "title": "Demo 1688 320Wh Outdoor Power Station",
      "price": 720.0,
      "currency": "CNY",
      "bsr": 900,
      "bsr_category": "户外电源",
      "rating": 4.2,
      "review_count": 1300,
      "reviews": [
        {"rating": 1, "title": "Charging brick gets very hot", "body": "The charger gets hot during charging and smells like burning plastic. Safety concern.", "date": "2026-09-25", "author": "Public Reviewer K"},
        {"rating": 2, "title": "Display reading inaccurate", "body": "The display shows 100% but the unit shuts down after 10 minutes.", "date": "2026-09-26", "author": "Public Reviewer L"},
        {"rating": 1, "title": "Missing cable in package", "body": "Package was missing the AC cable. Support asked me to wait.", "date": "2026-09-27", "author": "Public Reviewer M"},
        {"rating": 2, "title": "Too heavy for hiking", "body": "Weight is too much for backpacking. Fine for car camping.", "date": "2026-09-28", "author": "Public Reviewer N"},
        {"rating": 1, "title": "Battery capacity overstated", "body": "Battery does not last as long as claimed, and the runtime is disappointing.", "date": "2026-09-29", "author": "Public Reviewer O"}
      ]
    }
  }
}
````

## `data/mock/competitor_public_snapshots_changed.json`

````json
{
  "notice": "离线公开快照（变更版）：用于验证价格/排名异动预警，不代表真实竞品。",
  "captured_at": "2026-10-20T14:00:00+00:00",
  "snapshots": {
    "demo-amz-300": {
      "title": "Demo Amazon 300Wh Portable Power Station",
      "price": 279.0,
      "currency": "USD",
      "bsr": 980,
      "bsr_category": "Portable Power Stations",
      "rating": 4.2,
      "review_count": 1290,
      "reviews": [
        {"rating": 1, "title": "Battery drains too fast", "body": "The battery drained from 100% to 20% in one evening. Runtime is far shorter than expected for a 300Wh unit.", "date": "2026-10-01", "author": "Public Reviewer A"},
        {"rating": 2, "title": "Fan noise at night", "body": "The fan is loud and cycles on every few minutes. I could hear it from the tent.", "date": "2026-10-02", "author": "Public Reviewer B"},
        {"rating": 1, "title": "Solar charging is very slow", "body": "Solar input is slow even in full sun. It took all day with a 200W panel.", "date": "2026-10-03", "author": "Public Reviewer C"},
        {"rating": 2, "title": "App loses connection", "body": "The app disconnects and the display sometimes shows the wrong percentage.", "date": "2026-10-04", "author": "Public Reviewer D"},
        {"rating": 1, "title": "Still drains quickly", "body": "Battery still drains quickly after the firmware update.", "date": "2026-10-10", "author": "Public Reviewer P"}
      ]
    },
    "demo-ali-500": {
      "title": "Demo AliExpress 500Wh Portable Power Station",
      "price": 349.0,
      "currency": "USD",
      "bsr": 2900,
      "bsr_category": "Portable Power Stations",
      "rating": 4.0,
      "review_count": 2160,
      "reviews": [
        {"rating": 1, "title": "AC output shuts down", "body": "The AC output shuts down when I plug in a 500W kettle. It cannot handle the load.", "date": "2026-09-28", "author": "Public Reviewer F"},
        {"rating": 2, "title": "Arrived late and box damaged", "body": "Delivery took three weeks and the package arrived dented. Customer service did not reply.", "date": "2026-09-29", "author": "Public Reviewer G"},
        {"rating": 1, "title": "Heavy and bulky", "body": "Too heavy to carry to a campsite. The handle is uncomfortable.", "date": "2026-09-30", "author": "Public Reviewer H"},
        {"rating": 2, "title": "Confusing instructions", "body": "The manual is confusing and the setup guide is incomplete.", "date": "2026-10-01", "author": "Public Reviewer I"},
        {"rating": 1, "title": "Fan is very noisy", "body": "The fan is noisy under load and the app disconnects.", "date": "2026-10-11", "author": "Public Reviewer Q"}
      ]
    },
    "demo-1688-320": {
      "title": "Demo 1688 320Wh Outdoor Power Station",
      "price": 690.0,
      "currency": "CNY",
      "bsr": 1100,
      "bsr_category": "户外电源",
      "rating": 4.1,
      "review_count": 1390,
      "reviews": [
        {"rating": 1, "title": "Charging brick gets very hot", "body": "The charger gets hot during charging and smells like burning plastic. Safety concern.", "date": "2026-09-25", "author": "Public Reviewer K"},
        {"rating": 2, "title": "Display reading inaccurate", "body": "The display shows 100% but the unit shuts down after 10 minutes.", "date": "2026-09-26", "author": "Public Reviewer L"},
        {"rating": 1, "title": "Missing cable in package", "body": "Package was missing the AC cable. Support asked me to wait.", "date": "2026-09-27", "author": "Public Reviewer M"},
        {"rating": 2, "title": "Too heavy for hiking", "body": "Weight is too much for backpacking. Fine for car camping.", "date": "2026-09-28", "author": "Public Reviewer N"},
        {"rating": 1, "title": "Solar charging is slow", "body": "Solar charging is slow and the panel input is not stable.", "date": "2026-10-12", "author": "Public Reviewer R"}
      ]
    }
  }
}
````

## `data/mock/keywords.json`

````json
{
  "notice": "Simulated public keyword proxies. Search volumes are synthetic indices, not platform API data.",
  "keywords": [
    {"market": "US", "keyword": "portable power station for camping", "intent": "commercial", "search_index": 92, "difficulty": 68, "cpc_usd": 1.85},
    {"market": "US", "keyword": "lifepo4 power station", "intent": "commercial", "search_index": 78, "difficulty": 55, "cpc_usd": 1.42},
    {"market": "US", "keyword": "solar generator for rv", "intent": "commercial", "search_index": 71, "difficulty": 62, "cpc_usd": 1.66},
    {"market": "US", "keyword": "quiet power station", "intent": "transactional", "search_index": 44, "difficulty": 31, "cpc_usd": 0.96},
    {"market": "DE", "keyword": "mobile powerstation camping", "intent": "commercial", "search_index": 84, "difficulty": 59, "cpc_usd": 1.31},
    {"market": "DE", "keyword": "solar generator wohnmobil", "intent": "commercial", "search_index": 66, "difficulty": 48, "cpc_usd": 1.12},
    {"market": "DE", "keyword": "leise powerstation", "intent": "transactional", "search_index": 38, "difficulty": 27, "cpc_usd": 0.82},
    {"market": "DE", "keyword": "balkonkraftwerk speicher", "intent": "informational", "search_index": 73, "difficulty": 64, "cpc_usd": 1.05},
    {"market": "UK", "keyword": "portable power station uk", "intent": "commercial", "search_index": 76, "difficulty": 57, "cpc_usd": 1.27},
    {"market": "UK", "keyword": "camping power bank 240v", "intent": "commercial", "search_index": 58, "difficulty": 43, "cpc_usd": 0.98},
    {"market": "UK", "keyword": "solar panel for camping", "intent": "commercial", "search_index": 62, "difficulty": 46, "cpc_usd": 0.91},
    {"market": "FR", "keyword": "station electrique portable camping", "intent": "commercial", "search_index": 69, "difficulty": 50, "cpc_usd": 1.08},
    {"market": "FR", "keyword": "panneau solaire camping", "intent": "commercial", "search_index": 64, "difficulty": 44, "cpc_usd": 0.87},
    {"market": "FR", "keyword": "batterie externe 220v", "intent": "transactional", "search_index": 47, "difficulty": 33, "cpc_usd": 0.79}
  ]
}
````

## `data/mock/market_profiles.json`

````json
{
  "notice": "Simulated market-level proxies for offline demonstration. Values are illustrative, not market facts.",
  "markets": [
    {
      "market": "US",
      "language": "en",
      "currency": "USD",
      "demand_index": 88,
      "competition_index": 78,
      "growth_pct": 12.5,
      "household_energy_price_usd_kwh": 0.17,
      "outdoor_participation_pct": 54,
      "compliance_complexity": 55,
      "logistics_cost_index": 12,
      "vat_pct": 0,
      "import_duty_pct": 3.0,
      "avg_order_value_usd": 520
    },
    {
      "market": "DE",
      "language": "de",
      "currency": "EUR",
      "demand_index": 74,
      "competition_index": 61,
      "growth_pct": 8.2,
      "household_energy_price_usd_kwh": 0.40,
      "outdoor_participation_pct": 58,
      "compliance_complexity": 72,
      "logistics_cost_index": 14,
      "vat_pct": 19,
      "import_duty_pct": 2.5,
      "avg_order_value_usd": 560
    },
    {
      "market": "UK",
      "language": "en",
      "currency": "GBP",
      "demand_index": 68,
      "competition_index": 57,
      "growth_pct": 6.4,
      "household_energy_price_usd_kwh": 0.34,
      "outdoor_participation_pct": 52,
      "compliance_complexity": 60,
      "logistics_cost_index": 13,
      "vat_pct": 20,
      "import_duty_pct": 2.0,
      "avg_order_value_usd": 480
    },
    {
      "market": "FR",
      "language": "fr",
      "currency": "EUR",
      "demand_index": 64,
      "competition_index": 54,
      "growth_pct": 7.1,
      "household_energy_price_usd_kwh": 0.25,
      "outdoor_participation_pct": 55,
      "compliance_complexity": 70,
      "logistics_cost_index": 15,
      "vat_pct": 20,
      "import_duty_pct": 2.5,
      "avg_order_value_usd": 510
    }
  ]
}
````

## `data/mock/product_catalog.json`

````json
{
  "notice": "Demo catalog. Brands and products are fictional. All values are simulated and must be verified before commercial use.",
  "products": [
    {
      "sku": "NP-NOMAD-600",
      "name": "NorthPeak Nomad 600",
      "category": "portable-power-station",
      "capacity_wh": 600,
      "output_w": 600,
      "weight_kg": 7.8,
      "chemistry": "LiFePO4",
      "solar_input_w": 400,
      "cycles": 3000,
      "msrp_usd": 499.0,
      "target_markets": ["US", "DE", "UK", "FR"],
      "certifications": ["UN38.3", "FCC"],
      "use_cases": ["car camping", "weekend RV", "emergency backup"],
      "differentiators": ["compact carry handle", "fast solar recharge", "quiet operation"],
      "warranty_years": 3
    },
    {
      "sku": "TC-MINI-300",
      "name": "TrailCore Mini 300",
      "category": "portable-power-station",
      "capacity_wh": 300,
      "output_w": 300,
      "weight_kg": 4.2,
      "chemistry": "LiFePO4",
      "solar_input_w": 200,
      "cycles": 2500,
      "msrp_usd": 299.0,
      "target_markets": ["US", "DE", "UK", "FR"],
      "certifications": ["UN38.3", "CE", "RoHS", "WEEE", "EU Battery Regulation", "FCC", "UL 2743", "Prop 65"],
      "use_cases": ["day hiking", "festival", "phone and camera charging"],
      "differentiators": ["lightweight body", "USB-C PD 100W", "retractable handle"],
      "warranty_years": 2
    },
    {
      "sku": "BC-PRO-1000",
      "name": "BaseCamp Pro 1000",
      "category": "portable-power-station",
      "capacity_wh": 1024,
      "output_w": 1000,
      "weight_kg": 12.5,
      "chemistry": "LiFePO4",
      "solar_input_w": 600,
      "cycles": 3500,
      "msrp_usd": 799.0,
      "target_markets": ["US", "DE", "UK", "FR"],
      "certifications": ["UN38.3", "FCC", "CE", "RoHS", "WEEE"],
      "use_cases": ["family camping", "van life", "home emergency"],
      "differentiators": ["expandable battery port", "UPS switchover", "wheeled cart"],
      "warranty_years": 5
    },
    {
      "sku": "RP-RIDGE-1500",
      "name": "RidgePower 1500",
      "category": "portable-power-station",
      "capacity_wh": 1536,
      "output_w": 1800,
      "weight_kg": 16.8,
      "chemistry": "LiFePO4",
      "solar_input_w": 800,
      "cycles": 4000,
      "msrp_usd": 1199.0,
      "target_markets": ["US", "DE"],
      "certifications": ["UN38.3", "UL 2743", "FCC", "CE"],
      "use_cases": ["RV boondocking", "worksite", "whole-home backup"],
      "differentiators": ["high surge output", "dual solar input", "app monitoring"],
      "warranty_years": 5
    },
    {
      "sku": "NP-NOMAD-800",
      "name": "NorthPeak Nomad 800",
      "category": "portable-power-station",
      "capacity_wh": 768,
      "output_w": 800,
      "weight_kg": 9.4,
      "chemistry": "LiFePO4",
      "solar_input_w": 500,
      "cycles": 3200,
      "msrp_usd": 649.0,
      "target_markets": ["US", "UK", "FR"],
      "certifications": ["UN38.3", "UKCA"],
      "use_cases": ["overlanding", "tailgating", "remote work"],
      "differentiators": ["low-noise cooling", "dual 230V outlets", "smart load shedding"],
      "warranty_years": 3
    },
    {
      "sku": "CG-CAMP-500",
      "name": "CampGrid 500",
      "category": "portable-power-station",
      "capacity_wh": 512,
      "output_w": 500,
      "weight_kg": 6.9,
      "chemistry": "LiFePO4",
      "solar_input_w": 300,
      "cycles": 2800,
      "msrp_usd": 429.0,
      "target_markets": ["US", "DE", "UK"],
      "certifications": ["UN38.3", "CE", "WEEE"],
      "use_cases": ["car camping", "balcony backup", "outdoor photography"],
      "differentiators": ["flat-stack storage", "solar pass-through", "integrated lamp"],
      "warranty_years": 2
    },
    {
      "sku": "SF-SOLAR-120",
      "name": "SunFold 120 Portable Solar Panel",
      "category": "solar-panel",
      "capacity_wh": 0,
      "output_w": 120,
      "weight_kg": 4.6,
      "chemistry": "monocrystalline",
      "solar_input_w": 120,
      "cycles": 0,
      "msrp_usd": 249.0,
      "target_markets": ["US", "DE", "UK", "FR"],
      "certifications": ["CE", "RoHS"],
      "use_cases": ["camping", "hiking basecamp", "emergency charging"],
      "differentiators": ["foldable four-panel design", "IP67 junction box", "kickstand"],
      "warranty_years": 2
    },
    {
      "sku": "SF-SOLAR-200",
      "name": "SunFold 200 Portable Solar Panel",
      "category": "solar-panel",
      "capacity_wh": 0,
      "output_w": 200,
      "weight_kg": 7.2,
      "chemistry": "monocrystalline",
      "solar_input_w": 200,
      "cycles": 0,
      "msrp_usd": 359.0,
      "target_markets": ["US", "DE", "FR"],
      "certifications": ["CE", "RoHS", "WEEE"],
      "use_cases": ["RV", "van life", "longer off-grid trips"],
      "differentiators": ["high efficiency cells", "parallel-ready", "weather-resistant carry bag"],
      "warranty_years": 2
    }
  ]
}
````

## `data/mock/product_compliance_master.json`

````json
{
  "notice": "模拟产品合规主数据，仅用于面试演示与规则引擎验证；认证状态、参数和型号均为虚构，不可作为真实合规结论。",
  "products": [
    {
      "sku": "1688-600000000001",
      "model": "TrailHarbor 300",
      "target_markets": ["US", "EU"],
      "output_voltage_v": 120,
      "output_frequency_hz": 60,
      "input_voltage": "100-240V",
      "rated_power_w": 300,
      "battery_wh": 300,
      "battery_chemistry": "LiFePO4",
      "wireless": false,
      "wireless_tech": "",
      "ip_rating": "IP54",
      "operating_temp_c": "-10 to 40",
      "plug_type": "US Type B",
      "manual_languages": ["en"],
      "has_ce_mark": false,
      "has_lvd_report": false,
      "has_emc_report": false,
      "has_rohs_report": false,
      "has_weee_registration": false,
      "has_battery_regulation_doc": false,
      "has_gpsr_docs": false,
      "has_eu_rep": false,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": false,
      "has_fcc_part15b": false,
      "has_fcc_sdoc": false,
      "has_fcc_id": false,
      "has_fcc_label": false,
      "has_prop65_warning": false
    },
    {
      "sku": "1688-600000000009",
      "model": "TrailHarbor 320",
      "target_markets": ["US", "EU"],
      "output_voltage_v": 120,
      "output_frequency_hz": 60,
      "input_voltage": "100-240V",
      "rated_power_w": 300,
      "battery_wh": 320,
      "battery_chemistry": "LiFePO4",
      "wireless": false,
      "wireless_tech": "",
      "ip_rating": "IP54",
      "operating_temp_c": "-10 to 40",
      "plug_type": "US Type B",
      "manual_languages": ["en"],
      "has_ce_mark": true,
      "has_lvd_report": false,
      "has_emc_report": true,
      "has_rohs_report": false,
      "has_weee_registration": false,
      "has_battery_regulation_doc": false,
      "has_gpsr_docs": false,
      "has_eu_rep": false,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": true,
      "has_fcc_part15b": false,
      "has_fcc_sdoc": false,
      "has_fcc_id": false,
      "has_fcc_label": false,
      "has_prop65_warning": true
    },
    {
      "sku": "AMZ-B0DEMO0003",
      "model": "AuroraTrail 500",
      "target_markets": ["US"],
      "output_voltage_v": 120,
      "output_frequency_hz": 60,
      "input_voltage": "100-240V",
      "rated_power_w": 500,
      "battery_wh": 500,
      "battery_chemistry": "LiFePO4",
      "wireless": true,
      "wireless_tech": "Bluetooth",
      "ip_rating": "IP54",
      "operating_temp_c": "-10 to 40",
      "plug_type": "US Type B",
      "manual_languages": ["en"],
      "has_ce_mark": false,
      "has_lvd_report": false,
      "has_emc_report": false,
      "has_rohs_report": false,
      "has_weee_registration": false,
      "has_battery_regulation_doc": false,
      "has_gpsr_docs": false,
      "has_eu_rep": false,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": true,
      "has_fcc_part15b": true,
      "has_fcc_sdoc": true,
      "has_fcc_id": true,
      "has_fcc_label": true,
      "has_prop65_warning": true
    },
    {
      "sku": "1688-600000000005",
      "model": "TrailHarbor 400 EU",
      "target_markets": ["EU"],
      "output_voltage_v": 230,
      "output_frequency_hz": 50,
      "input_voltage": "100-240V",
      "rated_power_w": 400,
      "battery_wh": 400,
      "battery_chemistry": "LiFePO4",
      "wireless": false,
      "wireless_tech": "",
      "ip_rating": "IP54",
      "operating_temp_c": "-10 to 40",
      "plug_type": "EU Type F",
      "manual_languages": ["en", "de", "fr"],
      "has_ce_mark": true,
      "has_lvd_report": true,
      "has_emc_report": true,
      "has_rohs_report": true,
      "has_weee_registration": true,
      "has_battery_regulation_doc": true,
      "has_gpsr_docs": true,
      "has_eu_rep": true,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": false,
      "has_fcc_part15b": false,
      "has_fcc_sdoc": false,
      "has_fcc_id": false,
      "has_fcc_label": false,
      "has_prop65_warning": false
    },
    {
      "sku": "AMZ-B0DEMO0001",
      "model": "VoltNest Nomad 300",
      "target_markets": ["US", "EU"],
      "output_voltage_v": 120,
      "output_frequency_hz": 60,
      "input_voltage": "100-240V",
      "rated_power_w": 300,
      "battery_wh": 300,
      "battery_chemistry": "LiFePO4",
      "wireless": false,
      "wireless_tech": "",
      "ip_rating": "IP54",
      "operating_temp_c": "-10 to 40",
      "plug_type": "US Type B",
      "manual_languages": ["en"],
      "has_ce_mark": false,
      "has_lvd_report": false,
      "has_emc_report": false,
      "has_rohs_report": false,
      "has_weee_registration": false,
      "has_battery_regulation_doc": false,
      "has_gpsr_docs": false,
      "has_eu_rep": false,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": true,
      "has_fcc_part15b": true,
      "has_fcc_sdoc": true,
      "has_fcc_id": false,
      "has_fcc_label": true,
      "has_prop65_warning": true
    },
    {
      "sku": "AMZ-B0DEMO0005",
      "model": "SunPine 400",
      "target_markets": ["US"],
      "output_voltage_v": 120,
      "output_frequency_hz": 60,
      "input_voltage": "100-240V",
      "rated_power_w": 400,
      "battery_wh": 400,
      "battery_chemistry": "LiFePO4",
      "wireless": false,
      "wireless_tech": "",
      "ip_rating": "",
      "operating_temp_c": "-10 to 40",
      "plug_type": "US Type B",
      "manual_languages": ["en"],
      "has_ce_mark": false,
      "has_lvd_report": false,
      "has_emc_report": false,
      "has_rohs_report": false,
      "has_weee_registration": false,
      "has_battery_regulation_doc": false,
      "has_gpsr_docs": false,
      "has_eu_rep": false,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": false,
      "has_fcc_part15b": true,
      "has_fcc_sdoc": false,
      "has_fcc_id": false,
      "has_fcc_label": true,
      "has_prop65_warning": false
    },
    {
      "sku": "ALI-1005000000003",
      "model": "AliPower 500",
      "target_markets": ["US", "EU"],
      "output_voltage_v": 120,
      "output_frequency_hz": 60,
      "input_voltage": "100-240V",
      "rated_power_w": 600,
      "battery_wh": 500,
      "battery_chemistry": "LiFePO4",
      "wireless": true,
      "wireless_tech": "Wi-Fi",
      "ip_rating": "IP54",
      "operating_temp_c": "-10 to 40",
      "plug_type": "US Type B",
      "manual_languages": ["en"],
      "has_ce_mark": true,
      "has_lvd_report": true,
      "has_emc_report": true,
      "has_rohs_report": true,
      "has_weee_registration": false,
      "has_battery_regulation_doc": false,
      "has_gpsr_docs": false,
      "has_eu_rep": false,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": false,
      "has_fcc_part15b": false,
      "has_fcc_sdoc": false,
      "has_fcc_id": false,
      "has_fcc_label": false,
      "has_prop65_warning": false
    },
    {
      "sku": "1688-600000000003",
      "model": "TrailHarbor 500",
      "target_markets": ["US", "EU"],
      "output_voltage_v": 120,
      "output_frequency_hz": 60,
      "input_voltage": "100-240V",
      "rated_power_w": 500,
      "battery_wh": 500,
      "battery_chemistry": "LiFePO4",
      "wireless": false,
      "wireless_tech": "",
      "ip_rating": "IP54",
      "operating_temp_c": "-10 to 40",
      "plug_type": "US Type B",
      "manual_languages": ["en"],
      "has_ce_mark": false,
      "has_lvd_report": false,
      "has_emc_report": false,
      "has_rohs_report": false,
      "has_weee_registration": false,
      "has_battery_regulation_doc": false,
      "has_gpsr_docs": false,
      "has_eu_rep": false,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": false,
      "has_fcc_part15b": false,
      "has_fcc_sdoc": false,
      "has_fcc_id": false,
      "has_fcc_label": false,
      "has_prop65_warning": false
    },
    {
      "sku": "1688-600000000002",
      "model": "TrailHarbor 200",
      "target_markets": ["US", "EU"],
      "output_voltage_v": 120,
      "output_frequency_hz": 60,
      "input_voltage": "100-240V",
      "rated_power_w": 200,
      "battery_wh": 200,
      "battery_chemistry": "LiFePO4",
      "wireless": false,
      "wireless_tech": "",
      "ip_rating": "IP54",
      "operating_temp_c": "-10 to 40",
      "plug_type": "US Type B",
      "manual_languages": ["en"],
      "has_ce_mark": true,
      "has_lvd_report": true,
      "has_emc_report": true,
      "has_rohs_report": true,
      "has_weee_registration": true,
      "has_battery_regulation_doc": true,
      "has_gpsr_docs": false,
      "has_eu_rep": false,
      "has_red_report": false,
      "has_un383": true,
      "has_ul2743": false,
      "has_fcc_part15b": true,
      "has_fcc_sdoc": true,
      "has_fcc_id": false,
      "has_fcc_label": true,
      "has_prop65_warning": false
    }
  ]
}
````

## `data/mock/public_research_snapshot.json`

````json
{
  "notice": "离线公开数据快照。商品、品牌、ID、URL 与指标均为演示数据，不代表真实在售商品；live 模式只读取公开搜索页，不登录、不调用店铺 API。",
  "captured_at": "2026-10-20T08:00:00+00:00",
  "source_policy": "public-visible-only; no login; no private API; no captcha bypass",
  "records": [
    {
      "record_id": "amz-001",
      "platform": "amazon",
      "product_id": "B0DEMO0001",
      "title": "VoltNest Nomad 300 Portable Power Station, 300Wh LiFePO4 Battery, 300W AC Output, Solar Ready",
      "brand": "VoltNest",
      "url": "https://www.amazon.com/dp/B0DEMO0001",
      "market": "US",
      "currency": "USD",
      "price_local": 299.0,
      "capacity_wh": 300,
      "output_w": 300,
      "weight_kg": 4.2,
      "battery_type": "LiFePO4",
      "solar_input_w": 200,
      "ports": "AC x2, USB-C x1, USB-A x2, 12V x1",
      "rating": 4.6,
      "review_count": 1280,
      "seller": "VoltNest Demo Store",
      "monthly_search_volume": 42000,
      "competitor_count": 180,
      "ad_count": 32,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+300wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "amz-002",
      "platform": "amazon",
      "product_id": "B0DEMO0002",
      "title": "CampCore Mini 150 Portable Power Station, 150Wh Emergency Battery, 200W AC Outlet",
      "brand": "CampCore",
      "url": "https://www.amazon.com/dp/B0DEMO0002",
      "market": "US",
      "currency": "USD",
      "price_local": 169.0,
      "capacity_wh": 150,
      "output_w": 200,
      "weight_kg": 2.6,
      "battery_type": "LiFePO4",
      "solar_input_w": 100,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.4,
      "review_count": 640,
      "seller": "CampCore Demo Store",
      "monthly_search_volume": 18000,
      "competitor_count": 95,
      "ad_count": 18,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+150wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "amz-003",
      "platform": "amazon",
      "product_id": "B0DEMO0003",
      "title": "AuroraTrail 500 Portable Power Station, 500Wh LiFePO4, 500W AC Output for Camping and RV",
      "brand": "AuroraTrail",
      "url": "https://www.amazon.com/dp/B0DEMO0003",
      "market": "US",
      "currency": "USD",
      "price_local": 499.0,
      "capacity_wh": 500,
      "output_w": 500,
      "weight_kg": 6.8,
      "battery_type": "LiFePO4",
      "solar_input_w": 300,
      "ports": "AC x3, USB-C x2, USB-A x2, 12V x1",
      "rating": 4.7,
      "review_count": 3100,
      "seller": "AuroraTrail Demo Store",
      "monthly_search_volume": 55000,
      "competitor_count": 260,
      "ad_count": 45,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+500wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "amz-004",
      "platform": "amazon",
      "product_id": "B0DEMO0004",
      "title": "PeakHarbor 240 Portable Power Station, 240Wh Camping Battery with 300W AC Output",
      "brand": "PeakHarbor",
      "url": "https://www.amazon.com/dp/B0DEMO0004",
      "market": "US",
      "currency": "USD",
      "price_local": 239.0,
      "capacity_wh": 240,
      "output_w": 300,
      "weight_kg": 3.4,
      "battery_type": "LiFePO4",
      "solar_input_w": 150,
      "ports": "AC x2, USB-C x1, USB-A x2",
      "rating": 4.3,
      "review_count": 420,
      "seller": "PeakHarbor Demo Store",
      "monthly_search_volume": 22000,
      "competitor_count": 120,
      "ad_count": 22,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+240wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "amz-005",
      "platform": "amazon",
      "product_id": "B0DEMO0005",
      "title": "SunPine 400 Portable Power Station, 400Wh Solar Generator for Tent Camping",
      "brand": "SunPine",
      "url": "https://www.amazon.com/dp/B0DEMO0005",
      "market": "US",
      "currency": "USD",
      "price_local": 399.0,
      "capacity_wh": 400,
      "output_w": 400,
      "weight_kg": 5.4,
      "battery_type": "LiFePO4",
      "solar_input_w": 240,
      "ports": "AC x2, USB-C x1, USB-A x2, 12V x1",
      "rating": 4.5,
      "review_count": 980,
      "seller": "SunPine Demo Store",
      "monthly_search_volume": 31000,
      "competitor_count": 160,
      "ad_count": 28,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+400wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "amz-006",
      "platform": "amazon",
      "product_id": "B0DEMO0006",
      "title": "TerraCube 128 Mini Portable Power Station, 128Wh Pocket Camping Battery",
      "brand": "TerraCube",
      "url": "https://www.amazon.com/dp/B0DEMO0006",
      "market": "US",
      "currency": "USD",
      "price_local": 129.0,
      "capacity_wh": 128,
      "output_w": 150,
      "weight_kg": 2.2,
      "battery_type": "NMC",
      "solar_input_w": 80,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.2,
      "review_count": 310,
      "seller": "TerraCube Demo Store",
      "monthly_search_volume": 15000,
      "competitor_count": 70,
      "ad_count": 12,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+128wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "amz-007",
      "platform": "amazon",
      "product_id": "B0DEMO0007",
      "title": "TrailBox 600 Portable Power Station, 600Wh Large Capacity for RV Backup",
      "brand": "TrailBox",
      "url": "https://www.amazon.com/dp/B0DEMO0007",
      "market": "US",
      "currency": "USD",
      "price_local": 699.0,
      "capacity_wh": 600,
      "output_w": 600,
      "weight_kg": 8.5,
      "battery_type": "LiFePO4",
      "solar_input_w": 400,
      "ports": "AC x3, USB-C x2, USB-A x2",
      "rating": 4.6,
      "review_count": 1500,
      "seller": "TrailBox Demo Store",
      "monthly_search_volume": 36000,
      "competitor_count": 210,
      "ad_count": 30,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+600wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "amz-008",
      "platform": "amazon",
      "product_id": "B0DEMO0008",
      "title": "Nomad 88 Pocket Power Bank, 88Wh Small Camping Battery",
      "brand": "Nomad",
      "url": "https://www.amazon.com/dp/B0DEMO0008",
      "market": "US",
      "currency": "USD",
      "price_local": 89.0,
      "capacity_wh": 88,
      "output_w": 100,
      "weight_kg": 1.8,
      "battery_type": "NMC",
      "solar_input_w": 60,
      "ports": "AC x1, USB-C x1, USB-A x1",
      "rating": 4.0,
      "review_count": 180,
      "seller": "Nomad Demo Store",
      "monthly_search_volume": 9000,
      "competitor_count": 45,
      "ad_count": 6,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+88wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "ali-001",
      "platform": "aliexpress",
      "product_id": "1005000000001",
      "title": "Portable Power Station 300W 288Wh LiFePO4 Solar Generator for Camping",
      "brand": "Generic",
      "url": "https://www.aliexpress.com/item/1005000000001.html",
      "market": "US",
      "currency": "USD",
      "price_local": 189.0,
      "capacity_wh": 288,
      "output_w": 300,
      "weight_kg": 5.0,
      "battery_type": "LiFePO4",
      "solar_input_w": 180,
      "ports": "AC x2, USB-C x1, USB-A x2",
      "rating": 4.5,
      "review_count": 2100,
      "seller": "Demo Energy Factory Store",
      "monthly_search_volume": 36000,
      "competitor_count": 210,
      "ad_count": 15,
      "moq": 1,
      "source_page": "https://www.aliexpress.com/w/wholesale-portable-power-station-300wh.html",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "ali-002",
      "platform": "aliexpress",
      "product_id": "1005000000002",
      "title": "Camping Solar Generator 200Wh Portable Power Station 200W AC Output",
      "brand": "Generic",
      "url": "https://www.aliexpress.com/item/1005000000002.html",
      "market": "US",
      "currency": "USD",
      "price_local": 139.0,
      "capacity_wh": 200,
      "output_w": 200,
      "weight_kg": 3.8,
      "battery_type": "LiFePO4",
      "solar_input_w": 120,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.3,
      "review_count": 890,
      "seller": "Demo Outdoor Supply",
      "monthly_search_volume": 25000,
      "competitor_count": 130,
      "ad_count": 11,
      "moq": 1,
      "source_page": "https://www.aliexpress.com/w/wholesale-portable-power-station-200wh.html",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "ali-003",
      "platform": "aliexpress",
      "product_id": "1005000000003",
      "title": "500Wh Portable Power Station 600W Solar Generator for RV and Camping",
      "brand": "Generic",
      "url": "https://www.aliexpress.com/item/1005000000003.html",
      "market": "US",
      "currency": "USD",
      "price_local": 359.0,
      "capacity_wh": 500,
      "output_w": 600,
      "weight_kg": 7.2,
      "battery_type": "LiFePO4",
      "solar_input_w": 300,
      "ports": "AC x2, USB-C x2, USB-A x2",
      "rating": 4.6,
      "review_count": 1600,
      "seller": "Demo Power Tech",
      "monthly_search_volume": 28000,
      "competitor_count": 190,
      "ad_count": 19,
      "moq": 1,
      "source_page": "https://www.aliexpress.com/w/wholesale-portable-power-station-500wh.html",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "ali-004",
      "platform": "aliexpress",
      "product_id": "1005000000004",
      "title": "150Wh Mini Power Station Portable Camping Battery 180W AC",
      "brand": "Generic",
      "url": "https://www.aliexpress.com/item/1005000000004.html",
      "market": "US",
      "currency": "USD",
      "price_local": 99.0,
      "capacity_wh": 150,
      "output_w": 180,
      "weight_kg": 2.9,
      "battery_type": "NMC",
      "solar_input_w": 100,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.1,
      "review_count": 340,
      "seller": "Demo Camp Store",
      "monthly_search_volume": 14000,
      "competitor_count": 80,
      "ad_count": 7,
      "moq": 1,
      "source_page": "https://www.aliexpress.com/w/wholesale-portable-power-station-150wh.html",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "ali-005",
      "platform": "aliexpress",
      "product_id": "1005000000005",
      "title": "400Wh LiFePO4 Camping Generator Portable Power Station 400W",
      "brand": "Generic",
      "url": "https://www.aliexpress.com/item/1005000000005.html",
      "market": "US",
      "currency": "USD",
      "price_local": 269.0,
      "capacity_wh": 400,
      "output_w": 400,
      "weight_kg": 5.8,
      "battery_type": "LiFePO4",
      "solar_input_w": 240,
      "ports": "AC x2, USB-C x1, USB-A x2, 12V x1",
      "rating": 4.4,
      "review_count": 750,
      "seller": "Demo Solar Factory",
      "monthly_search_volume": 20000,
      "competitor_count": 150,
      "ad_count": 13,
      "moq": 1,
      "source_page": "https://www.aliexpress.com/w/wholesale-portable-power-station-400wh.html",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "ali-006",
      "platform": "aliexpress",
      "product_id": "1005000000006",
      "title": "240Wh Outdoor Power Supply Portable Power Station for Camping",
      "brand": "Generic",
      "url": "https://www.aliexpress.com/item/1005000000006.html",
      "market": "US",
      "currency": "USD",
      "price_local": 159.0,
      "capacity_wh": 240,
      "output_w": 250,
      "weight_kg": 3.6,
      "battery_type": "LiFePO4",
      "solar_input_w": 150,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.2,
      "review_count": 510,
      "seller": "Demo Green Power",
      "monthly_search_volume": 17000,
      "competitor_count": 100,
      "ad_count": 9,
      "moq": 1,
      "source_page": "https://www.aliexpress.com/w/wholesale-portable-power-station-240wh.html",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "ali-007",
      "platform": "aliexpress",
      "product_id": "1005000000007",
      "title": "600Wh Portable Power Station Solar Generator for Home Backup",
      "brand": "Generic",
      "url": "https://www.aliexpress.com/item/1005000000007.html",
      "market": "US",
      "currency": "USD",
      "price_local": 429.0,
      "capacity_wh": 600,
      "output_w": 600,
      "weight_kg": 8.0,
      "battery_type": "LiFePO4",
      "solar_input_w": 360,
      "ports": "AC x2, USB-C x2, USB-A x2",
      "rating": 4.5,
      "review_count": 1100,
      "seller": "Demo Backup Store",
      "monthly_search_volume": 26000,
      "competitor_count": 170,
      "ad_count": 16,
      "moq": 1,
      "source_page": "https://www.aliexpress.com/w/wholesale-portable-power-station-600wh.html",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "ali-008",
      "platform": "aliexpress",
      "product_id": "1005000000008",
      "title": "200W Foldable Solar Panel Portable Solar Charger for Camping",
      "brand": "Generic",
      "url": "https://www.aliexpress.com/item/1005000000008.html",
      "market": "US",
      "currency": "USD",
      "price_local": 169.0,
      "capacity_wh": 0,
      "output_w": 200,
      "weight_kg": 5.5,
      "battery_type": "Monocrystalline",
      "solar_input_w": 200,
      "ports": "MC4, USB-A",
      "rating": 4.4,
      "review_count": 620,
      "seller": "Demo Solar Panel",
      "monthly_search_volume": 18000,
      "competitor_count": 90,
      "ad_count": 8,
      "moq": 1,
      "source_page": "https://www.aliexpress.com/w/wholesale-200w-solar-panel.html",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-001",
      "platform": "alibaba_1688",
      "product_id": "600000000001",
      "title": "户外电源300Wh 露营便携式储能电源 300W 太阳能充电",
      "brand": "Demo Factory A",
      "url": "https://detail.1688.com/offer/600000000001.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 780.0,
      "capacity_wh": 300,
      "output_w": 300,
      "weight_kg": 4.5,
      "battery_type": "LiFePO4",
      "solar_input_w": 200,
      "ports": "AC x2, USB-C x1, USB-A x2",
      "rating": 4.6,
      "review_count": 2300,
      "seller": "Demo Factory A",
      "monthly_search_volume": 42000,
      "competitor_count": 240,
      "ad_count": 0,
      "moq": 2,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=户外电源300Wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-002",
      "platform": "alibaba_1688",
      "product_id": "600000000002",
      "title": "便携式储能电源200Wh 户外应急电源 露营备用电池",
      "brand": "Demo Factory B",
      "url": "https://detail.1688.com/offer/600000000002.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 520.0,
      "capacity_wh": 200,
      "output_w": 200,
      "weight_kg": 3.5,
      "battery_type": "LiFePO4",
      "solar_input_w": 120,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.5,
      "review_count": 1500,
      "seller": "Demo Factory B",
      "monthly_search_volume": 30000,
      "competitor_count": 140,
      "ad_count": 0,
      "moq": 5,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=户外电源200Wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-003",
      "platform": "alibaba_1688",
      "product_id": "600000000003",
      "title": "500Wh 户外移动电源 太阳能储能电源 露营房车备用",
      "brand": "Demo Factory C",
      "url": "https://detail.1688.com/offer/600000000003.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 1350.0,
      "capacity_wh": 500,
      "output_w": 500,
      "weight_kg": 6.9,
      "battery_type": "LiFePO4",
      "solar_input_w": 300,
      "ports": "AC x2, USB-C x1, USB-A x2, 12V x1",
      "rating": 4.4,
      "review_count": 980,
      "seller": "Demo Factory C",
      "monthly_search_volume": 38000,
      "competitor_count": 180,
      "ad_count": 0,
      "moq": 1,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=户外电源500Wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-004",
      "platform": "alibaba_1688",
      "product_id": "600000000004",
      "title": "150Wh 露营电源 小手提户外应急电源 150W",
      "brand": "Demo Factory D",
      "url": "https://detail.1688.com/offer/600000000004.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 360.0,
      "capacity_wh": 150,
      "output_w": 150,
      "weight_kg": 2.8,
      "battery_type": "NMC",
      "solar_input_w": 100,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.3,
      "review_count": 760,
      "seller": "Demo Factory D",
      "monthly_search_volume": 21000,
      "competitor_count": 90,
      "ad_count": 0,
      "moq": 10,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=户外电源150Wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-005",
      "platform": "alibaba_1688",
      "product_id": "600000000005",
      "title": "400Wh LiFePO4 便携储能电源 400W 户外露营太阳能",
      "brand": "Demo Factory E",
      "url": "https://detail.1688.com/offer/600000000005.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 980.0,
      "capacity_wh": 400,
      "output_w": 400,
      "weight_kg": 5.6,
      "battery_type": "LiFePO4",
      "solar_input_w": 240,
      "ports": "AC x2, USB-C x1, USB-A x2",
      "rating": 4.6,
      "review_count": 1800,
      "seller": "Demo Factory E",
      "monthly_search_volume": 26000,
      "competitor_count": 120,
      "ad_count": 0,
      "moq": 2,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=户外电源400Wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-006",
      "platform": "alibaba_1688",
      "product_id": "600000000006",
      "title": "240Wh 户外电源 便携式储能电源 露营应急备用",
      "brand": "Demo Factory F",
      "url": "https://detail.1688.com/offer/600000000006.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 610.0,
      "capacity_wh": 240,
      "output_w": 250,
      "weight_kg": 3.9,
      "battery_type": "LiFePO4",
      "solar_input_w": 150,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.2,
      "review_count": 500,
      "seller": "Demo Factory F",
      "monthly_search_volume": 18000,
      "competitor_count": 85,
      "ad_count": 0,
      "moq": 5,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=户外电源240Wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-007",
      "platform": "alibaba_1688",
      "product_id": "600000000007",
      "title": "1000Wh 大容量户外电源 房车储能电源",
      "brand": "Demo Factory G",
      "url": "https://detail.1688.com/offer/600000000007.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 2600.0,
      "capacity_wh": 1000,
      "output_w": 1000,
      "weight_kg": 12.0,
      "battery_type": "LiFePO4",
      "solar_input_w": 600,
      "ports": "AC x3, USB-C x2, USB-A x2",
      "rating": 4.5,
      "review_count": 1200,
      "seller": "Demo Factory G",
      "monthly_search_volume": 32000,
      "competitor_count": 160,
      "ad_count": 0,
      "moq": 1,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=户外电源1000Wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-008",
      "platform": "alibaba_1688",
      "product_id": "600000000008",
      "title": "100W 折叠太阳能板 户外露营便携充电板",
      "brand": "Demo Factory H",
      "url": "https://detail.1688.com/offer/600000000008.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 210.0,
      "capacity_wh": 0,
      "output_w": 100,
      "weight_kg": 3.0,
      "battery_type": "Monocrystalline",
      "solar_input_w": 100,
      "ports": "MC4, USB-A",
      "rating": 4.4,
      "review_count": 400,
      "seller": "Demo Factory H",
      "monthly_search_volume": 12000,
      "competitor_count": 70,
      "ad_count": 0,
      "moq": 20,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=折叠太阳能板100W",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "1688-009",
      "platform": "alibaba_1688",
      "product_id": "600000000009",
      "title": "320Wh 户外便携储能电源 300W 露营应急电源",
      "brand": "Demo Factory I",
      "url": "https://detail.1688.com/offer/600000000009.html",
      "market": "US",
      "origin_country": "CN",
      "currency": "CNY",
      "price_local": 720.0,
      "capacity_wh": 320,
      "output_w": 300,
      "weight_kg": 3.8,
      "battery_type": "LiFePO4",
      "solar_input_w": 200,
      "ports": "AC x2, USB-C x1, USB-A x2",
      "rating": 4.5,
      "review_count": 1300,
      "seller": "Demo Factory I",
      "monthly_search_volume": 28000,
      "competitor_count": 100,
      "ad_count": 0,
      "moq": 2,
      "source_page": "https://s.1688.com/selloffer/offer_search.htm?keywords=户外电源320Wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    },
    {
      "record_id": "amz-009",
      "platform": "amazon",
      "product_id": "B0DEMO0009",
      "title": "AuroraTrail 220 Portable Power Station, 220Wh Lightweight Camping Battery, 250W AC",
      "brand": "AuroraTrail",
      "url": "https://www.amazon.com/dp/B0DEMO0009",
      "market": "US",
      "currency": "USD",
      "price_local": 219.0,
      "capacity_wh": 220,
      "output_w": 250,
      "weight_kg": 3.1,
      "battery_type": "LiFePO4",
      "solar_input_w": 140,
      "ports": "AC x1, USB-C x1, USB-A x2",
      "rating": 4.4,
      "review_count": 560,
      "seller": "AuroraTrail Demo Store",
      "monthly_search_volume": 19000,
      "competitor_count": 105,
      "ad_count": 15,
      "moq": 1,
      "source_page": "https://www.amazon.com/s?k=portable+power+station+220wh",
      "collected_at": "2026-10-20T08:00:00+00:00"
    }
  ]
}
````

## `docs/amazon_listing.md`

````markdown
# 上架素材自动化模块运行说明

## 1. 模块定位

`listing_generator.py` 读取第二步的选品表，生成：

```text
选品 SKU
  → 多市场英文/本地化文案
  → 违禁词扫描与保守替换
  → Amazon 平铺文件 CSV（按站点）
  → 字段/长度/类型/必填/合规二次校验
  → content JSON + validation JSON + summary JSON
```

素材语气面向**欧美露营、周末短途、房车/自驾、家庭短时备电**用户，强调：

- 轻量、可单人搬运、后备箱收纳；
- 太阳能补电、无燃油/无尾气、安静使用；
- 真实限制、设备功率匹配、续航因设备而异；
- 不编造认证、销量、评价、GTIN、图片或绝对化安全承诺。

---

## 2. 快速运行

```bash
cd outdoor_ess_ai
python -m pip install -r requirements.txt

# 默认：美国站英文，读取 high_potential_products.xlsx
python listing_generator.py

# 英/德/法四个站点
python listing_generator.py --locales all

# 只生成英国站
python listing_generator.py --locales en-GB

# 限制 SKU 数、指定输出目录
python listing_generator.py --limit 5 --output-dir outputs/listing_test
```

默认输入：

```text
outputs/research/high_potential_products.xlsx
工作表：高潜力选品
```

默认输出：

```text
outputs/listing/
├── amazon_us_listings.csv          # Amazon US 平铺文件
├── en-US_content.json              # 完整文案与违规明细
├── en-US_validation.json           # 字段/格式/导入校验
├── listing_summary.json            # 多站点汇总
└── listing_generator.log
```

`--locales all` 会额外生成：

```text
amazon_uk_listings.csv + en-GB_content.json + en-GB_validation.json
amazon_de_listings.csv + de-DE_content.json + de-DE_validation.json
amazon_fr_listings.csv + fr-FR_content.json + fr-FR_validation.json
```

---

## 3. 输入与输出字段

### 3.1 输入选品表

支持 `.xlsx/.xlsm/.csv`，自动识别中英文表头。关键字段：

- SKU、平台、商品标题、品牌/供应商；
- 容量 Wh、输出功率 W、重量 kg、电芯类型、太阳能输入 W；
- 零售基准价 USD、毛利率、综合机会分、门槛状态；
- 合规提示、公开来源页。

默认只读取 `门槛状态 = 通过` 的行；`--include-failed` 可包含未通过门槛的 SKU。

可选输入列（有则优先使用，避免命令行重复填写）：

```text
main_image_url
external_product_id / external_product_id_type
recommended_browse_nodes
country_of_origin
number_of_ac_outlets
item_length / item_width / item_height
```

没有这些列时，主图/GTIN/Browse Node 会进入 blocker，不会伪造。

### 3.2 Amazon CSV

字段档案：

```text
config/amazon_listing_profile.yaml
```

当前 profile：

| 站点 | 文件 | 字段数 | 币种 | 电压 | 插头 |
| --- | --- | --- | --- | --- | --- |
| US | `amazon_us_listings.csv` | 60 | USD | 120V | US 3-pin |
| UK | `amazon_uk_listings.csv` | 60 | GBP | 230V | UK 3-pin |
| DE | `amazon_de_listings.csv` | 65 | EUR | 230V | EU 2-pin |
| FR | `amazon_fr_listings.csv` | 65 | EUR | 230V | EU 2-pin |

DE/FR 额外包含 5 个 GPSR 字段：

```text
gpsr_safety_attestation
gpsr_manufacturer_reference
gpsr_eu_responsible_person_name
gpsr_eu_responsible_person_address
gpsr_eu_responsible_person_email
```

CSV 使用 UTF-8、逗号分隔、LF 换行、最小引用；`product_description` 内使用 `<br>`，
不写入真实换行，避免平铺文件解析错位。

---

## 4. “字段 100% 匹配”的口径

Amazon 的库存文件模板**按站点、类目、时间版本变化**，不存在一份对所有类目永久通用的
平铺文件。本模块把字段独立成可替换 profile，生成时严格按 profile 的：

- 字段顺序；
- 字段名；
- 必填值；
- 最大长度；
- 数字/日期/URL/邮箱/enum 类型；
- 站点 extra 字段（EU GPSR）；

生成并校验。因此“100% 匹配”指的是**与当前 profile 100% 一致**。

正式上架前请：

1. 在 Seller Central 下载当前类目库存文件模板；
2. 把模板表头与 `config/amazon_listing_profile.yaml` 的 `header` 对齐；
3. 重新运行 `python listing_generator.py`；
4. 查看 `*_validation.json` 的 `format_ok` 与 `import_ready`。

代码不需要改，只替换 profile。

### 为什么默认 `import_ready=false`？

选品表不包含 Amazon 账号级/素材级资料，模块不会伪造：

| 阻塞项 | 原因 | 解决方式 |
| --- | --- | --- |
| `main_image_url` | 需要可公开访问的 Amazon 主图 | 上传图片后传 `--image-base-url` |
| `external_product_id` | 1688/AliExpress 行没有 GTIN/UPC | 提供 `--gtin-map` 或申请 GTIN 豁免 |
| `recommended_browse_nodes` | 需要目标类目节点 ID | 传 `--browse-node` |
| GPSR 五项 | DE/FR 欧盟责任人信息 | 填入真实欧盟责任人后重跑 |

补齐后示例：

```bash
python listing_generator.py \
  --locales en-US \
  --gtin-map data/gtin_map.csv \
  --image-base-url https://cdn.example.com/power \
  --browse-node 123456
```

`data/gtin_map.csv` 格式：

```csv
sku,external_product_id,external_product_id_type
1688-600000000001,750000000001,UPC
AMZ-B0DEMO0003,B0DEMO0003,ASIN
```

图片地址规则：

```text
{image_base_url}/{sku}/main.jpg
```

例如：

```text
https://cdn.example.com/power/1688-600000000001/main.jpg
```

仅填 URL 不会自动上传图片，需保证 URL 公网可访问且符合 Amazon 图片规范。

---

## 5. 文案结构

每个 SKU 生成：

- `item_name`：合规标题，≤200 字符；
- `bullet_point1` 至 `bullet_point5`：5 点核心描述，每点 ≤500 字符；
- `product_description`：完整详情页 HTML，≤2000 字符；
- `generic_keywords`：搜索词，≤250 bytes；
- `safety_warning`、`directions_for_use`、`legal_disclaimer_description`；
- `warranty_description`。

英文版本按市场区分：

- `en-US`：trunk、tailgating、outages、120V；
- `en-GB`：boot、staycations、power cuts、230V、UK 3-pin。

德/法版本使用本地化模板，并标记 `copy_review_required=true`；
发布前必须由母语运营审校。

### 合规话术

内置 `config/listing_copy_rules.yaml`，覆盖：

- 绝对化：best、#1、top rated、world's leading；
- 安全：100% safe、zero risk、guaranteed safe、explosion-proof、never overheats；
- 认证：UL listed、CE certified、FCC certified、RoHS certified；
- 性能：unlimited、forever、never dies、100% efficiency；
- 环保：eco-friendly、zero emissions、carbon neutral；
- 医疗：cure、treat、medical grade、FDA approved；
- 价格：cheapest、lowest price；
- 防水：waterproof（无 IP 等级时改为 water-resistant）。

处理逻辑：

1. 扫描 `item_name`、5 点、详情、搜索词、安全/使用/法律字段；
2. 命中后按配置做保守替换；
3. 将违规明细写入 `en-US_content.json` 的 `compliance.violations`；
4. 写入 CSV 前再次扫描 residual terms；
5. `*_validation.json` 记录最终 `compliance.status`。

规则初筛不替代 Amazon 审核、律师或认证机构意见。

---

## 6. CSV 校验

`*_validation.json` 包含：

| 字段 | 含义 |
| --- | --- |
| `format_ok` | 表头、列数、长度、类型、必填格式、残留违禁词是否通过 |
| `import_ready` | 是否补齐账号级/素材级必填值 |
| `blockers` | 阻止导入的字段及涉及 SKU |
| `warnings` | 非阻断风险（原产国、DG 分类、母语审校等） |
| `format_issues` | 具体格式错误 |
| `compliance` | 违禁词状态与明细 |

校验覆盖：

- 表头与 profile 完全一致；
- 每行列数一致；
- `item_name` ≤200、bullets ≤500、description ≤2000；
- `generic_keywords` ≤250 bytes；
- price 为 decimal，quantity 为整数；
- date 为 `YYYY-MM-DD`；
- URL 为 http(s)；
- enum 值合法；
- 无嵌入换行；
- 无残留违禁词；
- 必填账号字段缺失时列为 blocker。

---

## 7. 可自定义参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--input` | `outputs/research/high_potential_products.xlsx` | 选品表 |
| `--sheet` | `高潜力选品` | Excel 工作表 |
| `--profile` | `config/amazon_listing_profile.yaml` | Amazon 字段档案 |
| `--rules` | `config/listing_copy_rules.yaml` | 违禁词规则 |
| `--output-dir` | `outputs/listing` | 输出目录 |
| `--locales` | `en-US` | `en-US,en-GB,de-DE,fr-FR` 或 `all` |
| `--limit` | 全部 | 最多 SKU 数 |
| `--include-failed` | 关闭 | 包含未过门槛 SKU |
| `--gtin-map` | 空 | SKU → GTIN/UPC/ASIN 映射 |
| `--image-base-url` | 空 | 主图 URL 基址 |
| `--browse-node` | 空 | Amazon 类目节点 |
| `--brand` | `TrailHarbor` | 1688/Generic 行使用的消费品牌 |
| `--strict` | 关闭 | CSV 格式错误时退出码 2 |
| `--log-level` | `INFO` | 日志级别 |

修改 `amazon_listing_profile.yaml` 时：

- `key` 是内部字段名，不要改；
- `header` 改成 Seller Central 模板实际表头；
- `required_value`、`max_length`、`type`、`enum` 按模板调整；
- 站点 `filename` 可按团队命名调整。

---

## 8. 测试与验证

```bash
pytest tests/test_listing_generator.py -q
python listing_generator.py --locales en-US
python listing_generator.py --locales all
```

测试覆盖：

- 读取选品表只保留通过门槛行；
- 60 列 US CSV 表头与 profile 一致；
- 5 点完整、标题/详情/搜索词长度合规；
- 无残留违禁词；
- 四个站点分别生成 CSV 与本地化标题；
- 补齐 GTIN、图片、Browse Node 后 `import_ready=true`；
- 违禁词 scanner 自动替换并标记。

---

## 9. 已知限制

- Amazon 类目模板随站点/类目/时间变化，必须用当前模板复核 profile；
- 选品表没有 GTIN、主图、尺寸、AC 口数量、认证编号；
- 模块不会伪造这些字段，默认以 blocker/warning 呈现；
- DE/FR 文案为模板级本地化，必须母语审校；
- GPSR、WEEE、电池运输、CE/UKCA/FCC/UL 等合规结论需持证服务商确认；
- 锂电池危险品分类默认 `unknown`，不要直接当作可运输结论。
````

## `docs/architecture.md`

````markdown
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
````

## `docs/competitor_monitor.md`

````markdown
# 竞品监控自动化模块运行说明

## 1. 模块定位

`competitor_monitor.py` 是独立的竞品公开数据监控模块：

```text
自定义公开商品链接
  → 按可配置频率巡检
  → 抓取公开价格 / BSR 或公开排名 / 公开差评
  → 与上次状态比较
  → 价格/排名异动生成 TXT 预警
  → 差评痛点分类 + 高频词 + Markdown/JSON 报告
```

### 数据边界

- 仅读取竞品对外公开的商品页和公开评论页；
- 不登录、不调用商家后台 API、不使用商家权限；
- 不绕过验证码、登录墙、Cookie 校验或访问控制；
- 抓取前检查 `robots.txt`，按域名限速；
- 公开页面无法访问、结构变化或 robots 禁止时跳过该链接，继续处理其他竞品；
- 默认 `offline` 使用本地公开快照演示，真实监控需 `--mode live`。

> 公开页面可能随时改版，也可能对自动化访问设限。监控结果是公开数据快照，
> 不是平台后台数据，也不保证与卖家实际成交/库存一致。

---

## 2. 文件位置

| 文件 | 用途 |
| --- | --- |
| `competitor_monitor.py` | 独立入口：链接管理、巡检、预警、痛点分析 |
| `config/competitor_monitor.yaml` | 频率、阈值、路径、痛点分类、演示竞品 |
| `data/competitors/competitors.json` | 竞品链接注册表 |
| `data/competitors/state.json` | 上一次成功巡检状态（运行时生成） |
| `data/mock/competitor_public_snapshots.json` | 离线基线快照 |
| `data/mock/competitor_public_snapshots_changed.json` | 离线变更快照，用于验证预警 |
| `docs/competitor_monitor.md` | 本说明 |
| `tests/test_competitor_monitor.py` | 链接管理、巡检、预警、容错、解析测试 |
| `outputs/monitor/` | 快照、预警、报告、日志 |

---

## 3. 快速运行

```bash
cd outdoor_ess_ai
python -m pip install -r requirements.txt

# 查看当前竞品
python competitor_monitor.py list

# 添加公开商品链接
python competitor_monitor.py add "https://www.amazon.com/dp/B0XXXXXXXX" \
  --name "竞品 A" --platform auto

# 执行一轮巡检
python competitor_monitor.py run

# 按 6 小时循环巡检
python competitor_monitor.py schedule --interval-hours 6
```

默认配置 `monitor.mode=offline`，第一次运行会使用演示快照建立基线；
第二次使用变更快照可验证价格/排名预警：

```bash
python competitor_monitor.py run
python competitor_monitor.py run \
  --fixture data/mock/competitor_public_snapshots_changed.json
```

真实监控：

```bash
python competitor_monitor.py run --mode live
python competitor_monitor.py schedule --interval-hours 6 --mode live
```

---

## 4. 添加/删除竞品

### 4.1 添加

```bash
python competitor_monitor.py add "https://www.amazon.com/dp/B0XXXXXXXX" \
  --name "Amazon 300Wh 竞品" \
  --price-pct 3.5 \
  --price-abs 5 \
  --rank-abs 20
```

支持平台自动识别：

| 平台 | URL 特征 | 解析重点 |
| --- | --- | --- |
| Amazon | `/dp/ASIN`、`/gp/product/ASIN` | 价格、BSR、公开评论页 |
| AliExpress | `/item/数字ID.html` | 价格、公开评论 |
| 1688 | `/offer/数字ID.html` | 公开批发价、公开成交/评论、排名（若有） |
| Generic | 其他公开商品页 | JSON-LD / meta / 通用价格与评论选择器 |

`--platform auto` 无法识别时会归为 `generic`，仍可尝试 JSON-LD 解析。
重复 URL 会被拒绝；无效 URL 不会写入注册表。

### 4.2 查看

```bash
python competitor_monitor.py list
```

### 4.3 删除

```bash
python competitor_monitor.py remove <竞品ID>
python competitor_monitor.py remove <完整URL>
python competitor_monitor.py remove --all-demo
```

---

## 5. 巡检频率

配置：

```yaml
monitor:
  interval_hours: 6.0
```

命令行覆盖：

```bash
# 每 6 小时
python competitor_monitor.py schedule --interval-hours 6

# 每 2 小时
python competitor_monitor.py schedule --interval-hours 2

# 只跑一轮，用于测试/CI
python competitor_monitor.py schedule --interval-hours 6 --max-cycles 1
```

- `run` 是单轮巡检；
- `schedule` 是进程内循环，执行完立即开始计时；
- 等待时长会扣除本轮执行耗时，按“开始到开始”的固定节拍运行；
- 每轮内部异常不会终止循环；单个链接失败不会影响其他竞品；
- `Ctrl+C` 可停止；
- 如果生产环境需要跨机器/重启后仍运行，建议用 Windows 任务计划、
  systemd timer 或 Airflow 等外部调度器调用 `run`。

---

## 6. 采集字段与解析

每次成功巡检保存：

```text
outputs/monitor/snapshots/<run_id>/<competitor_id>.json
outputs/monitor/snapshots/latest_<competitor_id>.json
```

字段：

- `title`：公开商品标题；
- `price` / `currency`：公开价格与币种；
- `bsr` / `bsr_category`：Amazon Best Sellers Rank 或页面公开排名；
- `rating` / `review_count`：公开评分与评论数；
- `reviews`：公开差评/评论样本；
- `source_url` / `platform` / `captured_at`。

解析策略：

1. JSON-LD `Product` / `Offer` / `AggregateRating`；
2. `meta[property='product:price:amount']`；
3. Amazon/AliExpress/1688 常见价格与评论选择器；
4. Amazon 公开评论页 `product-reviews/{ASIN}?filterByStar=critical`（仅一页、无登录）；
5. 页面结构变化或无反爬访问时记录失败，不伪造数据。

> 非 Amazon 平台不一定有 BSR；报告会以空值/警告呈现，不强行生成排名。

---

## 7. 价格/排名预警

默认阈值：

```yaml
monitor:
  price_threshold_pct: 3.0
  price_threshold_abs: 5.0
  rank_threshold_abs: 20
```

触发规则：

```text
价格：|新价-旧价| / 旧价 × 100 >= price_threshold_pct
  或 |新价-旧价| >= price_threshold_abs

BSR：|旧排名-新排名| >= rank_threshold_abs
```

绝对价格阈值按页面原币种比较（CNY 行不会自动换算成 USD）。

- 首次巡检只建立基线，不预警；
- 币种不同不比较价格；
- BSR 类目变化时不比较排名；
- 每个竞品可单独覆盖阈值（`add --price-pct/--price-abs/--rank-abs`）。

输出：

```text
outputs/monitor/alerts/<run_id>_<competitor_id>_PRICE.txt
outputs/monitor/alerts/<run_id>_<competitor_id>_BSR.txt
outputs/monitor/alerts/latest_alerts.txt
```

单条 TXT 示例：

```text
[竞品监控预警]
竞品名称：Amazon 300Wh 竞品
链接：https://www.amazon.com/dp/B0XXXXXXXX
预警类型：PRICE
变动：价格下降：USD 299.00 → 279.00（6.69%）
旧值：299.0
新值：279.0
```

---

## 8. 差评痛点分析

### 8.1 负评筛选

只分析公开评论中：

```text
rating <= monitor.negative_rating_threshold（默认 2）
```

### 8.2 分类词典

`config/competitor_monitor.yaml` 的 `pain_categories` 可自定义，默认覆盖：

- 电池与续航；
- 充电速度/充电器；
- 太阳能充电；
- 噪音/风扇；
- 输出功率/过载；
- 重量/便携性；
- 做工/耐用性；
- 显示/App；
- 发热/安全；
- 物流/包装；
- 客服/售后；
- 说明书/上手；
- 接口/兼容性；
- 价格/性价比；
- 其他/未分类。

每条负评可命中多个类别，报告按提及次数排序；`share_pct` 是提及数/差评样本数。

### 8.3 输出

```text
outputs/monitor/reports/pain_points_<run_id>.md
outputs/monitor/reports/pain_points_<run_id>.json
outputs/monitor/reports/latest_pain_points.md
outputs/monitor/reports/latest_pain_points.json
```

报告包含：

1. 高频痛点总览；
2. 分类样例（截断原声，保留竞品与星级）；
3. 竞品对比（每家负评数 + Top 3 痛点）；
4. 高频词；
5. 建议动作；
6. 抓取失败/跳过链接。

> 规则分类是辅助分析，不替代人工质检；评论样本非全量，不能推断整体满意度。

---

## 9. 配置参数

| 配置 | 默认 | 说明 |
| --- | --- | --- |
| `monitor.interval_hours` | 6.0 | 巡检频率 |
| `monitor.mode` | offline | offline / live / auto |
| `monitor.respect_robots` | true | 是否遵守 robots.txt |
| `monitor.request_delay_seconds` | 2.0 | 同域请求间隔 |
| `monitor.timeout_seconds` | 20 | 请求超时 |
| `monitor.max_reviews_per_competitor` | 20 | 每个竞品最多保留评论 |
| `monitor.negative_rating_threshold` | 2 | 差评星级上限 |
| `monitor.price_threshold_pct` | 3.0 | 价格百分比阈值 |
| `monitor.price_threshold_abs` | 5.0 | 价格绝对阈值 |
| `monitor.rank_threshold_abs` | 20 | BSR 绝对变动阈值 |
| `monitor.max_pain_examples` | 3 | 每类最多样例 |
| `paths.*` | 见 YAML | 注册表/状态/快照/预警/报告路径 |

---

## 10. 容错行为

- 注册表中存在的无效 URL：加载时收进 `invalid_entries`，本轮记录失败，不中断；
- `add` 时无效 URL：直接拒绝并返回非零；
- 单个竞品 404/403/429/验证码/robots 禁止：跳过并写失败记录；
- 离线快照缺少某个自定义链接：该链接失败，其他竞品继续；
- 单轮调度异常：`schedule` 捕获后继续下一轮；
- `Ctrl+C`：正常退出；
- `--max-cycles 1`：便于 CI 验证，不进入睡眠。

---

## 11. 测试

```bash
pytest tests/test_competitor_monitor.py -q
python competitor_monitor.py run
python competitor_monitor.py schedule --max-cycles 1 --interval-hours 6
python scripts/check_syntax.py --root .
```

覆盖：

- 平台识别与自定义链接添加/删除；
- 无效链接跳过；
- 基线 → 变更快照产生 6 条价格/BSR 预警；
- 预警 TXT 内容；
- 差评痛点分类与报告生成；
- 6 小时间隔校验与单轮调度；
- 公开商品页价格/BSR/评论解析。

---

## 12. 合规提醒

- 仅使用公开可见数据；不登录、不使用店铺后台权限；
- 评论原声可能受版权/隐私规则约束，报告中仅截取短语并标注竞品；
- 价格、BSR、评论数是时点快照，可能因地区、登录状态、AB 测试、促销而变化；
- 认证、专利、商标、比价结论需人工复核；
- 生产使用前请确认目标网站的服务条款与 robots 规则。
````

## `docs/compliance_check.md`

````markdown
# 合规校验模块运行说明

## 1. 模块定位

`compliance_check.py` 对模拟产品参数做 CE/FCC 规则初筛，输出：

```text
产品参数 + 认证资料状态
  → 适用标准/指令匹配
  → 不符合项、风险级别、修改建议
  → 合规汇总 Excel + JSON
```

### 重要边界

- CE 不是一张“证书”，而是适用指令/法规下的符合性评估、技术文件与自我声明；
- FCC 按设备类型区分 SDoC 与认证（FCC ID）；
- 本模块只做规则初筛，不替代测试实验室、认证机构、律师、海关或平台审核；
- 产品认证状态为模拟数据，不能作为真实合规结论；
- 规则不构成法律意见。

---

## 2. 文件

| 文件 | 用途 |
| --- | --- |
| `compliance_check.py` | 规则引擎、Excel/JSON 输出 |
| `config/compliance_rules.yaml` | 标准清单、阈值、风险权重 |
| `data/mock/product_compliance_master.json` | 9 个 SKU 的模拟合规参数 |
| `outputs/compliance/compliance_check.xlsx` | 汇总、不符合项、产品参数、标准依据 |
| `outputs/compliance/compliance_summary.json` | 机器可读摘要 |

---

## 3. 快速运行

```bash
cd outdoor_ess_ai
python -m pip install -r requirements.txt
python compliance_check.py
```

指定输入/输出：

```bash
python compliance_check.py \
  --selection outputs/research/high_potential_products.xlsx \
  --master data/mock/product_compliance_master.json \
  --output outputs/compliance/compliance_check.xlsx \
  --json outputs/compliance/compliance_summary.json
```

`--strict`：存在高风险项时退出码 2，适合 CI。

---

## 4. 检查范围

### 4.1 欧盟 CE 相关

| 规则 | 标准/法规 | 检查点 |
| --- | --- | --- |
| LVD | 2014/35/EU | 输出电压/频率、LVD 报告、CE 标记 |
| EMC | 2014/30/EU | EMC 报告 |
| RoHS | 2011/65/EU | 均质材料检测/声明 |
| WEEE | 2012/19/EU | 成员国注册、回收标识 |
| Battery | (EU) 2023/1542 | 电池文件、碳足迹/标签/护照路线 |
| GPSR | (EU) 2023/988 | 风险评估、EU 责任人、追溯 |
| RED | 2014/53/EU | 无线模块测试与 DoC |
| 说明书语言 | 目标市场要求 | 至少覆盖 en/de/fr |

### 4.2 美国 FCC 相关

| 规则 | 标准 | 检查点 |
| --- | --- | --- |
| Part 15B | 47 CFR Part 15 Subpart B | 无意辐射体测试、SDoC |
| Part 15C | 47 CFR Part 15 Subpart C | 无线模块 FCC ID |
| FCC 标签 | Part 15 | 标签/说明书声明 |
| UL 2743 | UL 2743 / NRTL | 便携电源安全报告（零售常用） |
| Prop 65 | California H&S Code | 化学品暴露评估/警示 |

### 4.3 通用

- UN38.3 锂电池运输测试摘要；
- IATA DGR：>100Wh 空运限制，给出建议（低风险）；
- IP 等级缺失时提示（户外场景）；
- 额定功率与宣称输出功率一致性；
- 电压/频率/插头与目标市场匹配。

---

## 5. 风险评分

```text
风险分 = 100 - 高风险数×25 - 中风险数×10 - 低风险数×5
风险分下限 0，上限 100
```

状态：

| 状态 | 条件 |
| --- | --- |
| `FAIL` | 至少 1 个高风险 |
| `CONDITIONAL` | 无高风险，但有中风险 |
| `PASS` | 无高风险/中风险（可有低风险建议） |

> 低风险通常是“建议/运输提示”，不影响 PASS。

汇总页会同时给出 `美国` / `欧盟` 两个市场状态。

---

## 6. Excel 结构

| 工作表 | 内容 |
| --- | --- |
| `合规汇总` | 每个 SKU 的高/中/低风险数、风险分、状态、美国/欧盟状态、Top 风险 |
| `不符合项` | 标准、要求、观察值、严重级别、修改建议、需要的证据 |
| `产品参数` | 电压、频率、功率、电池、无线、IP、认证资料矩阵 |
| `标准依据` | 标准范围、证据清单、公开来源 |

颜色：

- 高风险：红色；
- 中风险：黄色；
- 低风险：蓝色；
- PASS/FAIL/CONDITIONAL 用状态色。

---

## 7. 修改建议示例

- 欧盟输出 120V/60Hz：为 EU 开发 230V/50Hz 版本，或明确不在 EU 销售；
- CE 标记但无 LVD/EMC：先补测试、技术文件与 DoC，再贴 CE；
- 无线但无 FCC ID：完成 Part 15C 认证，确认模块认证覆盖整机；
- 电池 >100Wh：核对 IATA DGR、UN38.3、MSDS、航空运输鉴定；
- 无 EU 责任人：指定 GPSR 欧盟责任人并标注联系方式；
- 无 IP 等级：先测试再使用防水/防尘表述，避免虚假宣传。

---

## 8. 自定义

### 8.1 产品主数据

在 `data/mock/product_compliance_master.json` 增加/修改 SKU：

```json
{
  "sku": "SKU-001",
  "target_markets": ["US", "EU"],
  "output_voltage_v": 120,
  "output_frequency_hz": 60,
  "battery_wh": 300,
  "wireless": false,
  "has_lvd_report": false,
  "has_fcc_part15b": false
}
```

实际使用时，应把“模拟认证状态”替换为可核验的测试报告/证书编号。

### 8.2 规则

`config/compliance_rules.yaml`：

- `severity_weights`：风险权重；
- `thresholds`：电压/频率/电池阈值；
- `manual_languages`：说明书语言；
- `standards`：标准名称、范围、需要的证据、来源。

代码中的规则与标准 ID 对应；新增标准时需同步增加判断逻辑。

---

## 9. 测试

```bash
pytest tests/test_operations_reports.py::test_compliance_rules_and_scores -q
python compliance_check.py
```

测试覆盖：

- 9 个 SKU 输出；
- 风险分公式；
- 欧盟/美国状态；
- CE/FCC 不符合项；
- Excel 四个工作表与行数。

---

## 10. 合规提醒

- 本模块不提供“保证通过”的结论；
- CE 技术文件、DoC、测试报告必须由真实产品与实验室出具；
- FCC SDoC/FCC ID 的责任方与标签需按规则落实；
- 锂电池运输、GPSR、Battery Regulation 等法规存在过渡期；
- 正式上架前请让合规服务商按目标市场/型号做最终确认。
````

## `docs/final_integration.md`

````markdown
# 最终整合与本地运行说明

## 1. 系统定位

前 5 步的模块已整合成一个**本地可运行的运营工作台**：

```text
Streamlit 控制台
  ├─ 选品研究
  ├─ Amazon Listing
  ├─ 竞品监控
  ├─ CE/FCC 合规
  ├─ 经营报表
  └─ 面试演示
```

所有模块通过页面按钮或 CLI 调用，不需要手动逐个执行零散 Python 脚本。
默认使用公开快照/固定种子模拟，不接入真实店铺后台。

---

## 2. 一键启动

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\start_all.ps1
```

脚本会：

1. 检测 `.venv`、系统 Python 或 `.vendor`；
2. 首次运行时创建虚拟环境并安装 `requirements.txt`；
3. 执行 `main.py init`；
4. 启动 Streamlit（默认 `127.0.0.1:8501`）；
5. 等待 `/_stcore/health` 返回 200；
6. 打开浏览器。

常用参数：

```powershell
# 换端口，不打开浏览器
powershell -ExecutionPolicy Bypass -File .\start_all.ps1 -Port 8502 -NoBrowser

# 已安装依赖时跳过安装
powershell -ExecutionPolicy Bypass -File .\start_all.ps1 -SkipInstall

# 停止
powershell -ExecutionPolicy Bypass -File .\stop_all.ps1
```

### macOS / Linux

```bash
chmod +x start_all.sh stop_all.sh
./start_all.sh
./stop_all.sh
```

> 当前系统是“轻量单体 + 按需子进程”架构：常驻后台服务只有 Streamlit；
> 选品、Listing、合规、报表、竞品巡检由按钮调用子进程执行，执行完即退出。
> 这样不需要额外部署 Redis/Celery/数据库，面试演示更轻。

---

## 3. Streamlit 界面

启动后打开 `http://127.0.0.1:8501`。

界面采用 **Tundra / 苔原账本（A+C）** 视觉：

- 左侧 232px 苔绿导航栏，7 个模块；
- 顶部 Workspace 面包屑与 Simulated 数据标识；
- 首屏业务流：选品 → 上架 → 合规 → 经营 → 竞品；
- 3 个核心指标，不做同规格指标卡堆叠；
- “待处理”行动队列；
- 右侧合规状态、Listing readiness、深色运行日志抽屉；
- 表格、状态胶囊、按钮统一为低饱和苔绿 + 墨色体系。

| 导航 | 一键动作 | 展示内容 |
| --- | --- | --- |
| 总览 | 运行全链路 | 业务流、核心指标、行动队列、Top 5 利润、日志 |
| 选品研究 | 运行选品 | 高潜力 Excel、毛利/容量/竞争度 |
| 上架素材 | 生成 Listing | 四站点 CSV、校验报告、预览 |
| 竞品监控 | 巡检竞品 | 预警 TXT、痛点 Markdown |
| 合规校验 | 合规筛查 | 风险分、不符合项、修改建议 |
| 经营报表 | 生成报表 | 广告/库存/利润 Excel |
| 面试演示 | 生成演示脚本 | JD 能力映射、讲解话术 |

每次运行会：

- 在页面显示命令输出；
- 成功/失败提示；
- 失败写入 `outputs/logs/errors.log`；
- 运行记录写入 `outputs/logs/ui_commands.log`；
- 重新加载最新 Excel/JSON。

所有表格支持页面预览和下载。

---

## 4. 全链路一键运行

总览页的“运行全链路”按顺序执行：

1. `main.py demo`：基础 7 阶段流水线；
2. `product_research.py`：公开数据选品；
3. `listing_generator.py --locales all`：四站点 Listing；
4. `compliance_check.py`：CE/FCC 合规；
5. `report_generator.py`：广告/库存/利润报表；
6. `competitor_monitor.py run`：竞品单轮巡检。

每一步失败会中断并提示，错误写入全局日志。

---

## 5. 全局异常捕获

`error_guard.py` 提供：

- `install_global_handler(app)`：`sys.excepthook` + `threading.excepthook`；
- `run_cli(main, app)`：所有 CLI 入口的统一包装；
- `log_exception(...)`：写入人类可读日志和 JSONL；
- `log_command_error(...)`：Streamlit 子进程失败记录。

日志：

```text
outputs/logs/errors.log       # 人类可读 traceback
outputs/logs/errors.jsonl     # 结构化：时间/模块/异常/argv/上下文/traceback
outputs/logs/ui_commands.log  # UI 每次按钮命令的退出码/耗时
outputs/logs/streamlit.err.log
```

已接入入口：

- `main.py`
- `product_research.py`
- `listing_generator.py`
- `competitor_monitor.py`
- `compliance_check.py`
- `report_generator.py`
- `interview_demo.py`
- `scripts/check_syntax.py`
- `scripts/export_bundle.py`
- `app.py`（页面级 try/except）

---

## 6. 面试演示

```bash
python interview_demo.py            # 执行全部模块 + 生成讲稿
python interview_demo.py --no-run   # 只基于现有产物生成讲稿
python interview_demo.py --quick    # 跳过基础 7 阶段流水线
```

输出：

```text
outputs/interview/interview_demo.md
outputs/interview/interview_demo.json
```

讲稿包含：

- 30 秒项目定位；
- 架构图；
- 5 分钟演示顺序；
- 每个模块对应 JD 能力点；
- 讲解话术；
- 面试官追问；
- 指标看板；
- 数据边界与风险控制；
- 结束语。

JD 映射：

| 模块 | JD 能力点 |
| --- | --- |
| 选品 | 市场调研、数据分析、选品模型、Excel |
| Listing | Amazon 运营、SEO、本地化、合规文案 |
| 合规 | CE/FCC、认证与测试、风险控制、法规意识 |
| 经营报表 | 广告、库存、财务、ROI、经营分析 |
| 竞品监控 | 竞品分析、公开数据采集、预警 |
| 基础流水线 | Python 自动化、系统集成、工程化 |

---

## 7. 新增/修改文件

| 文件 | 用途 |
| --- | --- |
| `app.py` | Streamlit 控制台 |
| `start_all.ps1` / `start_all.sh` | 一键启动 |
| `stop_all.ps1` / `stop_all.sh` | 停止服务 |
| `.streamlit/config.toml` | 关闭 developmentMode，固定本地地址 |
| `error_guard.py` | 全局异常捕获 |
| `interview_demo.py` | 面试演示脚本 |
| `docs/final_integration.md` | 本说明 |
| `docs/interview_demo` 输出 | 生成后的讲稿 |

---

## 8. 校验

```bash
pytest -q
python scripts/check_syntax.py --root .
python -m ruff check .
```

手工验证：

```powershell
powershell -ExecutionPolicy Bypass -File .\start_all.ps1 -Port 8503 -NoBrowser -SkipInstall
Invoke-WebRequest http://127.0.0.1:8503/_stcore/health
powershell -ExecutionPolicy Bypass -File .\stop_all.ps1
```

Streamlit 页面已通过 `streamlit.testing.v1.AppTest` 验证：

- 0 页面异常；
- 左侧 7 个模块导航 + 经营报表 3 个子标签；
- 每个模块一个主操作按钮；
- 点击“运行选品”和“运行全链路”均成功执行。

---

## 9. 常见问题

### Q1：端口被占用？

```powershell
powershell -ExecutionPolicy Bypass -File .\start_all.ps1 -Port 8505
```

或停止旧进程：

```powershell
powershell -ExecutionPolicy Bypass -File .\stop_all.ps1
```

### Q2：Streamlit 提示 `developmentMode`？

项目已包含 `.streamlit/config.toml` 并设置：

```toml
[global]
developmentMode = false
```

启动脚本也显式传入 `--global.developmentMode false`。

### Q3：按钮执行失败？

查看：

```text
outputs/logs/errors.log
outputs/logs/ui_commands.log
outputs/logs/streamlit.err.log
```

### Q4：可以接真实店铺后台吗？

当前刻意不接。架构上采集、存储、报表均可替换适配器；接入真实 API 需要授权、密钥、权限与合规评审。
````

## `docs/operations_reports.md`

````markdown
# 经营报表自动化模块运行说明

## 1. 模块定位

`report_generator.py` 基于选品表生成三份模拟经营报表：

```text
广告投放日报
库存预警表
月度利润核算表（含 ROI、库存周转天数）
```

所有经营数据由固定种子模拟，不接入真实店铺、广告、库存或 ERP 后台。

---

## 2. 文件与输出

| 文件 | 用途 |
| --- | --- |
| `report_generator.py` | 经营模拟、指标计算、Excel 输出 |
| `config/report_generator.yaml` | 周期、种子、广告/库存/成本假设 |
| `outputs/operations/ad_daily_report.xlsx` | 广告日报 |
| `outputs/operations/inventory_alert.xlsx` | 库存预警 |
| `outputs/operations/monthly_profit.xlsx` | 月度利润 + 经营概览 |
| `outputs/operations/report_summary.json` | 汇总指标与 9 个 SKU 明细 |

---

## 3. 快速运行

```bash
cd outdoor_ess_ai
python -m pip install -r requirements.txt
python report_generator.py
```

自定义：

```bash
python report_generator.py \
  --seed 42 \
  --period-end 2026-09-30 \
  --days 30 \
  --output-dir outputs/operations
```

参数：

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--input` | `outputs/research/high_potential_products.xlsx` | 选品表 |
| `--config` | `config/report_generator.yaml` | 模拟参数 |
| `--output-dir` | `outputs/operations` | 输出目录 |
| `--seed` | `20261021` | 固定随机种子 |
| `--period-end` | `2026-09-30` | 报表截止日 |
| `--days` | `30` | 周期天数 |
| `--log-level` | `INFO` | 日志级别 |

---

## 4. 模拟逻辑

### 4.1 广告日报

每个 SKU、每一天生成：

- 展示、点击、CTR、CPC；
- 广告花费、广告订单、CVR；
- 广告销售额、ACOS、ROAS；
- 广告贡献毛利。

计算关系：

```text
CTR  = 点击 ÷ 展示
CVR  = 广告订单 ÷ 点击
ACOS = 广告花费 ÷ 广告销售额
ROAS = 广告销售额 ÷ 广告花费
广告贡献毛利 = 广告销售额 × 参考毛利率 - 广告花费
```

模拟时先按目标 ACOS 区间（12%-22%）生成花费，再由 CVR 反推点击、由 CTR 反推展示，确保指标自洽。

### 4.2 库存预警

```text
日均销量 = 30 天销量 ÷ 30
覆盖天数 = (在库 + 在途) ÷ 日均销量
再订货点 = 日均销量 × (交期 + 安全天数)
周转天数 = 平均库存件数 ÷ 日均销量
年化周转 = 365 ÷ 周转天数
建议补货 = max(0, 目标库存 - (在库 + 在途))
目标库存 = 日均销量 × (交期 + 安全天数 + 30)
```

状态：

| 状态 | 条件 |
| --- | --- |
| 紧急补货 | 覆盖天数 < 交期 |
| 关注 | 覆盖天数 < 交期 + 安全天数 |
| 滞销 | 覆盖天数 > 90 天 |
| 健康 | 其他 |

### 4.3 月度利润

```text
收入 = 销量 × 售价
COGS = 销量 × 到岸成本
毛利 = 收入 - COGS
平台佣金 = 收入 × 15%
履约 = 销量 × (3 + 重量 × 1.8)
退款 = 收入 × 3%
仓储 = 平均库存金额 × 1%
其他 = 收入 × 1%
净利润 = 收入 - COGS - 佣金 - 履约 - 广告 - 退款 - 仓储 - 其他
净利率 = 净利润 ÷ 收入
ROI = 净利润 ÷ 总成本
总成本 = COGS + 佣金 + 履约 + 广告 + 退款 + 仓储 + 其他
```

> 这里的“毛利”是商品口径（未扣平台佣金/履约/广告）；广告日报的“参考毛利率”来自选品表的贡献毛利口径。Excel 指标说明会标注差异。

### 4.4 核心指标

- **ROI**：净利润 ÷ 总成本；不是“销售额/花费”。
- **库存周转天数**：平均库存件数 ÷ 日均销量（30 天口径）。
- **广告 ACOS**：广告花费 ÷ 广告销售额。
- **广告 ROAS**：广告销售额 ÷ 广告花费。
- **覆盖天数**：含在途库存，用于补货决策。

---

## 5. Excel 结构

### 5.1 广告日报

工作表：`广告日报` + `指标说明`

字段：

日期、星期、平台、SKU、商品、市场、展示、点击、CTR、CPC、广告花费、广告订单、CVR、广告销售额、ACOS、ROAS、广告贡献毛利、参考毛利率。

底部有合计行；ACOS 列有颜色刻度（越低越绿）。

### 5.2 库存预警

工作表：`库存预警` + `指标说明`

字段：

SKU、商品、平台、市场、30 天销量、日均销量、期初库存、在库、在途、覆盖天数、交期、安全天数、再订货点、建议补货、库存金额、库龄 >90 天、周转天数、年化周转、状态、优先级。

状态颜色：紧急补货红、关注黄、滞销灰、健康绿。

### 5.3 月度利润

工作表：`经营概览` + `月度利润` + `指标说明`

`经营概览`：

- 总销量、总收入、总广告花费、总净利润；
- 净利率、整体 ROI、广告 ACOS/ROAS；
- 库存预警 SKU 数、紧急补货 SKU 数；
- 最高 ROI SKU、最低覆盖 SKU。

`月度利润`：

SKU、商品、平台、市场、销量、收入、COGS、毛利、毛利率、平台佣金、履约、广告费、退款、仓储、其他、净利润、净利率、ROI、广告 ACOS、广告 ROAS、平均库存、库存周转天数、年化周转、库存金额。

底部有合计行；ROI 列有颜色刻度。

---

## 6. 配置

`config/report_generator.yaml`：

| 配置 | 默认 | 说明 |
| --- | --- | --- |
| `simulation.seed` | 20261021 | 固定随机种子 |
| `simulation.period_end` | 2026-09-30 | 截止日 |
| `simulation.days` | 30 | 周期天数 |
| `simulation.target_share` | 0.08 | 市场容量中目标份额 |
| `simulation.target_acos_range` | [0.12, 0.22] | 广告 ACOS 区间 |
| `simulation.cvr_range` | [0.04, 0.10] | 广告 CVR 区间 |
| `simulation.ctr_range` | [0.004, 0.012] | 广告 CTR 区间 |
| `simulation.lead_time_choices` | [25,30,35,40] | 供应商交期 |
| `simulation.safety_days` | 14 | 安全库存天数 |
| `cost.platform_fee_rate` | 0.15 | 平台佣金 |
| `cost.return_rate` | 0.03 | 退款率 |
| `cost.storage_rate_month` | 0.01 | 月仓储费率 |
| `cost.other_rate` | 0.01 | 其他费用率 |

---

## 7. 测试与校验

```bash
pytest tests/test_operations_reports.py::test_operations_formulas_and_excel -q
python report_generator.py
```

测试断言：

- 30 天 × 9 SKU = 270 条广告日报；
- CTR/CVR/CPC/ACOS/ROAS 公式自洽；
- 收入 = 销量 × 售价；
- 毛利 = 收入 - COGS；
- 净利润 = 收入 - 总成本；
- ROI = 净利润 ÷ 总成本；
- 周转天数 = 平均库存 ÷ 日均销量；
- 覆盖天数 = (在库+在途) ÷ 日均销量；
- 再订货点公式；
- 库存状态与覆盖天数一致；
- 三个 Excel 的工作表、行数、表头正确。

---

## 8. 使用边界

- 数据为固定种子模拟，不代表真实经营结果；
- 成本率、广告 ACOS、库存覆盖等是可调假设，面试展示时应说明假设；
- 实际使用时需替换为真实订单、广告、库存和财务数据；
- 平台佣金、仓储费、退货率因站点/类目/履约方式不同，应按实际合同调整。
````

## `docs/product_research.md`

````markdown
# 选品自动化模块运行说明

## 1. 模块定位

`product_research.py` 是户外露营**轻量化储能（100-500Wh）**的独立选品模块，完成：

```text
公开数据采集/快照 → 字段清洗 → 单 SKU 毛利 → 市场容量 → 竞争度
→ 综合机会分 → 高潜力筛选 → 结构化 Excel
```

它不依赖主项目的 7 阶段流水线，可以单独运行，也可以被其他脚本 import。

### 数据边界

- 仅处理 Amazon、AliExpress、1688 的**公开可见搜索页**或本地公开快照；
- 不登录卖家后台，不调用平台店铺 API；
- 不绕过验证码、登录墙、Cookie 校验或访问控制；
- live 抓取前检查 `robots.txt`，按域名限速；
- 遇到 403/429/验证码会停止该平台，不会换代理或伪造身份；
- 默认 `offline` 模式读取 `data/mock/public_research_snapshot.json`，数据为演示用途。

> 公开页面结构经常变化，也常对自动化访问设限。live 模式是“合规优先的尽力抓取”，
> 不保证每次都能获取；生产使用应优先考虑平台授权数据、人工导出或合规数据服务商。

---

## 2. 文件位置

| 文件 | 用途 |
| --- | --- |
| `product_research.py` | 独立入口：抓取、清洗、指标、Excel、CLI |
| `config/product_research.yaml` | 平台、成本、筛选、评分、输出配置 |
| `data/mock/public_research_snapshot.json` | 离线公开快照（26 条演示记录） |
| `docs/product_research.md` | 本说明 |
| `tests/test_product_research.py` | 清洗、指标自洽、Excel 结构测试 |
| `outputs/research/` | 运行产物目录 |

---

## 3. 安装与运行

```bash
cd outdoor_ess_ai
python -m pip install -r requirements.txt
```

### 3.1 最短运行

```bash
python product_research.py
```

默认：`offline` → 26 条公开快照 → 清洗 → 计算 → 输出 Excel/CSV/JSON。

### 3.2 常用命令

```bash
# 调整毛利率与输出数量
python product_research.py --min-margin 30 --top-n 15

# 缩小容量区间并限制重量
python product_research.py --min-wh 150 --max-wh 400 --max-weight 8

# 提高市场容量要求、降低竞争度门槛
python product_research.py --min-market-capacity 200000 --max-competition 65

# 尝试公开页面 live 抓取（失败即停止，不做绕过）
python product_research.py --mode live --limit 20

# 先尝试 live，失败回退本地公开快照
python product_research.py --mode auto

# 指定输出目录
python product_research.py --output-dir outputs/research_run2
```

### 3.3 退出码

| 退出码 | 含义 |
| --- | --- |
| 0 | 成功，正常输出 |
| 1 | 配置、抓取、清洗或导出失败 |
| 2 | 加了 `--strict` 且高潜力 SKU 为 0 |

---

## 4. 数据模式

| 模式 | 行为 | 适用场景 |
| --- | --- | --- |
| `offline` | 只读本地公开快照 | 演示、CI、可复现分析 |
| `live` | 仅请求公开搜索页；任一平台失败记录在 `live_failures`；全部失败则报错 | 小规模公开数据验证 |
| `auto` | 先尝试 live，无结果时回退快照 | 网络不稳定时的日常使用 |

live 模式使用 `requests` + `BeautifulSoup`，不执行 JavaScript，不模拟登录。
Amazon / AliExpress / 1688 的页面结构、反爬策略和 robots 规则会变化，适配器可能失效；
这不是绕过访问控制的理由。

公开搜索页通常不直接提供月搜索量、商品重量和供应商成本，因此 live 模式可能：

- 从标题解析容量/功率/重量，解析失败则降低数据质量分；
- 使用配置的 5kg 默认重量并标记 `weight_source=category_default`；
- 因缺少搜索量导致市场容量为 0，无法进入高潜力表；
- 因页面结构变化或反爬返回空结果。

生产使用时建议补充合规的关键词量数据、供应商报价和人工复核，而不是用猜测值填满。

---

## 5. 三个核心指标

### 5.1 单 SKU 毛利

```text
到岸成本 = 货源/估算成本 + 头程 + 关税 + 包装
平台佣金 = 零售基准价 × 平台费率
履约成本 = 固定履约费 + 重量 × 每公斤履约费
单件毛利 = 零售基准价 - 到岸成本 - 平台佣金 - 履约成本
毛利率 = 单件毛利 ÷ 零售基准价 × 100%
```

成本口径：

- **Amazon / AliExpress**：没有公开供应商成本，使用“公开零售价 × 配置成本率”估算，
  Excel 中 `cost_basis` 会明确标注；
- **1688**：使用公开批发价作为货源成本，零售价使用同容量段零售平台中位价作为基准；
- 头程、关税、包装、履约、平台费率均可在 `config/product_research.yaml` 调整；
- 广告费单独列为 `ad_cost_est_usd`，不混入毛利，另算贡献毛利。

### 5.2 市场容量

```text
月销量估算 = 月搜索量 × 平台转化率
市场容量 = 月销量估算 × 零售基准价
可获取容量 = 市场容量 × addressable_share（默认 15%）
```

- `月搜索量` 来自公开搜索/需求代理口径；
- 市场容量是品类级月度销售额，不等于单个 SKU 的实际销量；
- 1688 行使用目标市场零售价作为基准，便于比较“批发货源 → 零售市场”的空间；
- 转化率按平台配置，属于假设参数，需用真实投放数据校准。

### 5.3 竞争度

```text
列表密度 = log1p(竞品数量) / log1p(saturation_competitors) × 100
评论壁垒 = log1p(评论/成交数) / log1p(review_ceiling) × 100
广告压力 = 广告位数 / ad_ceiling × 100
价格离散 = 同容量段价格变异系数 / price_cv_full_scale_pct × 100
竞争度 = 0.35×密度 + 0.30×评论壁垒 + 0.20×广告压力 + 0.15×价格离散
```

- 0-100，**越高越激烈**；
- 综合机会分使用 `100 - 竞争度` 反向计分；
- 评论壁垒对 1688 使用公开成交/评价数代理，属于弱代理指标。

### 5.4 综合机会分

```text
0.35×毛利得分 + 0.25×市场得分 + 0.20×竞争机会 + 0.10×轻量得分 + 0.10×数据质量
```

默认高潜力门槛：

| 门槛 | 默认值 |
| --- | --- |
| 容量 | 100-500Wh |
| 重量 | ≤12kg（清洗上限 15kg） |
| 毛利率 | ≥25% |
| 市场容量 | ≥$120,000/月 |
| 竞争度 | ≤70 |
| 综合机会分 | ≥65 |

所有门槛都可以通过 CLI 或 YAML 覆盖。

---

## 6. 可自定义参数

### 6.1 CLI 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--config` | `config/product_research.yaml` | 配置文件 |
| `--mode` | `offline` | `offline` / `live` / `auto` |
| `--fixture` | `data/mock/public_research_snapshot.json` | 离线快照 |
| `--output-dir` | `outputs/research` | 输出目录 |
| `--limit` | `30` | 每个平台 live 抓取上限 |
| `--query` | 平台配置 | 覆盖 live 搜索词 |
| `--top-n` | `30` | 高潜表最多行数 |
| `--min-wh` / `--max-wh` | `100` / `500` | 容量区间 |
| `--max-weight` | `15` | 清洗重量上限 |
| `--min-price` / `--max-price` | `49` / `1500` | 公开价 USD 区间 |
| `--min-margin` | `25` | 最低毛利率（%） |
| `--min-market-capacity` | `120000` | 最低市场容量（USD/月） |
| `--max-competition` | `70` | 最高竞争度 |
| `--min-score` | `65` | 最低综合机会分 |
| `--strict` | 关闭 | 无高潜 SKU 时退出码 2 |
| `--log-level` | `INFO` | 日志级别 |

### 6.2 YAML 参数

| 配置段 | 关键字段 | 用途 |
| --- | --- | --- |
| `crawler` | `mode`、`delay_seconds`、`respect_robots`、`timeout_seconds` | 抓取边界 |
| `platforms` | `search_url`、`query`、`fee_rate`、`conversion_rate` | 平台适配与费率 |
| `filters` | `capacity_wh`、`max_weight_kg`、`price_per_wh_usd`、`exclude_keywords` | 清洗筛选 |
| `cost_model` | 汇率、头程、关税、包装、履约、广告比例 | 毛利测算 |
| `competition` | 权重、天花板、价格离散刻度 | 竞争度 |
| `market_capacity` | `addressable_share`、平台转化率 | 市场容量 |
| `opportunity` | 权重、`thresholds`、`top_n` | 综合分与高潜门槛 |
| `output` | 文件名 | 输出位置 |
| `fixture` | `path` | 离线公开快照 |

修改 YAML 后不需要改代码；CLI 参数会覆盖 YAML 的对应值。

---

## 7. 输出文件

```text
outputs/research/
├── high_potential_products.xlsx   # 核心交付：结构化 Excel
├── cleaned_products.csv           # 全部清洗后 SKU，便于二次分析
├── raw_public_snapshot.json       # 原始数据/抓取失败记录
├── research_summary.json          # 指标摘要、门槛、前 5 名、输出路径
└── product_research.log           # 运行日志
```

### Excel 工作表

| 工作表 | 内容 |
| --- | --- |
| `高潜力选品` | 通过全部门槛的 SKU，按综合机会分排序 |
| `全部清洗数据` | 所有清洗后 SKU，含未通过门槛的记录 |
| `指标说明` | 毛利、市场容量、竞争度、机会分的公式与门槛 |
| `筛选参数` | 本次运行的完整配置快照 |
| `数据质量` | 原始/清洗数量、平台分布、剔除原因、基准价、live 失败 |

### 核心决策字段

平台、标题、品牌、SKU、链接、目标市场、容量、功率、重量、电芯、太阳能输入、
评分、评论/成交数、卖家、原币价、USD 价、零售基准价、货源成本、到岸成本、
平台佣金、履约成本、单件毛利、毛利率、广告估算、贡献毛利率、月搜索量、
预估月销量、市场容量、可获取容量、竞品数、广告位数、竞争度、毛利/市场/
竞争/轻量/数据质量得分、综合机会分、推荐等级、门槛状态、合规提示、
成本口径、建议动作、MOQ、USD/Wh、来源页、采集时间、原始记录 ID。

---

## 8. 逻辑自洽校验

测试覆盖：

```bash
pytest tests/test_product_research.py -q
python product_research.py --mode offline
python product_research.py --mode offline --min-margin 50 --strict
```

自动断言：

- 所有 SKU 容量在 100-500Wh；
- `毛利 = 零售价 - 到岸成本 - 佣金 - 履约`（误差 ≤0.02 USD）；
- `毛利率 = 毛利 / 零售价 × 100`（误差 ≤0.05 个百分点）；
- `市场容量 = 预估月销量 × 零售价`（误差 ≤0.02 USD）；
- 竞争度在 0-100；
- 高潜表每一行都通过毛利率、市场容量、竞争度、综合分门槛；
- Excel 工作表、表头、行数与 CSV/JSON 一致。

> 这些校验保证“计算逻辑自洽”，不保证公开数据本身真实、完整或适用于你的业务。
> 认证、税务、物流与平台政策仍需人工复核。

---

## 9. 常见问题

### Q1：live 模式抓不到数据怎么办？

先看 `outputs/research/research_summary.json` 的 `live_failures` 和日志。
常见原因：robots.txt 禁止、HTTP 403/429、验证码、页面结构变化、网络不可达。
不要通过代理池、伪造 Cookie 或验证码识别绕过；改用 `auto` / `offline`，
或接入有授权的数据源。

### Q2：为什么 1688 的毛利看起来很高？

因为 1688 价格是公开批发价，零售基准价来自同容量段零售平台中位价；
没有计入你的真实头程、关税、退货、仓储、广告和运营成本。
`cost_basis` 字段会明确标注这一口径，必须用供应商报价复核。

### Q3：市场容量为什么不是本 SKU 的销量？

它是“品类级月搜索量 × 转化率 × 零售价”的 TAM 估算；
单 SKU 可获取容量还要乘 `addressable_share`，并受listing、评价、广告影响。

### Q4：可以改容量/重量/毛利率门槛吗？

可以。CLI 参数优先，其次改 `config/product_research.yaml`：
`filters.capacity_wh`、`filters.max_weight_kg`、`opportunity.thresholds`。

### Q5：Excel 打不开或提示缺少 openpyxl？

```bash
python -m pip install "openpyxl>=3.1,<4.0"
```
````

## `error_guard.py`

````python
"""全局异常捕获与错误日志。

所有 CLI / Streamlit 入口都通过本模块记录未捕获异常，便于面试演示时
快速定位问题。日志写入 ``outputs/logs/errors.log`` 和 ``errors.jsonl``。
"""

from __future__ import annotations

import json
import os
import platform
import sys
import threading
import traceback
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import utils

PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "outputs" / "logs"
HUMAN_LOG = LOG_DIR / "errors.log"
JSONL_LOG = LOG_DIR / "errors.jsonl"


def log_exception(
    exc: BaseException,
    *,
    app: str,
    context: Mapping[str, Any] | None = None,
    argv: Sequence[str] | None = None,
) -> Path:
    """记录异常到人类可读日志和 JSONL；自身失败也不抛出。"""

    timestamp = datetime.now(UTC).isoformat()
    trace = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    record = {
        "timestamp": timestamp,
        "app": app,
        "exception_type": type(exc).__name__,
        "message": str(exc),
        "argv": list(argv if argv is not None else sys.argv),
        "cwd": os.getcwd(),
        "python": sys.version,
        "platform": platform.platform(),
        "context": dict(context or {}),
        "traceback": trace,
    }
    try:
        utils.ensure_dir(LOG_DIR)
        utils.write_text(
            HUMAN_LOG,
            f"\n{'=' * 80}\n[{timestamp}] {app} / {type(exc).__name__}: {exc}\n"
            f"{trace}\n",
            append=True,
        )
        utils.write_text(
            JSONL_LOG,
            json.dumps(record, ensure_ascii=False, default=str) + "\n",
            append=True,
        )
    except Exception as log_error:  # 日志失败不能覆盖原始异常
        print(f"[error_guard] 无法写入错误日志: {log_error}", file=sys.stderr)
    return HUMAN_LOG


def install_global_handler(app: str) -> None:
    """安装 sys/threading 未捕获异常钩子。"""

    original_hook = sys.excepthook

    def sys_hook(exc_type: type[BaseException], exc: BaseException, tb: Any) -> None:
        if not issubclass(exc_type, KeyboardInterrupt):
            log_exception(
                exc,
                app=app,
                context={"hook": "sys.excepthook"},
            )
        original_hook(exc_type, exc, tb)

    sys.excepthook = sys_hook

    def thread_hook(args: threading.ExceptHookArgs) -> None:
        if args.exc_value is not None:
            log_exception(
                args.exc_value,
                app=app,
                context={"hook": "threading.excepthook", "thread": args.thread.name if args.thread else ""},
            )

    threading.excepthook = thread_hook


def run_cli(
    main_func: Callable[[Sequence[str] | None], int],
    app: str,
    argv: Sequence[str] | None = None,
) -> int:
    """包装 CLI main：捕获未处理异常、写日志、返回非零退出码。"""

    install_global_handler(app)
    try:
        return int(main_func(argv))
    except KeyboardInterrupt:
        print("\n已中断。", file=sys.stderr)
        return 130
    except Exception as exc:
        log_path = log_exception(
            exc,
            app=app,
            context={"hook": "run_cli"},
        )
        print(f"✗ 未捕获异常：{type(exc).__name__}: {exc}", file=sys.stderr)
        print(f"  错误日志：{log_path}", file=sys.stderr)
        return 1


def log_command_error(
    app: str,
    command: Sequence[str],
    returncode: int,
    stdout: str,
    stderr: str,
) -> Path:
    """记录子进程失败（Streamlit 一键运行时使用）。"""

    exc = RuntimeError(f"命令执行失败，退出码 {returncode}: {' '.join(command)}")
    return log_exception(
        exc,
        app=app,
        context={
            "hook": "subprocess",
            "returncode": returncode,
            "stdout_tail": stdout[-4000:],
            "stderr_tail": stderr[-4000:],
        },
        argv=command,
    )
````

## `ess_ai/__main__.py`

````python
"""命令行入口：``python -m ess_ai``。"""

from ess_ai.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
````

## `ess_ai/analysis/market_analyzer.py`

````python
"""市场评分与选品机会分析。

评分全部为可解释的规则模型，不依赖外部 API；权重来自 ``settings.yaml``。
"""

from __future__ import annotations

from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


def _num(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


class MarketAnalyzer:
    """把标准表转换为市场排名、商品机会与进入策略。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.analysis_dir = utils.ensure_dir(settings.path("paths.analysis_dir"))

    def analyze(self, normalized: dict[str, Any]) -> dict[str, Any]:
        market_scores = self._score_markets(normalized)
        opportunities = self._score_opportunities(normalized, market_scores)
        payload = {
            "run_id": normalized.get("run_id"),
            "generated_at": utils.utc_now_iso(),
            "data_mode": normalized.get("data_mode", ""),
            "market_scores": market_scores,
            "opportunities": opportunities,
            "top_opportunities": opportunities[:5],
            "positioning": self._build_positioning(market_scores, opportunities),
            "summary": self._build_summary(market_scores, opportunities),
            "weights": self.settings.get("business.scoring_weights", {}),
        }
        payload["artifacts"] = self._persist(payload)
        logger.info("分析完成: 市场 %d 个 / 机会 %d 条", len(market_scores), len(opportunities))
        return payload

    # ------------------------------------------------------------------
    def _score_markets(self, normalized: dict[str, Any]) -> list[dict[str, Any]]:
        weights = self.settings.get("business.scoring_weights", {}) or {}
        weight_total = sum(_num(v) for v in weights.values()) or 1.0
        trend_by_market: dict[str, list[dict[str, Any]]] = {}
        for row in normalized.get("trend_summary", []):
            trend_by_market.setdefault(str(row.get("market", "")).upper(), []).append(row)

        scores: list[dict[str, Any]] = []
        for market in normalized.get("market_summary", []):
            code = str(market.get("market", "")).upper()
            trends = trend_by_market.get(code, [])
            trend_avg = (
                sum(_num(x.get("avg_last_7d")) for x in trends) / len(trends) if trends else 0.0
            )
            trend_growth = (
                sum(_num(x.get("growth_pct")) for x in trends) / len(trends) if trends else 0.0
            )
            keyword_opp = _num(market.get("avg_keyword_opportunity"))
            growth_score = _clamp(50 + trend_growth * 4)
            demand_score = _clamp(
                _num(market.get("demand_index")) * 0.55
                + keyword_opp * 0.25
                + trend_avg * 0.10
                + growth_score * 0.10
            )
            competition_score = _clamp(100 - _num(market.get("competition_index")))
            compliance_score = _clamp(100 - _num(market.get("compliance_complexity")))
            logistics_score = _clamp(100 - _num(market.get("logistics_cost_index")) * 4.2)

            cost_ratio = (
                0.48
                + _num(market.get("logistics_cost_index")) / 100 * 0.35
                + _num(market.get("import_duty_pct")) / 100
            )
            margin_ratio = _clamp(1 - cost_ratio - 0.18, 0.0, 1.0)
            margin_score = _clamp(margin_ratio / 0.35 * 100)

            overall = (
                demand_score * _num(weights.get("demand"), 0.30)
                + competition_score * _num(weights.get("competition"), 0.20)
                + margin_score * _num(weights.get("margin"), 0.25)
                + compliance_score * _num(weights.get("compliance"), 0.10)
                + logistics_score * _num(weights.get("logistics"), 0.15)
            ) / weight_total

            scores.append(
                {
                    **market,
                    "sub_scores": {
                        "demand": round(demand_score, 2),
                        "competition": round(competition_score, 2),
                        "margin": round(margin_score, 2),
                        "compliance": round(compliance_score, 2),
                        "logistics": round(logistics_score, 2),
                    },
                    "estimated_gross_margin_pct": round(margin_ratio * 100, 2),
                    "trend_avg_last_7d": round(trend_avg, 2),
                    "trend_growth_pct": round(trend_growth, 2),
                    "overall_score": round(_clamp(overall), 2),
                    "tier": "A" if overall >= 65 else ("B" if overall >= 55 else "C"),
                }
            )
        scores.sort(key=lambda item: item["overall_score"], reverse=True)
        for index, item in enumerate(scores, start=1):
            item["rank"] = index
        return scores

    def _score_opportunities(
        self,
        normalized: dict[str, Any],
        market_scores: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        markets = {str(item["market"]): item for item in market_scores}
        opportunities: list[dict[str, Any]] = []
        for product in normalized.get("products", []):
            market = str(product.get("market", "")).upper()
            market_score = markets.get(market)
            if not market_score:
                continue
            price = _num(product.get("price_usd"))
            aov = _num(market_score.get("avg_order_value_usd"), 500)
            price_ratio = price / aov if aov else 1.0
            price_fit = _clamp(100 - max(0.0, price_ratio - 0.85) * 70)
            required = product.get("compliance_required") or []
            gaps = product.get("compliance_gaps") or []
            compliance_score = (
                _clamp(100 - len(gaps) / len(required) * 100) if required else 100.0
            )
            demand = _num(market_score.get("sub_scores", {}).get("demand"))
            margin = _num(market_score.get("sub_scores", {}).get("margin"))
            portability = _num(product.get("portability_score"))
            overall = (
                demand * 0.30
                + price_fit * 0.20
                + portability * 0.20
                + compliance_score * 0.15
                + margin * 0.15
            )
            opportunities.append(
                {
                    "market": market,
                    "sku": product.get("sku"),
                    "name": product.get("name"),
                    "category": product.get("category"),
                    "price_usd": price,
                    "price_local": product.get("price_local"),
                    "currency": product.get("currency"),
                    "capacity_wh": product.get("capacity_wh"),
                    "output_w": product.get("output_w"),
                    "weight_kg": product.get("weight_kg"),
                    "solar_input_w": product.get("solar_input_w"),
                    "cycles": product.get("cycles"),
                    "warranty_years": product.get("warranty_years"),
                    "chemistry": product.get("chemistry"),
                    "use_cases": list(product.get("use_cases") or []),
                    "differentiators": list(product.get("differentiators") or []),
                    "portability_score": portability,
                    "compliance_ready": bool(product.get("compliance_ready")),
                    "compliance_required": list(product.get("compliance_required") or []),
                    "certifications": list(product.get("certifications") or []),
                    "compliance_gaps": gaps,
                    "market_score": market_score.get("overall_score"),
                    "demand_score": round(demand, 2),
                    "price_fit_score": round(price_fit, 2),
                    "compliance_score": round(compliance_score, 2),
                    "opportunity_score": round(_clamp(overall), 2),
                    "recommended_action": (
                        "优先进入"
                        if overall >= 75
                        else ("小批量测试" if overall >= 65 else "观察/补齐合规后再评估")
                    ),
                    "localization_required": market in {"DE", "FR"},
                }
            )
        opportunities.sort(key=lambda item: item["opportunity_score"], reverse=True)
        for index, item in enumerate(opportunities, start=1):
            item["rank"] = index
        return opportunities

    @staticmethod
    def _build_positioning(
        market_scores: list[dict[str, Any]],
        opportunities: list[dict[str, Any]],
    ) -> dict[str, Any]:
        if not market_scores:
            return {}
        top_market = market_scores[0]
        top_product = opportunities[0] if opportunities else {}
        lightweight = [item for item in opportunities if _num(item.get("weight_kg")) <= 10]
        return {
            "entry_market": top_market.get("market"),
            "entry_market_score": top_market.get("overall_score"),
            "entry_sku": top_product.get("sku"),
            "entry_product": top_product.get("name"),
            "positioning_angle": "轻量化户外储能 + 太阳能快充 + 静音露营用电",
            "primary_segment": "周末露营 / 轻量房车 / 家庭应急备电",
            "lightweight_candidate_count": len(lightweight),
            "price_band_focus": "mid-premium",
            "differentiation": [
                "以 10kg 以内可单人搬运作为第一筛选门槛",
                "用太阳能输入功率与充满时间作为核心对比参数",
                "用静音、循环寿命和质保年限支撑溢价",
            ],
            "risk_note": "认证与电池运输合规必须先于投放完成，不得用文案替代资质。",
        }

    @staticmethod
    def _build_summary(
        market_scores: list[dict[str, Any]],
        opportunities: list[dict[str, Any]],
    ) -> list[str]:
        if not market_scores:
            return ["无可用市场数据。"]
        top = market_scores[0]
        best = opportunities[0] if opportunities else {}
        gap_count = sum(1 for item in opportunities if item.get("compliance_gaps"))
        return [
            f"首选市场：{top.get('market')}（综合 {top.get('overall_score')} 分，{top.get('tier')} 级）。",
            f"首选单品：{best.get('name', '暂无')}（{best.get('market', '-')} / {best.get('opportunity_score', 0)} 分）。",
            f"机会池共 {len(opportunities)} 条，其中 {gap_count} 条存在认证缺口，需先补齐再投放。",
            "建议路径：US 市场小批量验证 → DE/FR 本地化与合规加严 → UK 轻量扩品。",
        ]

    # ------------------------------------------------------------------
    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        json_path = utils.write_json(self.analysis_dir / "market_analysis.json", payload)
        market_csv = utils.write_csv(
            self.analysis_dir / "market_scores.csv",
            payload["market_scores"],
            fieldnames=[
                "rank",
                "market",
                "overall_score",
                "tier",
                "estimated_gross_margin_pct",
                "trend_growth_pct",
                "demand_index",
                "competition_index",
            ],
        )
        opportunity_csv = utils.write_csv(
            self.analysis_dir / "opportunities.csv",
            payload["opportunities"],
            fieldnames=[
                "rank",
                "market",
                "sku",
                "name",
                "price_usd",
                "weight_kg",
                "opportunity_score",
                "compliance_ready",
                "recommended_action",
                "compliance_gaps",
            ],
        )
        return {
            "analysis": str(json_path.relative_to(self.settings.root)),
            "market_scores_csv": str(market_csv.relative_to(self.settings.root)),
            "opportunities_csv": str(opportunity_csv.relative_to(self.settings.root)),
        }
````

## `ess_ai/cli.py`

````python
"""命令行入口。

常用：
    python main.py init
    python main.py demo
    python main.py check
    python main.py status
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

import utils
from ess_ai.config import ConfigError, Settings, load_settings
from ess_ai.pipelines.full_chain import FullChainPipeline

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _configure_stdio() -> None:
    """在 Windows GBK 控制台下强制 UTF-8，确保中文提示可读。"""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def _setup_logging(settings: Settings) -> None:
    settings.ensure_directories()
    log_file = settings.path("paths.logs_dir") / str(
        settings.get("logging.file_name", "outdoor_ess_ai.log")
    )
    utils.setup_logging(
        level=settings.get("logging.level", "INFO"),
        log_file=log_file,
        console=bool(settings.get("logging.console", True)),
        max_bytes=int(settings.get("logging.max_bytes", 5 * 1024 * 1024)),
        backup_count=int(settings.get("logging.backup_count", 5)),
        force=True,
    )


def _cmd_init(settings: Settings) -> int:
    _setup_logging(settings)
    dirs = settings.ensure_directories()
    print(f"✓ 项目：{settings.project_name}")
    print(f"✓ 配置：{settings.config_path}")
    print(f"✓ 已准备 {len(dirs)} 个目录")
    print("下一步：python main.py demo")
    return 0


def _cmd_status(settings: Settings) -> int:
    _setup_logging(settings)
    api_key = bool(os.getenv(str(settings.get("llm.api_key_env", "DEEPSEEK_API_KEY"))))
    print(f"项目      : {settings.project_name} v{settings.get('project.version', '0.1.0')}")
    print(f"运行模式  : {settings.mode}")
    print(f"模型      : {settings.get('llm.model')}")
    print(f"API Key   : {'已配置（仅 live 模式使用）' if api_key else '未配置（离线回退可用）'}")
    print(f"目标市场  : {', '.join(settings.markets)}")
    print(f"项目根目录: {settings.root}")
    print(f"报告目录  : {settings.path('paths.reports_dir')}")
    return 0


def _cmd_demo(settings: Settings, args: argparse.Namespace) -> int:
    _setup_logging(settings)
    markets = None
    if args.markets:
        markets = [item.strip().upper() for item in args.markets.split(",") if item.strip()]
    pipeline = FullChainPipeline(settings, seed=args.seed, markets=markets)
    result = pipeline.run()
    summary = result["summary"]
    print("")
    print("=" * 68)
    print(f"✓ 全链路运行完成：{result['run_id']}")
    print(f"  首选市场：{summary.get('top_market')}（{summary.get('top_market_score')} 分）")
    print(f"  首选单品：{summary.get('top_product')}（{summary.get('top_sku')}）")
    print(f"  Listing ：{summary.get('listing_count')} 条")
    print(f"  内容包  ：{summary.get('content_pack_count')} 个")
    print(
        f"  合规    ：通过 {summary.get('compliance_passed')} / "
        f"需处理 {summary.get('compliance_failed')}（最高风险 {summary.get('highest_risk')}）"
    )
    print(f"  报告    ：{result['report_path']}")
    print(f"  清单    ：{result['manifest_path']}")
    print("=" * 68)
    return 0


def _cmd_check() -> int:
    script = PROJECT_ROOT / "scripts" / "check_syntax.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--root", str(PROJECT_ROOT)],
        cwd=str(PROJECT_ROOT),
        check=False,
    )
    return int(completed.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="outdoor-ess-ai",
        description="欧美轻量化户外储能全链路 AI 自动化系统（离线模拟版）",
    )
    parser.add_argument("--config", help="自定义 settings.yaml 路径")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="初始化目录与日志")
    sub.add_parser("status", help="查看当前运行配置")
    sub.add_parser("check", help="校验 Python/YAML/JSON 语法与项目结构")

    demo = sub.add_parser("demo", help="运行全链路离线演示")
    demo.add_argument("--seed", type=int, help="覆盖模拟随机种子")
    demo.add_argument("--markets", help="逗号分隔的市场代码，如 US,DE")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    _configure_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "check":
        return _cmd_check()
    try:
        settings = load_settings(args.config)
    except (ConfigError, utils.UtilError) as exc:
        print(f"配置加载失败：{exc}", file=sys.stderr)
        return 2

    if args.command == "init":
        return _cmd_init(settings)
    if args.command == "status":
        return _cmd_status(settings)
    if args.command == "demo":
        try:
            return _cmd_demo(settings, args)
        except Exception as exc:
            print(f"运行失败：{type(exc).__name__}: {exc}", file=sys.stderr)
            print(f"详细日志：{settings.path('paths.logs_dir')}", file=sys.stderr)
            return 1
    parser.error(f"未知命令: {args.command}")
    return 2
````

## `ess_ai/collectors/mock_collector.py`

````python
"""离线模拟采集器。

重要边界：
    - 不访问任何电商平台 API、不登录卖家后台、不抓取个人信息；
    - 所有商品、价格、趋势、竞品数据均由固定随机种子生成；
    - 输出中的 ``source_id`` 仅用于说明模拟口径，不代表真实接口。
"""

from __future__ import annotations

import math
import random
from datetime import UTC, datetime, timedelta
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)

_COMPETITOR_BRANDS = (
    "Aurora Grid",
    "PeakCell",
    "Vento Power",
    "Terravolt",
    "Kestrel Energy",
    "NomadWorks",
    "BlueRidge",
    "SolHaven",
)
_CAPACITIES = (300, 500, 600, 768, 1000, 1500, 2000)


class MockCollector:
    """读取本地 mock 商品目录，生成带来源标记的市场快照。"""

    def __init__(
        self,
        settings: Settings,
        *,
        seed: int | None = None,
        markets: list[str] | None = None,
    ) -> None:
        self.settings = settings
        self.seed = int(seed if seed is not None else settings.get("project.seed", 20260401))
        self.markets = [str(item).upper() for item in (markets or settings.markets)]
        self.mock_dir = settings.path("paths.mock_dir")
        self.raw_dir = utils.ensure_dir(settings.path("paths.raw_dir"))

    # ------------------------------------------------------------------
    # 公共入口
    # ------------------------------------------------------------------
    def collect(self, run_id: str) -> dict[str, Any]:
        """执行一次模拟采集并写入 ``data/raw``，返回内存快照。"""

        rng = random.Random(self.seed)
        catalog = self._load_json("product_catalog.json")
        keyword_doc = self._load_json("keywords.json")
        market_doc = self._load_json("market_profiles.json")

        catalog_products = [item for item in catalog.get("products", []) if isinstance(item, dict)]
        keyword_rows = [item for item in keyword_doc.get("keywords", []) if isinstance(item, dict)]
        market_profiles = [
            item
            for item in market_doc.get("markets", [])
            if isinstance(item, dict) and str(item.get("market", "")).upper() in self.markets
        ]
        if not catalog_products or not market_profiles:
            raise utils.FileIOError("mock 数据缺失：商品目录或市场档案为空")

        products = self._build_products(rng, catalog_products, market_profiles)
        trends = self._build_trends(rng, keyword_rows)
        competitors = self._build_competitors(rng, market_profiles)

        payload: dict[str, Any] = {
            "run_id": run_id,
            "generated_at": utils.utc_now_iso(),
            "data_mode": "simulated-public-proxy",
            "notice": "全部数值为离线模拟，不来自任何平台店铺 API 或真实卖家后台。",
            "seed": self.seed,
            "markets": self.markets,
            "products": products,
            "keywords": keyword_rows,
            "trends": trends,
            "competitors": competitors,
            "market_profiles": market_profiles,
            "sources": [
                "public_trend_proxy",
                "public_price_pages",
                "public_competitor_pages",
                "public_macro_energy",
            ],
        }
        payload["artifacts"] = self._persist(payload)
        logger.info(
            "采集完成: %d 个商品市场记录 / %d 条趋势 / %d 个竞品",
            len(products),
            len(trends),
            len(competitors),
        )
        return payload

    # ------------------------------------------------------------------
    # 构造数据
    # ------------------------------------------------------------------
    def _load_json(self, filename: str) -> dict[str, Any]:
        path = self.mock_dir / filename
        value = utils.read_json(path)
        if not isinstance(value, dict):
            raise utils.FileIOError(f"mock 文件根节点必须是对象: {path}")
        return value

    def _build_products(
        self,
        rng: random.Random,
        catalog_products: list[dict[str, Any]],
        market_profiles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        fx = self.settings.get("business.fx_to_usd", {}) or {}
        rows: list[dict[str, Any]] = []
        collected_at = utils.utc_now_iso()
        for market_profile in market_profiles:
            market = str(market_profile["market"]).upper()
            currency = str(market_profile.get("currency", "USD"))
            fx_rate = float(fx.get(currency, 1.0))
            vat = float(market_profile.get("vat_pct", 0)) / 100.0
            for product in catalog_products:
                target_markets = [str(x).upper() for x in product.get("target_markets", [])]
                if target_markets and market not in target_markets:
                    continue
                price_factor = rng.uniform(0.95, 1.05)
                local_price = float(product.get("msrp_usd", 0)) * fx_rate * (1 + vat) * price_factor
                local_price = max(round(local_price) - 0.01, 1.0)
                rows.append(
                    {
                        **product,
                        "market": market,
                        "currency": currency,
                        "price_local": round(local_price, 2),
                        "price_usd_est": round(local_price / fx_rate, 2),
                        "seller_count": rng.randint(8, 65),
                        "rating": round(rng.uniform(4.0, 4.8), 1),
                        "review_count": rng.randint(25, 4800),
                        "source_id": "public_price_pages/simulated",
                        "collected_at": collected_at,
                    }
                )
        return rows

    def _build_trends(
        self,
        rng: random.Random,
        keyword_rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        today = datetime.now(UTC).date()
        for keyword in keyword_rows:
            market = str(keyword.get("market", "")).upper()
            if market not in self.markets:
                continue
            base = float(keyword.get("search_index", 30))
            for offset in range(27, -1, -1):
                day_index = 27 - offset
                seasonality = 7.5 * math.sin((2 * math.pi * day_index) / 28)
                noise = rng.uniform(-4.5, 4.5)
                value = max(0.0, min(100.0, base * 0.72 + 18 + seasonality + noise))
                rows.append(
                    {
                        "date": (today - timedelta(days=offset)).isoformat(),
                        "market": market,
                        "keyword": keyword.get("keyword", ""),
                        "search_index": round(value, 1),
                        "source_id": "public_trend_proxy/simulated",
                    }
                )
        return rows

    def _build_competitors(
        self,
        rng: random.Random,
        market_profiles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for market_profile in market_profiles:
            market = str(market_profile["market"]).upper()
            brands = rng.sample(_COMPETITOR_BRANDS, k=5)
            for brand in brands:
                capacity = rng.choice(_CAPACITIES)
                price = capacity * rng.uniform(0.55, 0.95) + rng.uniform(60, 140)
                rows.append(
                    {
                        "market": market,
                        "brand": brand,
                        "title": f"{brand} {capacity}Wh Portable Power Station",
                        "capacity_wh": capacity,
                        "output_w": int(capacity * rng.uniform(0.8, 1.2)),
                        "weight_kg": round(capacity * 0.009 + rng.uniform(2.2, 4.5), 2),
                        "price_usd_est": round(price, 2),
                        "rating": round(rng.uniform(3.9, 4.8), 1),
                        "review_count": rng.randint(15, 9000),
                        "source_id": "public_competitor_pages/simulated",
                    }
                )
        return rows

    # ------------------------------------------------------------------
    # 持久化
    # ------------------------------------------------------------------
    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        artifacts: dict[str, str] = {}
        mapping = {
            "products": "products.json",
            "keywords": "keywords.json",
            "trends": "trends.json",
            "competitors": "competitors.json",
            "market_profiles": "market_profiles.json",
        }
        for key, filename in mapping.items():
            path = utils.write_json(self.raw_dir / filename, payload[key])
            artifacts[key] = str(path.relative_to(self.settings.root))
        manifest = {
            "run_id": payload["run_id"],
            "generated_at": payload["generated_at"],
            "data_mode": payload["data_mode"],
            "seed": payload["seed"],
            "counts": {key: len(payload[key]) for key in mapping},
            "files": {
                key: {
                    "path": path,
                    "sha256": utils.file_sha256(self.settings.root / path),
                }
                for key, path in artifacts.items()
            },
        }
        manifest_path = utils.write_json(self.raw_dir / "collector_manifest.json", manifest)
        artifacts["manifest"] = str(manifest_path.relative_to(self.settings.root))
        return artifacts
````

## `ess_ai/compliance/checker.py`

````python
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
````

## `ess_ai/config.py`

````python
"""配置加载与路径解析。

优先级：环境变量 > ``.env`` > ``config/settings.yaml`` > 代码内置默认值。
业务代码只依赖本模块暴露的 ``Settings``，不要自行读取 YAML。
"""

from __future__ import annotations

import copy
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import utils

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"

_REQUIRED_KEYS = (
    "project.name",
    "project.mode",
    "paths.outputs_dir",
    "paths.logs_dir",
    "llm.model",
    "business.markets",
)


class ConfigError(ValueError):
    """配置缺失、格式错误或取值非法。"""


@dataclass(frozen=True)
class Settings:
    """只读配置对象，提供点号取值和基于项目根目录的路径解析。"""

    root: Path
    data: dict[str, Any]
    config_path: Path

    def get(self, dotted: str, default: Any = None) -> Any:
        """读取配置项，例如 ``settings.get("llm.model")``。"""

        return utils.deep_get(self.data, dotted, default)

    def section(self, name: str) -> dict[str, Any]:
        """读取一个配置段，缺失时返回空字典。"""

        value = self.get(name, {})
        return dict(value) if isinstance(value, Mapping) else {}

    def path(self, dotted: str, default: str | None = None) -> Path:
        """读取路径配置并解析为绝对路径。"""

        raw = self.get(dotted, default)
        if not raw:
            raise ConfigError(f"缺少路径配置: {dotted}")
        candidate = Path(str(raw)).expanduser()
        return candidate if candidate.is_absolute() else (self.root / candidate).resolve()

    @property
    def project_name(self) -> str:
        return str(self.get("project.name", "outdoor-ess-ai"))

    @property
    def mode(self) -> str:
        return str(self.get("project.mode", "offline")).lower()

    @property
    def is_offline(self) -> bool:
        return self.mode != "live"

    @property
    def markets(self) -> list[str]:
        value = self.get("business.markets", [])
        return [str(item).upper() for item in value] if isinstance(value, list) else []

    def ensure_directories(self) -> list[Path]:
        """创建所有以 ``_dir`` 结尾的路径配置，返回去重后的目录列表。"""

        paths_section = self.section("paths")
        created: list[Path] = []
        seen: set[Path] = set()
        for key in paths_section:
            if not key.endswith("_dir"):
                continue
            target = self.path(f"paths.{key}")
            if target not in seen:
                utils.ensure_dir(target)
                seen.add(target)
                created.append(target)
        return created

    def with_root(self, new_root: str | Path) -> Settings:
        """复制配置并切换根目录，主要用于测试隔离。"""

        return Settings(root=Path(new_root).resolve(), data=copy.deepcopy(self.data), config_path=self.config_path)

    def as_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self.data)


def _load_dotenv(root: Path) -> None:
    """加载 ``.env``（不覆盖已存在的环境变量）。"""

    env_file = root / ".env"
    if not env_file.exists():
        return
    try:
        from dotenv import load_dotenv  # type: ignore[import-not-found]

        load_dotenv(env_file, override=False)
        return
    except ImportError:
        pass

    # 没有 python-dotenv 时的最小回退实现
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            os.environ.setdefault(key, value)


def _apply_env_overrides(data: dict[str, Any]) -> None:
    overrides = {
        "ESS_AI_MODE": "project.mode",
        "ESS_AI_LOG_LEVEL": "logging.level",
        "ESS_AI_MODEL": "llm.model",
        "ESS_AI_BASE_URL": "llm.base_url",
        "ESS_AI_OUTPUT_DIR": "paths.outputs_dir",
    }
    for env_name, dotted in overrides.items():
        value = os.getenv(env_name)
        if not value:
            continue
        parts = dotted.split(".")
        cursor = data
        for part in parts[:-1]:
            node = cursor.get(part)
            if not isinstance(node, dict):
                node = {}
                cursor[part] = node
            cursor = node
        cursor[parts[-1]] = value


def _validate(data: Mapping[str, Any]) -> None:
    for key in _REQUIRED_KEYS:
        if utils.deep_get(data, key) in (None, "", []):
            raise ConfigError(f"缺少必填配置: {key}")

    mode = str(utils.deep_get(data, "project.mode", "")).lower()
    if mode not in {"offline", "live"}:
        raise ConfigError("project.mode 只能是 offline 或 live")

    markets = utils.deep_get(data, "business.markets", [])
    if not isinstance(markets, list) or not markets:
        raise ConfigError("business.markets 必须是非空列表")
    allowed = set(str(x).upper() for x in utils.deep_get(data, "business.supported_markets", []))
    if allowed:
        unknown = [m for m in markets if str(m).upper() not in allowed]
        if unknown:
            raise ConfigError(f"存在未支持的市场代码: {unknown}")


def load_settings(
    config_path: str | Path | None = None,
    *,
    root: str | Path | None = None,
) -> Settings:
    """加载并校验配置，返回不可变 ``Settings``。"""

    project_root = Path(root).expanduser().resolve() if root else PROJECT_ROOT
    path = Path(config_path).expanduser() if config_path else project_root / "config" / "settings.yaml"
    if not path.is_absolute():
        path = (project_root / path).resolve()

    _load_dotenv(project_root)
    raw = utils.read_yaml(path)
    if not isinstance(raw, dict):
        raise ConfigError(f"配置文件根节点必须是映射: {path}")

    data = copy.deepcopy(raw)
    _apply_env_overrides(data)
    _validate(data)
    return Settings(root=project_root, data=data, config_path=path)
````

## `ess_ai/content/generator.py`

````python
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
````

## `ess_ai/integrations/llm_client.py`

````python
"""DeepSeek OpenAI-compatible 客户端。

默认离线：没有密钥或 ``project.mode=offline`` 时不会发起网络请求，而是返回
调用方提供的 fallback。这样演示、测试与 CI 不依赖任何外部服务。
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


class LLMError(RuntimeError):
    """大模型调用失败。"""


@dataclass(frozen=True)
class LLMResult:
    """一次补全结果，附带可审计的元信息。"""

    text: str
    model: str
    provider: str = "deepseek"
    offline: bool = False
    usage: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class DeepSeekClient:
    """最小封装：仅暴露聊天补全，避免业务层耦合 SDK 细节。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model = str(settings.get("llm.model", "deepseek-v4.1-flash"))
        self.base_url = str(
            os.getenv("DEEPSEEK_BASE_URL")
            or settings.get("llm.base_url", "https://api.deepseek.com/v1")
        )
        self.api_key_env = str(settings.get("llm.api_key_env", "DEEPSEEK_API_KEY"))
        self.api_key = os.getenv(self.api_key_env, "").strip()
        self.temperature = float(settings.get("llm.temperature", 0.3))
        self.max_tokens = int(settings.get("llm.max_tokens", 4096))
        self.timeout = float(settings.get("llm.timeout_seconds", 60))
        self.max_retries = max(0, int(settings.get("llm.max_retries", 3)))
        self.offline_fallback = bool(settings.get("llm.offline_fallback", True))

    @property
    def configured(self) -> bool:
        """是否具备发起真实请求的条件。"""

        return bool(self.api_key) and not self.settings.is_offline

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        fallback: str = "",
        temperature: float | None = None,
        json_mode: bool = False,
    ) -> LLMResult:
        """执行一次聊天补全；离线或失败时按配置回退。"""

        if not self.configured:
            return LLMResult(
                text=fallback,
                model=self.model,
                offline=True,
                error=None if not self.api_key else "project.mode=offline",
            )

        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            return self._fallback(fallback, f"openai SDK 未安装: {exc}")

        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.temperature if temperature is None else float(temperature),
            "max_tokens": self.max_tokens,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        last_error: str | None = None
        for attempt in range(self.max_retries + 1):
            try:
                client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    timeout=self.timeout,
                    max_retries=0,
                )
                response = client.chat.completions.create(**kwargs)
                text = ""
                if response.choices:
                    text = response.choices[0].message.content or ""
                usage: dict[str, Any] = {}
                raw_usage = getattr(response, "usage", None)
                if raw_usage is not None:
                    usage = (
                        raw_usage.model_dump()
                        if hasattr(raw_usage, "model_dump")
                        else dict(raw_usage)
                    )
                if not text.strip():
                    raise LLMError("模型返回空内容")
                return LLMResult(
                    text=text.strip(),
                    model=self.model,
                    usage=usage,
                )
            except Exception as exc:  # SDK 异常类型随版本变化，统一兜底
                last_error = f"{type(exc).__name__}: {exc}"
                logger.warning(
                    "DeepSeek 调用失败（第 %d/%d 次）: %s",
                    attempt + 1,
                    self.max_retries + 1,
                    last_error,
                )
                if attempt < self.max_retries:
                    time.sleep(min(2**attempt, 8))

        if self.offline_fallback:
            return self._fallback(fallback, last_error)
        raise LLMError(f"DeepSeek 调用失败: {last_error}")

    def _fallback(self, fallback: str, error: str | None) -> LLMResult:
        if not self.offline_fallback:
            raise LLMError(error or "模型不可用")
        return LLMResult(text=fallback, model=self.model, offline=True, error=error)

    def read_prompt(self, name: str) -> str:
        """从 ``prompts/`` 读取提示词模板。"""

        prompt_dir = self.settings.path("paths.prompts_dir")
        return utils.read_text(prompt_dir / name)
````

## `ess_ai/listing/optimizer.py`

````python
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
````

## `ess_ai/pipelines/full_chain.py`

````python
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
````

## `ess_ai/processing/normalizer.py`

````python
"""数据清洗与标准化。

输入为采集层的原始快照，输出为统一币种、统一口径、可分析的扁平记录。
"""

from __future__ import annotations

import statistics
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


class DataNormalizer:
    """把原始 JSON 转换为市场、商品、趋势、关键词四类标准表。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.processed_dir = utils.ensure_dir(settings.path("paths.processed_dir"))

    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        market_profiles = {
            str(item.get("market", "")).upper(): item
            for item in raw.get("market_profiles", [])
            if isinstance(item, dict)
        }
        required_by_market = self.settings.get("compliance.market_requirements", {}) or {}

        products = [
            self._normalize_product(item, market_profiles, required_by_market)
            for item in raw.get("products", [])
            if isinstance(item, dict)
        ]
        products = [item for item in products if item.get("market")]

        trends = [item for item in raw.get("trends", []) if isinstance(item, dict)]
        keywords = [self._normalize_keyword(item) for item in raw.get("keywords", []) if isinstance(item, dict)]
        competitors = [item for item in raw.get("competitors", []) if isinstance(item, dict)]

        payload = {
            "run_id": raw.get("run_id"),
            "generated_at": utils.utc_now_iso(),
            "data_mode": raw.get("data_mode", "simulated-public-proxy"),
            "notice": raw.get("notice", ""),
            "products": products,
            "trend_summary": self._summarize_trends(trends),
            "keywords": keywords,
            "competitor_summary": self._summarize_competitors(competitors),
            "market_summary": self._summarize_markets(market_profiles, products, keywords),
            "counts": {
                "products": len(products),
                "trends": len(trends),
                "keywords": len(keywords),
                "competitors": len(competitors),
                "markets": len(market_profiles),
            },
        }
        payload["artifacts"] = self._persist(payload)
        logger.info("清洗完成: %d 条商品市场记录", len(products))
        return payload

    # ------------------------------------------------------------------
    def _normalize_product(
        self,
        item: dict[str, Any],
        market_profiles: dict[str, dict[str, Any]],
        required_by_market: dict[str, Any],
    ) -> dict[str, Any]:
        market = str(item.get("market", "")).upper()
        capacity = _number(item.get("capacity_wh"))
        output_w = _number(item.get("output_w"))
        weight = _number(item.get("weight_kg"))
        price = _number(item.get("price_usd_est"))
        certifications = [str(x) for x in (item.get("certifications") or [])]
        required = [str(x) for x in (required_by_market.get(market, []) or [])]
        gaps = [cert for cert in required if cert not in certifications]

        portability = _clamp(
            100 - max(0.0, weight - 3.0) * 5.2 + min(capacity, 1500.0) / 180.0,
            0.0,
            100.0,
        )
        if capacity > 0:
            price_per_wh: float | None = round(price / capacity, 4)
        else:
            price_per_wh = None

        profile = market_profiles.get(market, {})
        return {
            **item,
            "market": market,
            "capacity_wh": int(capacity),
            "output_w": int(output_w),
            "weight_kg": round(weight, 3),
            "price_usd": round(price, 2),
            "price_local": round(_number(item.get("price_local"), price), 2),
            "price_per_wh": price_per_wh,
            "power_density_w_kg": round(output_w / weight, 3) if weight > 0 else 0.0,
            "portability_score": round(portability, 2),
            "is_lightweight": bool(weight and weight <= 10.0),
            "is_high_capacity": capacity >= 1000,
            "price_band": "budget" if price < 400 else ("mid" if price <= 800 else "premium"),
            "language": profile.get("language", "en"),
            "compliance_required": required,
            "compliance_gaps": gaps,
            "compliance_ready": not gaps,
        }

    @staticmethod
    def _normalize_keyword(item: dict[str, Any]) -> dict[str, Any]:
        search_index = _number(item.get("search_index"))
        difficulty = _number(item.get("difficulty"))
        return {
            **item,
            "market": str(item.get("market", "")).upper(),
            "search_index": round(search_index, 1),
            "difficulty": round(difficulty, 1),
            "cpc_usd": round(_number(item.get("cpc_usd")), 2),
            "opportunity_index": round(search_index * 0.6 + (100 - difficulty) * 0.4, 2),
            "source_id": "public_trend_proxy/simulated",
        }

    @staticmethod
    def _summarize_trends(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in rows:
            key = (str(row.get("market", "")).upper(), str(row.get("keyword", "")))
            grouped.setdefault(key, []).append(row)

        summary: list[dict[str, Any]] = []
        for (market, keyword), items in sorted(grouped.items()):
            ordered = sorted(items, key=lambda x: str(x.get("date", "")))
            values = [_number(x.get("search_index")) for x in ordered]
            if not values:
                continue
            first = values[0]
            last = values[-1]
            growth = ((last - first) / first * 100.0) if first else 0.0
            summary.append(
                {
                    "market": market,
                    "keyword": keyword,
                    "days": len(values),
                    "avg_index": round(statistics.fmean(values), 2),
                    "avg_last_7d": round(statistics.fmean(values[-7:]), 2),
                    "growth_pct": round(growth, 2),
                    "volatility": round(statistics.pstdev(values), 2),
                    "peak_index": round(max(values), 1),
                }
            )
        return summary

    @staticmethod
    def _summarize_competitors(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            grouped.setdefault(str(row.get("market", "")).upper(), []).append(row)
        summary: list[dict[str, Any]] = []
        for market, items in sorted(grouped.items()):
            prices = [_number(x.get("price_usd_est")) for x in items]
            ratings = [_number(x.get("rating")) for x in items]
            summary.append(
                {
                    "market": market,
                    "competitor_count": len(items),
                    "avg_price_usd": round(statistics.fmean(prices), 2) if prices else 0.0,
                    "avg_rating": round(statistics.fmean(ratings), 2) if ratings else 0.0,
                }
            )
        return summary

    @staticmethod
    def _summarize_markets(
        profiles: dict[str, dict[str, Any]],
        products: list[dict[str, Any]],
        keywords: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        summary: list[dict[str, Any]] = []
        for market, profile in sorted(profiles.items()):
            market_products = [x for x in products if x.get("market") == market]
            market_keywords = [x for x in keywords if x.get("market") == market]
            prices = [_number(x.get("price_usd")) for x in market_products]
            weights = [_number(x.get("weight_kg")) for x in market_products if _number(x.get("weight_kg")) > 0]
            summary.append(
                {
                    "market": market,
                    "language": profile.get("language", "en"),
                    "currency": profile.get("currency", "USD"),
                    "demand_index": _number(profile.get("demand_index")),
                    "competition_index": _number(profile.get("competition_index")),
                    "growth_pct": _number(profile.get("growth_pct")),
                    "household_energy_price_usd_kwh": _number(
                        profile.get("household_energy_price_usd_kwh")
                    ),
                    "outdoor_participation_pct": _number(profile.get("outdoor_participation_pct")),
                    "compliance_complexity": _number(profile.get("compliance_complexity")),
                    "logistics_cost_index": _number(profile.get("logistics_cost_index")),
                    "vat_pct": _number(profile.get("vat_pct")),
                    "import_duty_pct": _number(profile.get("import_duty_pct")),
                    "avg_order_value_usd": _number(profile.get("avg_order_value_usd")),
                    "product_count": len(market_products),
                    "keyword_count": len(market_keywords),
                    "avg_price_usd": round(statistics.fmean(prices), 2) if prices else 0.0,
                    "avg_weight_kg": round(statistics.fmean(weights), 2) if weights else 0.0,
                    "avg_keyword_opportunity": round(
                        statistics.fmean([_number(x.get("opportunity_index")) for x in market_keywords]), 2
                    )
                    if market_keywords
                    else 0.0,
                }
            )
        return summary

    def _persist(self, payload: dict[str, Any]) -> dict[str, str]:
        json_path = utils.write_json(self.processed_dir / "normalized.json", payload)
        csv_fields = [
            "market",
            "sku",
            "name",
            "category",
            "capacity_wh",
            "output_w",
            "weight_kg",
            "price_usd",
            "price_per_wh",
            "portability_score",
            "price_band",
            "compliance_ready",
            "compliance_gaps",
        ]
        csv_path = utils.write_csv(
            self.processed_dir / "products.csv",
            payload["products"],
            fieldnames=csv_fields,
        )
        return {
            "normalized": str(json_path.relative_to(self.settings.root)),
            "products_csv": str(csv_path.relative_to(self.settings.root)),
        }
````

## `ess_ai/reporting/report_builder.py`

````python
"""报告汇总层：将各阶段结果编排为可读、可交付的 Markdown 报告。"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import utils
from ess_ai.config import Settings

logger = utils.get_logger(__name__)


class ReportBuilder:
    """生成全链路报告与机器可读摘要。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.reports_dir = utils.ensure_dir(settings.path("paths.reports_dir"))

    def build(
        self,
        *,
        run_id: str,
        analysis: dict[str, Any],
        listings: dict[str, Any],
        content: dict[str, Any],
        compliance: dict[str, Any],
        manifest: dict[str, Any],
    ) -> dict[str, Any]:
        summary = self._summary(run_id, analysis, listings, content, compliance)
        markdown = self._markdown(
            run_id=run_id,
            analysis=analysis,
            listings=listings,
            content=content,
            compliance=compliance,
            manifest=manifest,
            summary=summary,
        )
        report_path = utils.write_text(self.reports_dir / "full_chain_report.md", markdown)
        summary_path = utils.write_json(self.reports_dir / "report_summary.json", summary)
        logger.info("报告生成完成: %s", report_path)
        return {
            "report_path": str(report_path.relative_to(self.settings.root)),
            "summary_path": str(summary_path.relative_to(self.settings.root)),
            "summary": summary,
        }

    @staticmethod
    def _summary(
        run_id: str,
        analysis: dict[str, Any],
        listings: dict[str, Any],
        content: dict[str, Any],
        compliance: dict[str, Any],
    ) -> dict[str, Any]:
        top_market = (analysis.get("market_scores") or [{}])[0]
        top_product = (analysis.get("top_opportunities") or [{}])[0]
        compliance_summary = compliance.get("summary", {})
        return {
            "run_id": run_id,
            "generated_at": utils.utc_now_iso(),
            "data_mode": analysis.get("data_mode", "simulated-public-proxy"),
            "top_market": top_market.get("market"),
            "top_market_score": top_market.get("overall_score"),
            "top_sku": top_product.get("sku"),
            "top_product": top_product.get("name"),
            "top_opportunity_score": top_product.get("opportunity_score"),
            "listing_count": len(listings.get("listings", [])),
            "content_pack_count": len(content.get("packs", [])),
            "compliance_passed": compliance_summary.get("passed", 0),
            "compliance_failed": compliance_summary.get("failed", 0),
            "highest_risk": compliance_summary.get("highest_risk", "clear"),
            "summary": analysis.get("summary", []),
        }

    def _markdown(
        self,
        *,
        run_id: str,
        analysis: dict[str, Any],
        listings: dict[str, Any],
        content: dict[str, Any],
        compliance: dict[str, Any],
        manifest: dict[str, Any],
        summary: dict[str, Any],
    ) -> str:
        market_scores = analysis.get("market_scores", [])
        opportunities = analysis.get("top_opportunities", [])
        positioning = analysis.get("positioning", {})
        listing_items = listings.get("listings", [])
        compliance_summary = compliance.get("summary", {})
        issue_counts = compliance_summary.get("issue_counts", {})

        lines = [
            "# 欧美轻量化户外储能 · 全链路运营报告",
            "",
            f"> 运行 ID：`{run_id}` ｜ 生成时间：{utils.utc_now_iso()} ｜ 模式：离线模拟",
            "",
            "## 1. 执行摘要",
            "",
        ]
        lines.extend(f"- {item}" for item in summary.get("summary", []))
        lines.extend(
            [
                "",
                "## 2. 市场排名",
                "",
                self._table(
                    ["排名", "市场", "综合分", "等级", "需求", "竞争", "毛利", "合规", "物流"],
                    [
                        [
                            item.get("rank"),
                            item.get("market"),
                            item.get("overall_score"),
                            item.get("tier"),
                            (item.get("sub_scores") or {}).get("demand"),
                            (item.get("sub_scores") or {}).get("competition"),
                            (item.get("sub_scores") or {}).get("margin"),
                            (item.get("sub_scores") or {}).get("compliance"),
                            (item.get("sub_scores") or {}).get("logistics"),
                        ]
                        for item in market_scores
                    ],
                ),
                "",
                "评分口径：需求 30%、竞争 20%、毛利 25%、合规 10%、物流 15%，可按 `settings.yaml` 调整。",
                "",
                "## 3. 选品机会 Top 5",
                "",
                self._table(
                    ["排名", "市场", "SKU", "商品", "售价 USD", "重量 kg", "机会分", "认证", "建议"],
                    [
                        [
                            item.get("rank"),
                            item.get("market"),
                            item.get("sku"),
                            item.get("name"),
                            item.get("price_usd"),
                            item.get("weight_kg"),
                            item.get("opportunity_score"),
                            "齐备" if item.get("compliance_ready") else "有缺口",
                            item.get("recommended_action"),
                        ]
                        for item in opportunities
                    ],
                ),
                "",
                "## 4. 定位与进入策略",
                "",
                f"- **首发市场：** {positioning.get('entry_market', '-')}",
                f"- **首发单品：** {positioning.get('entry_product', '-')}",
                f"- **定位角度：** {positioning.get('positioning_angle', '-')}",
                f"- **核心人群：** {positioning.get('primary_segment', '-')}",
                f"- **风险提示：** {positioning.get('risk_note', '-')}",
                "",
            ]
        )
        if positioning.get("differentiation"):
            lines.append("差异化抓手：")
            lines.extend(f"- {item}" for item in positioning["differentiation"])
            lines.append("")

        lines.extend(["## 5. Listing 与内容资产", ""])
        if listing_items:
            sample = listing_items[0]
            lines.extend(
                [
                    f"### 示例 Listing：{sample.get('listing_id')}",
                    "",
                    f"**标题：** {sample.get('title')}",
                    "",
                    f"**价格：** ${sample.get('price_usd')} USD（本地价 {sample.get('price_local')} {sample.get('currency')}）",
                    "",
                    "**五点描述：**",
                    "",
                ]
            )
            lines.extend(f"{index}. {bullet}" for index, bullet in enumerate(sample.get("bullets", []), start=1))
            lines.extend(
                [
                    "",
                    f"**搜索词：** {sample.get('search_terms')}",
                    "",
                    f"**合规状态：** {'可进入人工复核' if sample.get('compliance', {}).get('ready') else '存在认证缺口'}",
                    "",
                    f"- Listing 总数：{len(listing_items)}",
                    f"- 内容资产包：{len(content.get('packs', []))}",
                    "",
                ]
            )
        else:
            lines.extend(["暂无 Listing 输出。", ""])

        lines.extend(
            [
                "## 6. 合规初筛",
                "",
                f"- 通过（无高风险）：{compliance_summary.get('passed', 0)}",
                f"- 需处理：{compliance_summary.get('failed', 0)}",
                f"- 最高风险：{compliance_summary.get('highest_risk', 'clear')}",
                f"- 问题计数：高 {issue_counts.get('high', 0)} / 中 {issue_counts.get('medium', 0)} / 低 {issue_counts.get('low', 0)}",
                "",
                "> 规则初筛不构成法律或认证意见；认证范围、标签、电池运输与目的国法规需由持证服务商复核。",
                "",
            ]
        )
        failed_results = [x for x in compliance.get("results", []) if not x.get("passed")]
        if failed_results:
            lines.extend(["### 待处理项（前 5 条）", ""])
            for result in failed_results[:5]:
                issue = result["issues"][0]
                lines.append(
                    f"- `{result.get('listing_id')}`：{issue.get('message')}（{issue.get('code')}）"
                )
            lines.append("")

        lines.extend(
            [
                "## 7. 产出清单",
                "",
                self._table(
                    ["阶段", "状态", "耗时 ms", "产物数"],
                    [
                        [
                            stage.get("name"),
                            stage.get("status"),
                            stage.get("elapsed_ms"),
                            len(stage.get("outputs", [])),
                        ]
                        for stage in manifest.get("stages", [])
                    ],
                ),
                "",
                "## 8. 下一步",
                "",
                "1. 由合规服务商核验目标市场认证范围，优先补齐高风险缺口。",
                "2. 用真实供应商报价替换模拟毛利参数，复核 landed cost。",
                "3. 对 DE/FR 文案做母语审校，再进入小批量投放。",
                "4. 接入真实公开数据时，保留来源、采集时间与快照哈希。",
                "",
                "## 9. 数据边界",
                "",
                "- 不接入任何电商平台店铺 API；",
                "- 所有商品、价格、趋势、竞品数据均为固定种子模拟；",
                "- 不收集个人信息，不复制受版权保护的竞品文案；",
                "- 认证、法规与电池运输结论必须人工复核。",
                "",
                "---",
                "",
                f"*本报告由 {self.settings.project_name} v{self.settings.get('project.version', '0.1.0')} 自动生成。*",
                "",
            ]
        )
        return "\n".join(lines)

    @staticmethod
    def _table(headers: Iterable[str], rows: Iterable[Iterable[Any]]) -> str:
        header_list = [str(item) for item in headers]
        lines = [
            "| " + " | ".join(header_list) + " |",
            "| " + " | ".join("---" for _ in header_list) + " |",
        ]
        for row in rows:
            cells = [str(value).replace("|", "\\|").replace("\n", " ") if value is not None else "-" for value in row]
            lines.append("| " + " | ".join(cells) + " |")
        return "\n".join(lines)
````

## `ess_ai/storage/repository.py`

````python
"""本地存储适配器。

当前实现为文件系统 JSON 存储，后续可在不改业务层的前提下替换为
SQLite / 对象存储 / 数据仓库适配器。
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import utils

logger = utils.get_logger(__name__)


class JsonStore:
    """按名称读写 JSON 快照，默认落在 ``data/processed``。"""

    def __init__(self, root: str | Path) -> None:
        self.root = utils.ensure_dir(root)

    def _path(self, name: str) -> Path:
        safe = utils.safe_filename(name, default="snapshot")
        if not safe.endswith(".json"):
            safe += ".json"
        return self.root / safe

    def save(self, name: str, payload: Any) -> Path:
        path = utils.write_json(self._path(name), payload)
        logger.debug("快照已写入: %s", path)
        return path

    def load(self, name: str, default: Any = None) -> Any:
        return utils.read_json(self._path(name), default)

    def exists(self, name: str) -> bool:
        return self._path(name).exists()

    def list_snapshots(self) -> list[Path]:
        return sorted(self.root.glob("*.json"))


class RunStore:
    """维护每次流水线运行的 manifest，保证阶段结果可追溯。"""

    def __init__(self, root: str | Path) -> None:
        self.root = utils.ensure_dir(root)

    def manifest_path(self, run_id: str) -> Path:
        return self.root / utils.safe_filename(run_id) / "manifest.json"

    def create(self, run_id: str, metadata: Mapping[str, Any]) -> Path:
        manifest = {
            "run_id": run_id,
            "status": "running",
            "created_at": utils.utc_now_iso(),
            "updated_at": utils.utc_now_iso(),
            "metadata": dict(metadata),
            "stages": [],
        }
        return utils.write_json(self.manifest_path(run_id), manifest)

    def _read(self, run_id: str) -> dict[str, Any]:
        manifest = utils.read_json(self.manifest_path(run_id), default={})
        if not isinstance(manifest, dict) or not manifest:
            raise utils.FileIOError(f"运行清单不存在或损坏: {run_id}")
        return manifest

    def load(self, run_id: str) -> dict[str, Any]:
        """读取运行清单。"""

        return self._read(run_id)

    def add_stage(
        self,
        run_id: str,
        *,
        name: str,
        status: str,
        elapsed_ms: float,
        outputs: list[str] | None = None,
        error: str | None = None,
    ) -> Path:
        manifest = self._read(run_id)
        stage: dict[str, Any] = {
            "name": name,
            "status": status,
            "elapsed_ms": round(float(elapsed_ms), 2),
            "outputs": outputs or [],
            "finished_at": utils.utc_now_iso(),
        }
        if error:
            stage["error"] = error
        stages = [
            item
            for item in manifest.setdefault("stages", [])
            if item.get("name") != name
        ]
        stages.append(stage)
        manifest["stages"] = stages
        manifest["updated_at"] = utils.utc_now_iso()
        return utils.write_json(self.manifest_path(run_id), manifest)

    def finalize(self, run_id: str, *, status: str, summary: Mapping[str, Any]) -> Path:
        manifest = self._read(run_id)
        manifest["status"] = status
        manifest["summary"] = dict(summary)
        manifest["updated_at"] = utils.utc_now_iso()
        return utils.write_json(self.manifest_path(run_id), manifest)
````

## `interview_demo.py`

````python
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
````

## `listing_generator.py`

````python
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
````

## `product_research.py`

````python
#!/usr/bin/env python3
"""户外露营轻量化储能 · 公开数据选品自动化模块。

边界声明
--------
1. 仅处理 Amazon / AliExpress / 1688 的公开可见搜索页或本地公开快照；
2. 不登录、不使用卖家后台、不调用任何店铺 API；
3. 不绕过验证码、不伪造 Cookie、不使用代理池对抗访问控制；
4. live 抓取前检查 robots.txt，失败时明确记录并停止，不静默绕过；
5. 演示默认使用 ``data/mock/public_research_snapshot.json``，数据均标注为模拟。

用法
----
    python product_research.py
    python product_research.py --mode offline --min-margin 30 --top-n 20
    python product_research.py --mode live --limit 20
    python product_research.py --help
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urljoin, urlsplit
from urllib.robotparser import RobotFileParser

# ---------------------------------------------------------------------------
# 路径与可选依赖
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import utils  # noqa: E402

logger = utils.get_logger("product_research")

try:  # Excel 是硬依赖，但延迟到导出时给出更清晰的错误
    import openpyxl  # noqa: F401
except ImportError:  # pragma: no cover - 运行环境缺依赖
    openpyxl = None  # type: ignore[assignment]

DEFAULT_CONFIG = PROJECT_ROOT / "config" / "product_research.yaml"
PLATFORM_ALIASES = {
    "amazon": "amazon",
    "amz": "amazon",
    "aliexpress": "aliexpress",
    "ali": "aliexpress",
    "1688": "alibaba_1688",
    "alibaba_1688": "alibaba_1688",
}
SKU_PREFIX = {"amazon": "AMZ", "aliexpress": "ALI", "alibaba_1688": "1688"}
CAPACITY_BUCKETS = ((100, 199), (200, 299), (300, 399), (400, 500))


# ---------------------------------------------------------------------------
# 基础类型与配置
# ---------------------------------------------------------------------------
class ResearchError(RuntimeError):
    """选品模块业务异常。"""


class CrawlError(ResearchError):
    """公开页面抓取失败。"""


class RobotsDenied(CrawlError):
    """robots.txt 不允许抓取。"""


class ParseError(ResearchError):
    """公开页面结构变化，未能解析出商品。"""


@dataclass(frozen=True)
class ResearchConfig:
    root: Path
    path: Path
    data: dict[str, Any]

    def get(self, dotted: str, default: Any = None) -> Any:
        return utils.deep_get(self.data, dotted, default)

    def section(self, name: str) -> dict[str, Any]:
        value = self.get(name, {})
        return dict(value) if isinstance(value, dict) else {}

    def platform_items(self) -> list[tuple[str, dict[str, Any]]]:
        platforms = self.section("platforms")
        return [
            (str(key), dict(value))
            for key, value in platforms.items()
            if isinstance(value, dict) and value.get("enabled", True)
        ]

    def resolve(self, dotted: str) -> Path:
        raw = self.get(dotted)
        if not raw:
            raise ResearchError(f"缺少路径配置: {dotted}")
        path = Path(str(raw)).expanduser()
        return path if path.is_absolute() else (self.root / path).resolve()


def load_research_config(
    config_path: str | Path | None = None,
    *,
    root: str | Path | None = None,
) -> ResearchConfig:
    project_root = Path(root).expanduser().resolve() if root else PROJECT_ROOT
    path = Path(config_path).expanduser() if config_path else project_root / "config" / "product_research.yaml"
    if not path.is_absolute():
        path = (project_root / path).resolve()
    data = utils.read_yaml(path)
    if not isinstance(data, dict):
        raise ResearchError(f"配置文件根节点必须是映射: {path}")
    if not data.get("platforms"):
        raise ResearchError("配置缺少 platforms")
    if not data.get("filters"):
        raise ResearchError("配置缺少 filters")
    return ResearchConfig(root=project_root, path=path, data=data)


def _num(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(value))
    if not match:
        return default
    try:
        return float(match.group(0).replace(",", ""))
    except ValueError:
        return default


def _int(value: Any, default: int = 0) -> int:
    return int(round(_num(value, float(default))))


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _bucket(capacity: float) -> str:
    for low, high in CAPACITY_BUCKETS:
        if low <= capacity <= high:
            return f"{low}-{high}"
    return "out_of_range"


def _title_key(title: str) -> str:
    return re.sub(r"[^\w]+", "", str(title).lower(), flags=re.UNICODE)


def _extract_spec(title: str, field: str) -> float:
    """从公开标题中解析容量/重量/功率，作为字段缺失时的回退。"""

    text = str(title)
    if field == "capacity_wh":
        match = re.search(r"(\d{2,4}(?:\.\d+)?)\s*wh\b", text, flags=re.IGNORECASE)
        if match:
            return _num(match.group(1))
        match = re.search(r"(\d+(?:\.\d+)?)\s*kwh\b", text, flags=re.IGNORECASE)
        return _num(match.group(1)) * 1000 if match else 0.0
    if field == "weight_kg":
        match = re.search(r"(\d+(?:\.\d+)?)\s*kg\b", text, flags=re.IGNORECASE)
        return _num(match.group(1)) if match else 0.0
    if field == "output_w":
        match = re.search(r"(\d{2,4})\s*w\b", text, flags=re.IGNORECASE)
        return _num(match.group(1)) if match else 0.0
    return 0.0


def _parse_rating(text: str) -> float:
    match = re.search(r"([0-5](?:\.\d)?)\s*(?:out of 5|/5|分|星)?", str(text))
    return _num(match.group(1)) if match else 0.0


# ---------------------------------------------------------------------------
# 清洗
# ---------------------------------------------------------------------------
class ProductCleaner:
    """把公开页面/快照记录清洗成统一分析表。"""

    def __init__(self, config: ResearchConfig) -> None:
        self.config = config
        self.filters = config.section("filters")
        self.platforms = {key: value for key, value in config.platform_items()}
        self.fx = config.get("cost_model.fx_to_usd", {}) or {}

    def clean(self, raw_records: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        kept: dict[tuple[str, str], dict[str, Any]] = {}
        drops: Counter[str] = Counter()
        raw_by_platform: Counter[str] = Counter()
        clean_by_platform: Counter[str] = Counter()
        seen_ids: set[tuple[str, str]] = set()
        seen_titles: set[tuple[str, str]] = set()

        for raw in raw_records:
            if not isinstance(raw, dict):
                drops["invalid_record"] += 1
                continue
            platform = PLATFORM_ALIASES.get(str(raw.get("platform", "")).lower(), "")
            if not platform or platform not in self.platforms:
                drops["unknown_platform"] += 1
                continue
            raw_by_platform[platform] += 1
            title = re.sub(r"\s+", " ", str(raw.get("title", ""))).strip()
            if not title:
                drops["missing_title"] += 1
                continue

            lower_title = title.lower()
            excluded = next(
                (word for word in self.filters.get("exclude_keywords", []) if str(word).lower() in lower_title),
                None,
            )
            if excluded:
                drops["excluded_keyword"] += 1
                continue

            price_local = _num(raw.get("price_local", raw.get("price", 0)))
            if price_local <= 0:
                drops["missing_price"] += 1
                continue

            platform_cfg = self.platforms[platform]
            currency = str(raw.get("currency") or platform_cfg.get("currency", "USD")).upper()
            fx = _num(self.fx.get(currency), 1.0)
            price_usd = price_local * fx

            capacity = _num(raw.get("capacity_wh")) or _extract_spec(title, "capacity_wh")
            if capacity <= 0:
                drops["missing_capacity"] += 1
                continue
            output_w = _num(raw.get("output_w")) or _extract_spec(title, "output_w")
            weight = _num(raw.get("weight_kg")) or _extract_spec(title, "weight_kg")
            weight_source = "public_field" if _num(raw.get("weight_kg")) else "title_parse"
            if weight <= 0:
                weight = 5.0
                weight_source = "category_default"

            low_cap, high_cap = [float(x) for x in self.filters.get("capacity_wh", [100, 500])]
            if not low_cap <= capacity <= high_cap:
                drops["capacity_out_of_range"] += 1
                continue
            max_weight = float(self.filters.get("max_weight_kg", 15))
            if weight > max_weight:
                drops["weight_out_of_range"] += 1
                continue
            low_price, high_price = [float(x) for x in self.filters.get("price_usd", [49, 1500])]
            if not low_price <= price_usd <= high_price:
                drops["price_out_of_range"] += 1
                continue
            price_per_wh = price_usd / capacity
            low_ppw, high_ppw = [float(x) for x in self.filters.get("price_per_wh_usd", [0.1, 8])]
            if not low_ppw <= price_per_wh <= high_ppw:
                drops["price_per_wh_outlier"] += 1
                continue
            rating = _num(raw.get("rating"))
            if rating and rating < float(self.filters.get("min_rating", 0)):
                drops["rating_below_threshold"] += 1
                continue

            product_id = str(raw.get("product_id") or raw.get("sku") or raw.get("record_id") or "")
            if not product_id:
                product_id = utils.safe_filename(_title_key(title))[:40]
            identity = (platform, product_id)
            if identity in seen_ids:
                drops["duplicate_product_id"] += 1
                continue

            key = (platform, str(raw.get("product_id") or _title_key(title)))
            title_identity = (platform, _title_key(title))
            if title_identity in seen_titles:
                drops["duplicate_title"] += 1
                continue
            missing = [
                name
                for name, value in (
                    ("url", raw.get("url")),
                    ("monthly_search_volume", raw.get("monthly_search_volume")),
                    ("competitor_count", raw.get("competitor_count")),
                    ("review_count", raw.get("review_count")),
                )
                if not value
            ]
            quality = 100.0 - 8.0 * len(missing)
            if weight_source == "category_default":
                quality -= 12
            if not raw.get("brand"):
                quality -= 3
            quality = _clamp(quality)

            row = {
                "record_id": str(raw.get("record_id") or product_id),
                "platform": platform,
                "platform_label": str(platform_cfg.get("label", platform)),
                "product_id": product_id,
                "sku": f"{SKU_PREFIX.get(platform, platform.upper()[:3])}-{product_id}",
                "title": title,
                "brand": str(raw.get("brand") or "Unknown"),
                "url": str(raw.get("url") or raw.get("source_page") or ""),
                "source_page": str(raw.get("source_page") or raw.get("url") or ""),
                "market": str(raw.get("market") or platform_cfg.get("market", "US")).upper(),
                "currency": currency,
                "price_local": round(price_local, 2),
                "price_usd": round(price_usd, 2),
                "capacity_wh": round(capacity, 1),
                "output_w": round(output_w, 1),
                "weight_kg": round(weight, 2),
                "weight_source": weight_source,
                "battery_type": str(raw.get("battery_type") or "Unknown"),
                "solar_input_w": round(_num(raw.get("solar_input_w")), 1),
                "ports": str(raw.get("ports") or ""),
                "rating": round(rating, 2),
                "review_count": _int(raw.get("review_count")),
                "seller": str(raw.get("seller") or ""),
                "monthly_search_volume": _int(raw.get("monthly_search_volume")),
                "competitor_count": _int(raw.get("competitor_count")),
                "ad_count": _int(raw.get("ad_count")),
                "moq": max(1, _int(raw.get("moq"), 1)),
                "is_sourcing": bool(platform_cfg.get("is_sourcing", False)),
                "fee_rate": _num(platform_cfg.get("fee_rate"), 0.15),
                "benchmark_cost_ratio": _num(platform_cfg.get("benchmark_cost_ratio"), 0.42),
                "conversion_rate": _num(platform_cfg.get("conversion_rate"), 0.02),
                "price_per_wh_usd": round(price_per_wh, 4),
                "price_band": "low" if price_usd < 150 else ("mid" if price_usd <= 400 else "high"),
                "demand_source": "public_search_proxy" if raw.get("monthly_search_volume") else "missing",
                "data_quality_score": round(quality, 2),
                "missing_fields": ",".join(missing),
                "data_source": str(raw.get("data_source") or "offline_public_snapshot"),
                "captured_at": str(raw.get("collected_at") or ""),
            }

            previous = kept.get(key)
            if previous is not None:
                drops["duplicate_title"] += 1
                if row["review_count"] > previous["review_count"]:
                    kept[key] = row
                continue
            seen_ids.add(identity)
            seen_titles.add(title_identity)
            kept[key] = row

        rows = list(kept.values())
        rows.sort(key=lambda item: (item["platform"], -item["review_count"]))
        for row in rows:
            clean_by_platform[row["platform"]] += 1
        stats = {
            "raw_records": sum(raw_by_platform.values()),
            "clean_records": len(rows),
            "dropped_records": sum(drops.values()),
            "dropped_by_reason": dict(drops.most_common()),
            "by_platform_raw": dict(raw_by_platform),
            "by_platform_clean": dict(clean_by_platform),
        }
        return rows, stats


# ---------------------------------------------------------------------------
# 指标计算
# ---------------------------------------------------------------------------
class SelectionMetrics:
    """计算单 SKU 毛利、市场容量、竞争度与综合机会分。

    所有指标都是可解释的规则模型，不依赖平台私有 API。关键公式同时写入
    Excel 的“指标说明”页，便于业务复核。
    """

    def __init__(self, config: ResearchConfig) -> None:
        self.config = config
        self.cost = config.section("cost_model")
        self.competition_cfg = config.section("competition")
        self.capacity_cfg = config.section("market_capacity")
        self.opportunity_cfg = config.section("opportunity")
        self.thresholds = dict(self.opportunity_cfg.get("thresholds", {}) or {})

    def enrich(self, rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
        if not rows:
            raise ResearchError("清洗后没有可用商品，无法计算选品指标")
        retail_rows = [row for row in rows if not row["is_sourcing"]]
        benchmark = self._retail_benchmarks(retail_rows or rows)
        cv_by_bucket, cv_by_platform = self._price_dispersion(retail_rows or rows)
        total_weight = sum(float(v) for v in (self.opportunity_cfg.get("weights") or {}).values()) or 1.0

        enriched: list[dict[str, Any]] = []
        for source in rows:
            row = dict(source)
            bucket = _bucket(row["capacity_wh"])
            is_sourcing = bool(row["is_sourcing"])
            retail_price = benchmark["by_bucket"].get(bucket, benchmark["overall"])
            benchmark_source = "capacity_bucket_median" if bucket in benchmark["by_bucket"] else "overall_median"
            if not is_sourcing:
                retail_price = row["price_usd"]
                benchmark_source = "own_listing_price"
            retail_price = round(float(retail_price), 2)

            supply_cost = row["price_usd"] if is_sourcing else row["price_usd"] * row["benchmark_cost_ratio"]
            supply_cost = round(float(supply_cost), 2)
            weight = float(row["weight_kg"])
            freight = round(
                max(
                    float(self.cost.get("minimum_freight_usd", 6.0)),
                    weight * float(self.cost.get("inbound_freight_per_kg_usd", 2.2)),
                ),
                2,
            )
            duty_rate = float((self.cost.get("duty_pct_by_market") or {}).get(row["market"], 3.0))
            duty = round(supply_cost * duty_rate / 100.0, 2)
            packaging = round(float(self.cost.get("packaging_usd", 1.5)), 2)
            landed = round(supply_cost + freight + duty + packaging, 2)
            fee = round(retail_price * float(row["fee_rate"]), 2)
            fulfillment = round(
                float(self.cost.get("fulfillment_base_usd", 3.0))
                + weight * float(self.cost.get("fulfillment_per_kg_usd", 1.8)),
                2,
            )
            gross_profit = round(retail_price - landed - fee - fulfillment, 2)
            gross_margin = round(gross_profit / retail_price * 100.0, 2) if retail_price else 0.0
            ad_cost = round(retail_price * float(self.cost.get("ad_cost_ratio", 0.08)), 2)
            contribution = round(gross_profit - ad_cost, 2)
            contribution_margin = round(contribution / retail_price * 100.0, 2) if retail_price else 0.0

            search_volume = int(row["monthly_search_volume"])
            conversion = float(row["conversion_rate"])
            monthly_units = round(search_volume * conversion, 0)
            market_capacity = round(monthly_units * retail_price, 2)
            addressable_share = float(self.capacity_cfg.get("addressable_share", 0.15))
            addressable_units = round(monthly_units * addressable_share, 0)
            addressable_revenue = round(addressable_units * retail_price, 2)

            price_cv = cv_by_bucket.get(bucket, 0.0) if is_sourcing else cv_by_platform.get(
                (row["platform"], bucket), cv_by_bucket.get(bucket, 0.0)
            )
            competition = self._competition_score(row, price_cv)
            margin_score = _clamp(gross_margin / 45.0 * 100.0)
            market_score = _clamp(market_capacity / 500_000.0 * 100.0)
            competition_opportunity = _clamp(100.0 - competition)
            lightweight_score = _clamp(100.0 - max(0.0, weight - 2.0) * 7.5)
            data_quality = _clamp(float(row["data_quality_score"]))
            weights = self.opportunity_cfg.get("weights", {}) or {}
            opportunity = (
                margin_score * float(weights.get("margin", 0.35))
                + market_score * float(weights.get("market", 0.25))
                + competition_opportunity * float(weights.get("competition", 0.20))
                + lightweight_score * float(weights.get("lightweight", 0.10))
                + data_quality * float(weights.get("data_quality", 0.10))
            ) / total_weight

            gates: list[str] = []
            if gross_margin < float(self.thresholds.get("min_gross_margin_pct", 25)):
                gates.append(f"毛利率<{self.thresholds.get('min_gross_margin_pct', 25)}%")
            if market_capacity < float(self.thresholds.get("min_market_capacity_usd", 120000)):
                gates.append("市场容量不足")
            if competition > float(self.thresholds.get("max_competition_score", 70)):
                gates.append("竞争度过高")
            if weight > float(self.thresholds.get("max_weight_kg", 12)):
                gates.append("重量超限")
            if opportunity < float(self.thresholds.get("min_opportunity_score", 65)):
                gates.append("综合分不足")

            row.update(
                {
                    "retail_price_usd": retail_price,
                    "retail_benchmark_source": benchmark_source,
                    "supply_cost_usd": supply_cost,
                    "inbound_freight_usd": freight,
                    "duty_usd": duty,
                    "packaging_usd": packaging,
                    "landed_cost_usd": landed,
                    "platform_fee_usd": fee,
                    "fulfillment_cost_usd": fulfillment,
                    "gross_profit_usd": gross_profit,
                    "gross_margin_pct": gross_margin,
                    "ad_cost_est_usd": ad_cost,
                    "contribution_profit_usd": contribution,
                    "contribution_margin_pct": contribution_margin,
                    "monthly_units": int(monthly_units),
                    "market_capacity_usd": market_capacity,
                    "addressable_units": int(addressable_units),
                    "addressable_revenue_usd": addressable_revenue,
                    "price_dispersion_pct": round(price_cv, 2),
                    "competition_score": round(competition, 2),
                    "margin_score": round(margin_score, 2),
                    "market_score": round(market_score, 2),
                    "competition_opportunity_score": round(competition_opportunity, 2),
                    "lightweight_score": round(lightweight_score, 2),
                    "opportunity_score": round(opportunity, 2),
                    "gate_failures": gates,
                    "gate_status": "通过" if not gates else "未通过：" + "；".join(gates),
                    "high_potential": not gates,
                    "recommendation": self._recommendation(opportunity, gates),
                    "suggested_action": self._suggested_action(row, is_sourcing, gates),
                    "compliance_note": self._compliance_note(row["market"]),
                    "cost_basis": (
                        "1688 公开批发价 + 目标市场零售中位价"
                        if is_sourcing
                        else f"{row['platform_label']} 公开零售价 × 成本率 {row['benchmark_cost_ratio']:.0%}"
                    ),
                    "target_channel": (
                        "Amazon US（1688 货源假设）" if is_sourcing else f"{row['platform_label']} {row['market']}"
                    ),
                }
            )
            enriched.append(row)

        enriched.sort(key=lambda item: (-item["opportunity_score"], item["competition_score"]))
        for index, row in enumerate(enriched, start=1):
            row["rank"] = index
        high = [row for row in enriched if row["high_potential"]][: int(self.opportunity_cfg.get("top_n", 30))]
        passing_count = sum(1 for row in enriched if row["high_potential"])
        gate_counts = Counter(reason.split("：")[0] for row in enriched for reason in row["gate_failures"])
        stats = {
            "total": len(enriched),
            "high_potential": len(high),
            "high_potential_total": passing_count,
            "gate_failures": dict(gate_counts),
            "avg_margin_pct": round(statistics.fmean(row["gross_margin_pct"] for row in enriched), 2),
            "avg_competition": round(statistics.fmean(row["competition_score"] for row in enriched), 2),
            "median_market_capacity": round(statistics.median(row["market_capacity_usd"] for row in enriched), 2),
            "benchmark": {key: round(value, 2) for key, value in benchmark["by_bucket"].items()},
        }
        return enriched, high, stats

    def _retail_benchmarks(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        by_bucket: dict[str, list[float]] = defaultdict(list)
        for row in rows:
            by_bucket[_bucket(row["capacity_wh"])].append(float(row["price_usd"]))
        medians = {key: statistics.median(values) for key, values in by_bucket.items() if values}
        all_prices = [float(row["price_usd"]) for row in rows if row["price_usd"] > 0]
        return {
            "by_bucket": medians,
            "overall": statistics.median(all_prices) if all_prices else 0.0,
        }

    @staticmethod
    def _price_dispersion(rows: list[dict[str, Any]]) -> tuple[dict[str, float], dict[tuple[str, str], float]]:
        by_bucket: dict[str, list[float]] = defaultdict(list)
        by_platform: dict[tuple[str, str], list[float]] = defaultdict(list)
        for row in rows:
            price = float(row["price_usd"])
            bucket = _bucket(row["capacity_wh"])
            by_bucket[bucket].append(price)
            by_platform[(row["platform"], bucket)].append(price)

        def cv(values: list[float]) -> float:
            if len(values) < 2:
                return 0.0
            mean = statistics.fmean(values)
            return statistics.pstdev(values) / mean * 100.0 if mean else 0.0

        return (
            {key: cv(values) for key, values in by_bucket.items()},
            {key: cv(values) for key, values in by_platform.items()},
        )

    def _competition_score(self, row: dict[str, Any], price_cv: float) -> float:
        weights = self.competition_cfg.get("weights", {}) or {}
        density = _clamp(
            math.log1p(max(0, int(row["competitor_count"])))
            / math.log1p(float(self.competition_cfg.get("saturation_competitors", 1000)))
            * 100.0
        )
        review = _clamp(
            math.log1p(max(0, int(row["review_count"])))
            / math.log1p(float(self.competition_cfg.get("review_ceiling", 50000)))
            * 100.0
        )
        ad = _clamp(
            int(row["ad_count"]) / max(1.0, float(self.competition_cfg.get("ad_ceiling", 60))) * 100.0
        )
        price = _clamp(price_cv / max(1.0, float(self.competition_cfg.get("price_cv_full_scale_pct", 60))) * 100.0)
        total = sum(float(v) for v in weights.values()) or 1.0
        return (
            density * float(weights.get("listing_density", 0.35))
            + review * float(weights.get("review_barrier", 0.30))
            + ad * float(weights.get("ad_pressure", 0.20))
            + price * float(weights.get("price_dispersion", 0.15))
        ) / total

    @staticmethod
    def _recommendation(score: float, gates: list[str]) -> str:
        if gates:
            return "未达门槛"
        if score >= 80:
            return "S-优先打样"
        if score >= 70:
            return "A-小批量测试"
        return "B-进入观察池"

    @staticmethod
    def _suggested_action(row: dict[str, Any], is_sourcing: bool, gates: list[str]) -> str:
        if gates:
            return "先补齐：" + "；".join(gates)
        if is_sourcing:
            return "联系 1688 供应商索样，核验容量/电芯/BMS/认证，再按目标市场零售价复核"
        return "对标公开零售页，补充供应商报价、头程与退货率后复核毛利"

    @staticmethod
    def _compliance_note(market: str) -> str:
        mapping = {
            "US": "需核验 UL 2743 / FCC / UN38.3 / Prop 65；本表不构成认证结论",
            "DE": "需核验 CE / RoHS / WEEE / UN38.3 / EU Battery Regulation；本表不构成认证结论",
            "FR": "需核验 CE / RoHS / WEEE / UN38.3 / EU Battery Regulation；本表不构成认证结论",
            "UK": "需核验 UKCA / RoHS / WEEE / UN38.3；本表不构成认证结论",
        }
        return mapping.get(market, "需按目标市场核验电池、电气与运输合规；本表不构成认证结论")


# ---------------------------------------------------------------------------
# 公开页面抓取：robots.txt + 限速 + 不绕过访问控制
# ---------------------------------------------------------------------------
class PublicFetcher:
    """只读取公开 HTML，主动遵守 robots.txt 与请求间隔。"""

    def __init__(self, config: ResearchConfig) -> None:
        crawler = config.section("crawler")
        self.user_agent = str(
            crawler.get("user_agent", "OutdoorEssAI/0.2 (public-research; contact: research@example.com)")
        )
        self.timeout = float(crawler.get("timeout_seconds", 20))
        self.delay = max(0.0, float(crawler.get("delay_seconds", 2.0)))
        self.respect_robots = bool(crawler.get("respect_robots", True))
        self._robots: dict[str, bool] = {}
        self._last_request: dict[str, float] = {}
        self._session: Any = None
        self._requests: Any = None

    def _get_session(self) -> Any:
        if self._requests is None:
            try:
                import requests as _requests
            except ImportError as exc:  # pragma: no cover
                raise CrawlError("live 模式需要 requests：pip install requests") from exc
            self._requests = _requests
            self._session = _requests.Session()
            self._session.headers.update(
                {
                    "User-Agent": self.user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
                    "Cache-Control": "no-cache",
                }
            )
        return self._session

    def _robots_allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin in self._robots:
            return self._robots[origin]
        robots_url = f"{origin}/robots.txt"
        try:
            response = self._get_session().get(robots_url, timeout=self.timeout)
        except Exception as exc:
            raise CrawlError(f"读取 robots.txt 失败：{robots_url}：{exc}") from exc
        if response.status_code == 404:
            allowed = True
        elif response.status_code in {401, 403}:
            allowed = False
        elif not 200 <= response.status_code < 300:
            allowed = False
        else:
            parser = RobotFileParser()
            parser.set_url(robots_url)
            parser.parse(response.text.splitlines())
            allowed = parser.can_fetch(self.user_agent, url)
        self._robots[origin] = allowed
        return allowed

    def get(self, url: str) -> str:
        if not self._robots_allowed(url):
            raise RobotsDenied(
                f"robots.txt 不允许抓取 {url}；已停止，未尝试绕过。"
            )
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        last = self._last_request.get(origin, 0.0)
        wait = self.delay - (time.monotonic() - last)
        if wait > 0:
            time.sleep(wait)
        try:
            response = self._get_session().get(url, timeout=self.timeout, allow_redirects=True)
        except Exception as exc:
            raise CrawlError(f"公开页面请求异常：{url}：{exc}") from exc
        self._last_request[origin] = time.monotonic()
        if response.status_code in {401, 403, 429, 503}:
            raise CrawlError(
                f"公开页面拒绝访问（HTTP {response.status_code}）：{url}；"
                "不进行验证码、Cookie 或代理绕过。"
            )
        if response.status_code >= 400:
            raise CrawlError(f"公开页面请求失败（HTTP {response.status_code}）：{url}")
        text = response.text or ""
        lowered = text[:5000].lower()
        if "captcha" in lowered or "robot check" in lowered or "verify you are human" in lowered:
            raise CrawlError(f"公开页面返回验证码/人机校验：{url}；已停止，不做绕过。")
        return text

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None


def _soup(html: str) -> Any:
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:  # pragma: no cover
        raise CrawlError("live 模式需要 beautifulsoup4：pip install beautifulsoup4") from exc
    return BeautifulSoup(html, "html.parser")


def _walk_jsonld(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        types = value.get("@type")
        if types == "Product" or (isinstance(types, list) and "Product" in types):
            yield value
        for child in value.values():
            yield from _walk_jsonld(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_jsonld(child)


def _jsonld_products(html: str, page_url: str) -> list[dict[str, Any]]:
    soup = _soup(html)
    products: list[dict[str, Any]] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            payload = json.loads(script.string or script.get_text() or "")
        except (TypeError, ValueError):
            continue
        for item in _walk_jsonld(payload):
            offers = item.get("offers")
            if isinstance(offers, list):
                offers = offers[0] if offers else {}
            if not isinstance(offers, dict):
                offers = {}
            price = _num(offers.get("price", offers.get("lowPrice", 0)))
            if price <= 0:
                continue
            rating = item.get("aggregateRating") or {}
            url = urljoin(page_url, str(item.get("url") or page_url))
            brand = item.get("brand")
            if isinstance(brand, dict):
                brand = brand.get("name")
            products.append(
                {
                    "title": str(item.get("name") or "").strip(),
                    "brand": str(brand or ""),
                    "url": url,
                    "price_local": price,
                    "currency": str(offers.get("priceCurrency") or "USD").upper(),
                    "rating": _num(rating.get("ratingValue")),
                    "review_count": _int(rating.get("reviewCount") or rating.get("ratingCount")),
                    "seller": str((offers.get("seller") or {}).get("name") or "")
                    if isinstance(offers.get("seller"), dict)
                    else "",
                }
            )
    return [item for item in products if item["title"] and item["price_local"] > 0]


class BasePlatformAdapter:
    key = ""
    label = ""

    def __init__(self, key: str, platform_cfg: dict[str, Any], fetcher: PublicFetcher) -> None:
        self.key = key
        self.cfg = platform_cfg
        self.label = str(platform_cfg.get("label", key))
        self.fetcher = fetcher

    def search_url(self, query: str | None = None) -> str:
        query = query or str(self.cfg.get("query", "portable power station"))
        template = str(self.cfg.get("search_url", ""))
        return template.format(query=quote_plus(query))

    def crawl(self, *, limit: int, query: str | None = None) -> list[dict[str, Any]]:
        page_url = self.search_url(query)
        html = self.fetcher.get(page_url)
        records = self.parse(html, page_url)
        if not records:
            raise ParseError(
                f"{self.label} 公开搜索页未解析出商品，可能页面结构变化或被要求登录。"
            )
        for record in records:
            record.setdefault("platform", self.key)
            record.setdefault("market", self.cfg.get("market", "US"))
            record.setdefault("currency", self.cfg.get("currency", "USD"))
            record.setdefault("source_page", page_url)
            record.setdefault("data_source", "public_live_page")
            record.setdefault("collected_at", utils.utc_now_iso())
            record.setdefault("competitor_count", len(records))
        return records[:limit]

    def parse(self, html: str, page_url: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    def _record_from_jsonld(self, item: dict[str, Any], page_url: str) -> dict[str, Any]:
        return {
            "platform": self.key,
            "product_id": self._product_id(item.get("url", ""), item.get("title", "")),
            "title": item.get("title", ""),
            "brand": item.get("brand", ""),
            "url": item.get("url") or page_url,
            "market": self.cfg.get("market", "US"),
            "currency": item.get("currency") or self.cfg.get("currency", "USD"),
            "price_local": item.get("price_local", 0),
            "rating": item.get("rating", 0),
            "review_count": item.get("review_count", 0),
            "seller": item.get("seller", ""),
            "monthly_search_volume": 0,
            "competitor_count": 0,
            "ad_count": 0,
            "source_page": page_url,
            "data_source": "public_live_page",
            "collected_at": utils.utc_now_iso(),
        }

    @staticmethod
    def _product_id(url: str, title: str) -> str:
        match = re.search(r"(?:/dp/|/item/|offer/)([A-Za-z0-9_-]{5,})", str(url))
        if match:
            return match.group(1)
        return utils.safe_filename(_title_key(title))[:32] or "unknown"


class AmazonAdapter(BasePlatformAdapter):
    def parse(self, html: str, page_url: str) -> list[dict[str, Any]]:
        soup = _soup(html)
        page_text = soup.get_text(" ", strip=True)
        count_match = re.search(r"(?:over|about)\s+([\d,]+)\s+results", page_text, re.IGNORECASE)
        page_count = _int(count_match.group(1)) if count_match else 0
        records: list[dict[str, Any]] = []
        cards = soup.select("div[data-component-type='s-search-result']")
        for card in cards:
            asin = str(card.get("data-asin") or "").strip()
            title_node = card.select_one("h2 a span") or card.select_one("h2 span")
            title = title_node.get_text(" ", strip=True) if title_node else ""
            price_node = card.select_one(".a-price .a-offscreen") or card.select_one(".a-price")
            price = _num(price_node.get_text(" ", strip=True) if price_node else 0)
            if not title or price <= 0:
                continue
            link_node = card.select_one("h2 a[href]") or card.select_one("a.a-link-normal[href]")
            link = urljoin(page_url, str(link_node.get("href"))) if link_node else ""
            rating_node = card.select_one("span.a-icon-alt")
            rating = _parse_rating(rating_node.get_text(" ", strip=True) if rating_node else "")
            reviews_node = (
                card.select_one("a[href*='customerReviews'] span")
                or card.select_one("a[href*='product-reviews'] span")
                or card.select_one("span.a-size-base.s-underline-text")
            )
            records.append(
                {
                    "platform": self.key,
                    "product_id": asin or self._product_id(link, title),
                    "title": title,
                    "brand": title.split()[0] if title else "",
                    "url": link or page_url,
                    "market": self.cfg.get("market", "US"),
                    "currency": self.cfg.get("currency", "USD"),
                    "price_local": price,
                    "rating": rating,
                    "review_count": _int(reviews_node.get_text(" ", strip=True) if reviews_node else 0),
                    "seller": "",
                    "monthly_search_volume": 0,
                    "competitor_count": page_count or len(cards),
                    "ad_count": 1 if card.select_one("[data-component-type='sp-sponsored-result']") else 0,
                    "source_page": page_url,
                    "data_source": "public_live_page",
                    "collected_at": utils.utc_now_iso(),
                }
            )
        if records:
            return records
        return [self._record_from_jsonld(item, page_url) for item in _jsonld_products(html, page_url)]


class AliExpressAdapter(BasePlatformAdapter):
    def parse(self, html: str, page_url: str) -> list[dict[str, Any]]:
        soup = _soup(html)
        page_text = soup.get_text(" ", strip=True)
        count_match = re.search(r"([\d,]+)\s+(?:results|items)", page_text, re.IGNORECASE)
        page_count = _int(count_match.group(1)) if count_match else 0
        records: list[dict[str, Any]] = []
        cards = soup.select(
            "div.search-item-card-wrapper-gallery, a.search-item-card, div.product-card"
        )
        for card in cards:
            link_node = card.select_one("a[href*='/item/']") or card.select_one("a[href]")
            link = urljoin(page_url, str(link_node.get("href"))) if link_node else ""
            title_node = (
                card.select_one("h3")
                or card.select_one("[class*='title']")
                or card.select_one("a[title]")
            )
            title = title_node.get_text(" ", strip=True) if title_node else ""
            price_node = (
                card.select_one("[class*='price']")
                or card.select_one(".seo-optimized-price")
                or card.select_one(".product-price")
            )
            price = _num(price_node.get_text(" ", strip=True) if price_node else 0)
            if not title or price <= 0:
                continue
            rating_node = card.select_one("[class*='star']") or card.select_one("[class*='rating']")
            review_node = card.select_one("[class*='trade']") or card.select_one("[class*='review']")
            records.append(
                {
                    "platform": self.key,
                    "product_id": self._product_id(link, title),
                    "title": title,
                    "brand": "",
                    "url": link or page_url,
                    "market": self.cfg.get("market", "US"),
                    "currency": self.cfg.get("currency", "USD"),
                    "price_local": price,
                    "rating": _parse_rating(rating_node.get_text(" ", strip=True) if rating_node else ""),
                    "review_count": _int(review_node.get_text(" ", strip=True) if review_node else 0),
                    "seller": "",
                    "monthly_search_volume": 0,
                    "competitor_count": page_count or len(cards),
                    "ad_count": 0,
                    "source_page": page_url,
                    "data_source": "public_live_page",
                    "collected_at": utils.utc_now_iso(),
                }
            )
        if records:
            return records
        return [self._record_from_jsonld(item, page_url) for item in _jsonld_products(html, page_url)]


class Alibaba1688Adapter(BasePlatformAdapter):
    def parse(self, html: str, page_url: str) -> list[dict[str, Any]]:
        soup = _soup(html)
        cards = soup.select("div[data-offer-id], div.offer-list-row, div.sm-offer-item")
        records: list[dict[str, Any]] = []
        for card in cards:
            offer_id = str(card.get("data-offer-id") or "").strip()
            link_node = card.select_one("a[href*='detail.1688.com/offer']") or card.select_one("a[href]")
            link = urljoin(page_url, str(link_node.get("href"))) if link_node else ""
            title_node = (
                card.select_one(".title-text")
                or card.select_one("[class*='title']")
                or card.select_one("a[title]")
            )
            title = title_node.get_text(" ", strip=True) if title_node else ""
            if not title and link_node:
                title = str(link_node.get("title") or "")
            price_node = (
                card.select_one(".price")
                or card.select_one(".offer-price")
                or card.select_one("[class*='price']")
            )
            price = _num(price_node.get_text(" ", strip=True) if price_node else 0)
            if not title or price <= 0:
                continue
            seller_node = card.select_one(".company-name") or card.select_one(".shop-name")
            trade_node = card.select_one("[class*='trade']")
            moq_match = re.search(r"(\d+)\s*(?:件|个|台)", card.get_text(" ", strip=True))
            records.append(
                {
                    "platform": self.key,
                    "product_id": offer_id or self._product_id(link, title),
                    "title": title,
                    "brand": "",
                    "url": link or page_url,
                    "market": self.cfg.get("market", "US"),
                    "origin_country": "CN",
                    "currency": self.cfg.get("currency", "CNY"),
                    "price_local": price,
                    "rating": 0,
                    "review_count": _int(trade_node.get_text(" ", strip=True) if trade_node else 0),
                    "seller": seller_node.get_text(" ", strip=True) if seller_node else "",
                    "monthly_search_volume": 0,
                    "competitor_count": len(cards),
                    "ad_count": 0,
                    "moq": _int(moq_match.group(1)) if moq_match else 1,
                    "source_page": page_url,
                    "data_source": "public_live_page",
                    "collected_at": utils.utc_now_iso(),
                }
            )
        if records:
            return records
        return [self._record_from_jsonld(item, page_url) for item in _jsonld_products(html, page_url)]


ADAPTERS: dict[str, type[BasePlatformAdapter]] = {
    "amazon": AmazonAdapter,
    "aliexpress": AliExpressAdapter,
    "alibaba_1688": Alibaba1688Adapter,
}


def collect_live(
    config: ResearchConfig,
    *,
    limit: int,
    query: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    fetcher = PublicFetcher(config)
    records: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    try:
        for key, platform_cfg in config.platform_items():
            adapter_cls = ADAPTERS.get(key)
            if adapter_cls is None:
                failures.append({"platform": key, "error": "未实现公开页面适配器"})
                continue
            try:
                items = adapter_cls(key, platform_cfg, fetcher).crawl(limit=limit, query=query)
                records.extend(items)
                logger.info("live 抓取成功: %s，%d 条", platform_cfg.get("label", key), len(items))
            except (CrawlError, ParseError) as exc:
                logger.warning("live 抓取失败: %s：%s", platform_cfg.get("label", key), exc)
                failures.append({"platform": key, "error": str(exc)})
    finally:
        fetcher.close()
    return records, failures


def load_fixture(config: ResearchConfig) -> list[dict[str, Any]]:
    fixture_path = config.resolve("fixture.path")
    payload = utils.read_json(fixture_path)
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ResearchError(f"公开快照格式错误: {fixture_path}")
    captured_at = str(payload.get("captured_at") or utils.utc_now_iso())
    records: list[dict[str, Any]] = []
    for item in payload["records"]:
        if not isinstance(item, dict):
            continue
        record = dict(item)
        record.setdefault("data_source", "offline_public_snapshot")
        record.setdefault("collected_at", captured_at)
        records.append(record)
    logger.info("已加载离线公开快照: %s，%d 条", fixture_path, len(records))
    return records


def collect_public_data(
    config: ResearchConfig,
    *,
    mode: str,
    limit: int,
    query: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    mode = mode.lower()
    if mode == "offline":
        return load_fixture(config), {"mode": "offline", "live_failures": []}
    if mode == "live":
        records, failures = collect_live(config, limit=limit, query=query)
        if not records:
            raise CrawlError(
                "live 模式未获取到任何公开商品；请检查网络、robots.txt 或页面结构，"
                "不要通过验证码/Cookie/代理绕过访问控制。"
            )
        return records, {"mode": "live", "live_failures": failures}
    if mode == "auto":
        try:
            records, failures = collect_live(config, limit=limit, query=query)
            if records:
                return records, {"mode": "auto_live", "live_failures": failures}
        except CrawlError as exc:
            logger.warning("auto 模式 live 失败，回退快照：%s", exc)
        return load_fixture(config), {"mode": "auto_fixture", "live_failures": []}
    raise ResearchError(f"未知 mode: {mode}")


# ---------------------------------------------------------------------------
# Excel 输出
# ---------------------------------------------------------------------------
# (字段名, 中文表头, 列宽, 数字格式)
CORE_COLUMNS: list[tuple[str, str, int, str]] = [
    ("rank", "排名", 8, "0"),
    ("platform_label", "平台", 11, "@"),
    ("title", "商品标题", 48, "@"),
    ("brand", "品牌/供应商", 16, "@"),
    ("sku", "SKU", 18, "@"),
    ("url", "商品链接", 30, "@"),
    ("market", "目标市场", 10, "@"),
    ("capacity_wh", "容量(Wh)", 10, "#,##0"),
    ("output_w", "输出功率(W)", 11, "#,##0"),
    ("weight_kg", "重量(kg)", 10, "0.00"),
    ("battery_type", "电芯类型", 12, "@"),
    ("solar_input_w", "太阳能输入(W)", 13, "#,##0"),
    ("rating", "评分", 8, "0.0"),
    ("review_count", "评论/成交数", 12, "#,##0"),
    ("seller", "卖家/供应商", 20, "@"),
    ("price_local", "公开售价(原币)", 15, "#,##0.00"),
    ("currency", "币种", 8, "@"),
    ("price_usd", "公开价(USD)", 13, "$#,##0.00"),
    ("retail_price_usd", "零售基准价(USD)", 15, "$#,##0.00"),
    ("supply_cost_usd", "货源/估算成本(USD)", 17, "$#,##0.00"),
    ("landed_cost_usd", "到岸成本(USD)", 14, "$#,##0.00"),
    ("platform_fee_usd", "平台佣金(USD)", 13, "$#,##0.00"),
    ("fulfillment_cost_usd", "履约成本(USD)", 13, "$#,##0.00"),
    ("gross_profit_usd", "单件毛利(USD)", 14, "$#,##0.00"),
    ("gross_margin_pct", "毛利率(%)", 11, "0.0"),
    ("ad_cost_est_usd", "广告估算(USD)", 13, "$#,##0.00"),
    ("contribution_margin_pct", "贡献毛利率(%)", 14, "0.0"),
    ("monthly_search_volume", "月搜索量", 11, "#,##0"),
    ("monthly_units", "预估月销量", 11, "#,##0"),
    ("market_capacity_usd", "市场容量(USD/月)", 16, "$#,##0"),
    ("addressable_revenue_usd", "可获取容量(USD/月)", 17, "$#,##0"),
    ("competitor_count", "竞品数量", 10, "#,##0"),
    ("ad_count", "广告位数", 10, "#,##0"),
    ("competition_score", "竞争度(越低越好)", 15, "0.0"),
    ("margin_score", "毛利得分", 10, "0.0"),
    ("market_score", "市场得分", 10, "0.0"),
    ("competition_opportunity_score", "竞争机会分", 12, "0.0"),
    ("lightweight_score", "轻量得分", 10, "0.0"),
    ("data_quality_score", "数据质量分", 11, "0.0"),
    ("opportunity_score", "综合机会分", 12, "0.0"),
    ("recommendation", "推荐等级", 14, "@"),
    ("gate_status", "门槛状态", 30, "@"),
    ("compliance_note", "合规提示", 46, "@"),
    ("target_channel", "目标渠道", 20, "@"),
    ("cost_basis", "成本口径", 36, "@"),
    ("suggested_action", "建议动作", 42, "@"),
    ("moq", "MOQ", 8, "#,##0"),
    ("price_per_wh_usd", "USD/Wh", 10, "0.000"),
    ("source_page", "公开来源页", 36, "@"),
    ("captured_at", "采集时间", 20, "@"),
    ("record_id", "原始记录ID", 18, "@"),
    ("data_source", "数据来源", 22, "@"),
    ("demand_source", "需求口径", 16, "@"),
    ("weight_source", "重量来源", 12, "@"),
    ("retail_benchmark_source", "零售基准来源", 18, "@"),
    ("price_band", "价格带", 10, "@"),
]
COLUMN_KEYS = [item[0] for item in CORE_COLUMNS]
MONEY_KEYS = {
    "price_usd",
    "retail_price_usd",
    "supply_cost_usd",
    "landed_cost_usd",
    "platform_fee_usd",
    "fulfillment_cost_usd",
    "gross_profit_usd",
    "ad_cost_est_usd",
    "market_capacity_usd",
    "addressable_revenue_usd",
}


class ExcelExporter:
    """生成带格式、筛选、指标说明和数据质量页的 Excel。"""

    def __init__(self, config: ResearchConfig) -> None:
        self.config = config

    def export(
        self,
        *,
        high_rows: list[dict[str, Any]],
        all_rows: list[dict[str, Any]],
        summary: dict[str, Any],
        output_path: Path,
    ) -> Path:
        if openpyxl is None:
            raise ResearchError("生成 Excel 需要 openpyxl：pip install openpyxl")
        from openpyxl import Workbook
        from openpyxl.formatting.rule import ColorScaleRule
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

        wb = Workbook()
        ws = wb.active
        ws.title = "高潜力选品"
        self._write_data_sheet(
            ws,
            high_rows,
            metadata=summary,
            title="户外露营轻量化储能 · 高潜力选品表（100-500Wh）",
            with_meta=True,
        )
        self._apply_highlights(ws, len(high_rows), ColorScaleRule)

        ws_all = wb.create_sheet("全部清洗数据")
        self._write_data_sheet(
            ws_all,
            all_rows,
            metadata=summary,
            title="全部清洗数据",
            with_meta=False,
        )
        self._apply_highlights(ws_all, len(all_rows), ColorScaleRule, header_row=1)

        ws_metric = wb.create_sheet("指标说明")
        self._write_metric_sheet(ws_metric, summary, Alignment, Border, Font, PatternFill, Side)

        ws_params = wb.create_sheet("筛选参数")
        self._write_params_sheet(ws_params, Alignment, Border, Font, PatternFill, Side)

        ws_quality = wb.create_sheet("数据质量")
        self._write_quality_sheet(ws_quality, summary, Alignment, Border, Font, PatternFill, Side)

        wb.properties.title = "户外露营轻量化储能高潜力选品表"
        wb.properties.creator = "Outdoor ESS AI product_research.py"
        wb.properties.description = "公开数据选品分析；不接入平台店铺 API。"
        utils.ensure_dir(output_path.parent)
        wb.save(output_path)
        logger.info("Excel 已生成: %s", output_path)
        return output_path

    def _write_data_sheet(
        self,
        ws: Any,
        rows: list[dict[str, Any]],
        *,
        metadata: dict[str, Any],
        title: str,
        with_meta: bool,
    ) -> None:
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
        from openpyxl.utils import get_column_letter

        header_row = 6 if with_meta else 1
        if with_meta:
            ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=12)
            ws["A1"] = title
            ws["A1"].font = Font(bold=True, size=16, color="1F4E78")
            ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=16)
            ws["A2"] = (
                f"运行：{metadata.get('run_id', '-')}  |  数据模式：{metadata.get('mode', '-')}  |  "
                f"生成：{metadata.get('generated_at', '-')}  |  样本：{metadata.get('cleaned_records', 0)} 条 / "
                f"高潜力：{metadata.get('high_potential_records', 0)} 条"
            )
            ws["A2"].font = Font(size=9, color="595959")
            ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=18)
            ws["A3"] = (
                f"筛选：容量 {metadata.get('filters', {}).get('capacity_wh', '-')} Wh ｜ "
                f"重量≤{metadata.get('filters', {}).get('max_weight_kg', '-')}kg ｜ "
                f"毛利率≥{metadata.get('filters', {}).get('min_gross_margin_pct', '-')}% ｜ "
                f"市场容量≥${metadata.get('filters', {}).get('min_market_capacity_usd', 0):,.0f}/月 ｜ "
                f"竞争度≤{metadata.get('filters', {}).get('max_competition_score', '-')}"
            )
            ws["A3"].font = Font(size=9, color="595959")
            ws.merge_cells(start_row=4, start_column=1, end_row=4, end_column=20)
            ws["A4"] = (
                "口径：毛利=零售价-到岸成本-平台佣金-履约成本；市场容量=月搜索量×转化率×零售价；"
                "竞争度越高越激烈。公开数据/模拟数据不构成认证或投资建议。"
            )
            ws["A4"].font = Font(size=9, color="7F6000")
            ws["A4"].fill = PatternFill("solid", fgColor="FFF2CC")
            for row in range(1, 5):
                ws.row_dimensions[row].height = 24 if row == 1 else 20

        header_fill = PatternFill("solid", fgColor="1F4E78")
        header_font = Font(color="FFFFFF", bold=True, size=10)
        border = Border(
            left=Side(style="thin", color="D9E2F3"),
            right=Side(style="thin", color="D9E2F3"),
            top=Side(style="thin", color="D9E2F3"),
            bottom=Side(style="thin", color="D9E2F3"),
        )
        for col_index, (_key, header, width, _fmt) in enumerate(CORE_COLUMNS, start=1):
            cell = ws.cell(row=header_row, column=col_index, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border
            ws.column_dimensions[get_column_letter(col_index)].width = width
        ws.row_dimensions[header_row].height = 38

        if not rows:
            ws.merge_cells(
                start_row=header_row + 1,
                start_column=1,
                end_row=header_row + 1,
                end_column=8,
            )
            ws.cell(row=header_row + 1, column=1, value="当前参数下无符合全部门槛的 SKU，请放宽阈值后重跑。")
            ws.cell(row=header_row + 1, column=1).font = Font(color="C00000", italic=True)
            return

        for row_index, row in enumerate(rows, start=header_row + 1):
            for col_index, (key, _header, _width, fmt) in enumerate(CORE_COLUMNS, start=1):
                value = row.get(key)
                if isinstance(value, (list, dict)):
                    value = json.dumps(value, ensure_ascii=False)
                cell = ws.cell(row=row_index, column=col_index, value=value)
                cell.border = border
                cell.alignment = Alignment(
                    vertical="top",
                    wrap_text=key in {"title", "compliance_note", "suggested_action", "gate_status", "cost_basis"},
                )
                if key in MONEY_KEYS or key == "price_local":
                    cell.number_format = "$#,##0.00" if key in MONEY_KEYS else "#,##0.00"
                elif fmt:
                    cell.number_format = fmt
                if key in {"url", "source_page"} and value:
                    cell.hyperlink = str(value)
                    cell.font = Font(color="0563C1", underline="single")
            ws.row_dimensions[row_index].height = 34

        last_col = get_column_letter(len(CORE_COLUMNS))
        ws.auto_filter.ref = f"A{header_row}:{last_col}{header_row + len(rows)}"
        ws.freeze_panes = f"A{header_row + 1}"
        ws.sheet_view.showGridLines = False
        ws.page_setup.orientation = "landscape"
        ws.page_setup.fitToWidth = 1
        ws.sheet_properties.pageSetUpPr.fitToPage = True

    @staticmethod
    def _apply_highlights(ws: Any, row_count: int, color_scale_cls: Any, *, header_row: int = 6) -> None:
        if row_count <= 0:
            return
        from openpyxl.formatting.rule import ColorScaleRule
        from openpyxl.utils import get_column_letter

        positions = {key: index for index, (key, *_rest) in enumerate(CORE_COLUMNS, start=1)}
        last_row = header_row + row_count
        for key, reverse in (("opportunity_score", False), ("gross_margin_pct", False), ("competition_score", True)):
            col = get_column_letter(positions[key])
            if reverse:
                rule = ColorScaleRule(
                    start_type="num",
                    start_value=0,
                    start_color="63BE7B",
                    mid_type="num",
                    mid_value=50,
                    mid_color="FFEB84",
                    end_type="num",
                    end_value=100,
                    end_color="F8696B",
                )
            else:
                rule = ColorScaleRule(
                    start_type="num",
                    start_value=0,
                    start_color="F8696B",
                    mid_type="num",
                    mid_value=50,
                    mid_color="FFEB84",
                    end_type="num",
                    end_value=100,
                    end_color="63BE7B",
                )
            ws.conditional_formatting.add(f"{col}{header_row + 1}:{col}{last_row}", rule)

    def _write_metric_sheet(self, ws: Any, summary: dict[str, Any], *_: Any) -> None:
        from openpyxl.styles import Alignment, Font, PatternFill

        ws.title = "指标说明"
        ws.append(["指标", "字段", "计算公式", "业务解释", "当前门槛"])
        fill = PatternFill("solid", fgColor="1F4E78")
        for cell in ws[1]:
            cell.fill = fill
            cell.font = Font(color="FFFFFF", bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")
        metrics = [
            ("单件毛利", "gross_profit_usd", "零售基准价 - 到岸成本 - 平台佣金 - 履约成本", "单件商品的可变成本后利润，不含广告与固定费用。", "-"),
            ("毛利率", "gross_margin_pct", "单件毛利 ÷ 零售基准价 × 100%", "越高越好；低于门槛不进入高潜表。", f"≥{summary.get('filters', {}).get('min_gross_margin_pct', 25)}%"),
            ("到岸成本", "landed_cost_usd", "货源/估算成本 + 头程 + 关税 + 包装", "零售平台成本按公开价×成本率估算；1688 按公开批发价。", "-"),
            ("市场容量", "market_capacity_usd", "月搜索量 × 平台转化率 × 零售基准价", "目标市场月度可寻址销售额，不代表本 SKU 实际销量。", f"≥${summary.get('filters', {}).get('min_market_capacity_usd', 120000):,.0f}"),
            ("可获取容量", "addressable_revenue_usd", "市场容量 × 可获取份额", "按配置的 addressable_share 估算，默认 15%。", "-"),
            ("竞争度", "competition_score", "0.35×列表密度 + 0.30×评论壁垒 + 0.20×广告压力 + 0.15×价格离散", "0-100，越高越激烈；因此反向进入综合分。", f"≤{summary.get('filters', {}).get('max_competition_score', 70)}"),
            ("综合机会分", "opportunity_score", "0.35×毛利得分 + 0.25×市场得分 + 0.20×竞争机会 + 0.10×轻量得分 + 0.10×数据质量", "0-100，用于排序；仅作决策辅助。", f"≥{summary.get('filters', {}).get('min_opportunity_score', 65)}"),
            ("轻量化得分", "lightweight_score", "100 - max(0, 重量-2kg)×7.5", "越轻越高，最高 100。", "-"),
            ("数据质量分", "data_quality_score", "100 - 缺失字段惩罚 - 估算重量惩罚", "公开页面字段缺失会降低可信度。", "-"),
        ]
        for item in metrics:
            ws.append(list(item))
        widths = [16, 24, 52, 60, 22]
        for index, width in enumerate(widths, start=1):
            ws.column_dimensions[chr(64 + index)].width = width
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
            for cell in row:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
        ws.freeze_panes = "A2"

    def _write_params_sheet(self, ws: Any, *_: Any) -> None:
        from openpyxl.styles import Alignment, Font, PatternFill

        ws.title = "筛选参数"
        ws.append(["参数", "当前值", "说明"])
        for cell in ws[1]:
            cell.fill = PatternFill("solid", fgColor="1F4E78")
            cell.font = Font(color="FFFFFF", bold=True)
        for key, value in _flatten(self.config.data).items():
            rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
            ws.append([key, rendered, "修改 config/product_research.yaml 或使用 CLI 参数覆盖"])
        ws.column_dimensions["A"].width = 46
        ws.column_dimensions["B"].width = 50
        ws.column_dimensions["C"].width = 46
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
            for cell in row:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
        ws.freeze_panes = "A2"

    def _write_quality_sheet(self, ws: Any, summary: dict[str, Any], *_: Any) -> None:
        from openpyxl.styles import Font, PatternFill

        ws.title = "数据质量"
        ws.append(["类别", "指标", "数值"])
        for cell in ws[1]:
            cell.fill = PatternFill("solid", fgColor="1F4E78")
            cell.font = Font(color="FFFFFF", bold=True)
        quality = summary.get("quality", {})
        rows = [
            ("总量", "原始记录", quality.get("raw_records", 0)),
            ("总量", "清洗后记录", quality.get("clean_records", 0)),
            ("总量", "高潜力记录", summary.get("high_potential_records", 0)),
            ("总量", "平均毛利率(%)", quality.get("avg_margin_pct", 0)),
            ("总量", "平均竞争度", quality.get("avg_competition", 0)),
            ("总量", "市场中位容量(USD/月)", quality.get("median_market_capacity", 0)),
        ]
        for key, value in (quality.get("by_platform_raw") or {}).items():
            rows.append(("平台原始", key, value))
        for key, value in (quality.get("by_platform_clean") or {}).items():
            rows.append(("平台清洗后", key, value))
        for key, value in (quality.get("dropped_by_reason") or {}).items():
            rows.append(("剔除原因", key, value))
        for key, value in (quality.get("benchmark") or {}).items():
            rows.append(("零售基准价", f"{key} Wh", value))
        for failure in summary.get("live_failures", []):
            rows.append(("live 失败", failure.get("platform", ""), failure.get("error", "")))
        for item in rows:
            ws.append(list(item))
        ws.column_dimensions["A"].width = 18
        ws.column_dimensions["B"].width = 38
        ws.column_dimensions["C"].width = 80
        ws.freeze_panes = "A2"


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    result: dict[str, Any] = {}
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            result.update(_flatten(child, path))
    else:
        result[prefix] = value
    return result


def _display_path(root: Path, path: Path) -> str:
    """优先返回相对项目根目录的路径；外部输出目录返回绝对路径。"""

    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


# ---------------------------------------------------------------------------
# 引擎与 CLI
# ---------------------------------------------------------------------------
def apply_overrides(
    config: ResearchConfig,
    *,
    mode: str | None = None,
    output_dir: str | None = None,
    fixture: str | None = None,
    top_n: int | None = None,
    min_wh: float | None = None,
    max_wh: float | None = None,
    max_weight: float | None = None,
    min_margin: float | None = None,
    min_market_capacity: float | None = None,
    max_competition: float | None = None,
    min_score: float | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> ResearchConfig:
    data = copy.deepcopy(config.data)
    if mode:
        data.setdefault("crawler", {})["mode"] = mode
    if fixture:
        data.setdefault("fixture", {})["path"] = fixture
    if output_dir:
        data.setdefault("output", {})["dir"] = output_dir
    filters = data.setdefault("filters", {})
    if min_wh is not None or max_wh is not None:
        current = list(filters.get("capacity_wh", [100, 500]))
        filters["capacity_wh"] = [
            float(min_wh if min_wh is not None else current[0]),
            float(max_wh if max_wh is not None else current[1]),
        ]
    if max_weight is not None:
        filters["max_weight_kg"] = float(max_weight)
    if min_price is not None or max_price is not None:
        current = list(filters.get("price_usd", [49, 1500]))
        filters["price_usd"] = [
            float(min_price if min_price is not None else current[0]),
            float(max_price if max_price is not None else current[1]),
        ]
    thresholds = data.setdefault("opportunity", {}).setdefault("thresholds", {})
    if min_margin is not None:
        thresholds["min_gross_margin_pct"] = float(min_margin)
    if min_market_capacity is not None:
        thresholds["min_market_capacity_usd"] = float(min_market_capacity)
    if max_competition is not None:
        thresholds["max_competition_score"] = float(max_competition)
    if min_score is not None:
        thresholds["min_opportunity_score"] = float(min_score)
    if top_n is not None:
        data.setdefault("opportunity", {})["top_n"] = int(top_n)
    return ResearchConfig(root=config.root, path=config.path, data=data)


class ProductResearchEngine:
    """采集 → 清洗 → 指标 → Excel/CSV/JSON 的独立编排器。"""

    def __init__(self, config: ResearchConfig) -> None:
        self.config = config
        self.output_dir = config.resolve("output.dir")
        self.cleaner = ProductCleaner(config)
        self.metrics = SelectionMetrics(config)
        self.exporter = ExcelExporter(config)

    def run(
        self,
        *,
        mode: str | None = None,
        limit: int | None = None,
        query: str | None = None,
    ) -> dict[str, Any]:
        utils.ensure_dir(self.output_dir)
        selected_mode = str(mode or self.config.get("crawler.mode", "offline")).lower()
        limit = int(limit or self.config.get("crawler.max_results_per_platform", 30))
        run_id = f"research_{utils.timestamp()}"
        generated_at = utils.utc_now_iso()

        raw_records, meta = collect_public_data(
            self.config, mode=selected_mode, limit=limit, query=query
        )
        clean_rows, quality = self.cleaner.clean(raw_records)
        all_rows, high_rows, metric_stats = self.metrics.enrich(clean_rows)

        thresholds = dict(self.config.get("opportunity.thresholds", {}) or {})
        filters = {
            "capacity_wh": [float(x) for x in self.config.get("filters.capacity_wh", [100, 500])],
            "max_weight_kg": float(self.config.get("filters.max_weight_kg", 15)),
            "price_usd": [float(x) for x in self.config.get("filters.price_usd", [49, 1500])],
            "min_gross_margin_pct": float(thresholds.get("min_gross_margin_pct", 25)),
            "min_market_capacity_usd": float(thresholds.get("min_market_capacity_usd", 120000)),
            "max_competition_score": float(thresholds.get("max_competition_score", 70)),
            "max_weight_threshold_kg": float(thresholds.get("max_weight_kg", 12)),
            "min_opportunity_score": float(thresholds.get("min_opportunity_score", 65)),
            "top_n": int(self.config.get("opportunity.top_n", 30)),
        }

        raw_path = utils.write_json(
            self.output_dir / str(self.config.get("output.raw_name", "raw_public_snapshot.json")),
            {
                "run_id": run_id,
                "generated_at": generated_at,
                "mode": meta.get("mode", selected_mode),
                "source_policy": "public-visible-only; no login; no private API; no captcha bypass",
                "live_failures": meta.get("live_failures", []),
                "records": raw_records,
            },
        )
        csv_path = utils.write_csv(
            self.output_dir / str(self.config.get("output.csv_name", "cleaned_products.csv")),
            all_rows,
            fieldnames=COLUMN_KEYS,
        )
        excel_path = self.output_dir / str(
            self.config.get("output.excel_name", "high_potential_products.xlsx")
        )

        summary: dict[str, Any] = {
            "run_id": run_id,
            "generated_at": generated_at,
            "mode": meta.get("mode", selected_mode),
            "data_policy": "public-visible-only; no login; no private API; no captcha bypass",
            "notice": "公开数据/模拟数据选品结果，不构成认证、法律或投资建议。",
            "raw_records": quality.get("raw_records", len(raw_records)),
            "cleaned_records": len(all_rows),
            "high_potential_records": len(high_rows),
            "filters": filters,
            "quality": {**quality, **metric_stats},
            "live_failures": meta.get("live_failures", []),
            "top5": [
                {
                    "rank": row["rank"],
                    "platform": row["platform_label"],
                    "title": row["title"],
                    "capacity_wh": row["capacity_wh"],
                    "gross_margin_pct": row["gross_margin_pct"],
                    "market_capacity_usd": row["market_capacity_usd"],
                    "competition_score": row["competition_score"],
                    "opportunity_score": row["opportunity_score"],
                }
                for row in (high_rows or all_rows)[:5]
            ],
            "outputs": {
                "excel": _display_path(self.config.root, excel_path),
                "csv": _display_path(self.config.root, csv_path),
                "raw": _display_path(self.config.root, raw_path),
            },
        }
        self.exporter.export(
            high_rows=high_rows,
            all_rows=all_rows,
            summary=summary,
            output_path=excel_path,
        )
        summary_path = self.output_dir / str(
            self.config.get("output.summary_name", "research_summary.json")
        )
        summary["outputs"]["summary"] = _display_path(self.config.root, summary_path)
        utils.write_json(summary_path, summary)
        logger.info(
            "选品完成: 原始 %d / 清洗 %d / 高潜力 %d",
            summary["raw_records"],
            summary["cleaned_records"],
            summary["high_potential_records"],
        )
        return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="product_research",
        description="公开数据选品：100-500Wh 户外露营轻量化储能",
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="选品配置文件")
    parser.add_argument("--mode", choices=["offline", "live", "auto"], help="数据模式")
    parser.add_argument("--fixture", help="离线公开快照 JSON 路径")
    parser.add_argument("--output-dir", help="输出目录，默认 outputs/research")
    parser.add_argument("--limit", type=int, help="每个平台最多抓取条数（live）")
    parser.add_argument("--query", help="live 搜索关键词，默认使用平台配置")
    parser.add_argument("--top-n", type=int, help="高潜表最多输出条数")
    parser.add_argument("--min-wh", type=float, help="最小容量 Wh")
    parser.add_argument("--max-wh", type=float, help="最大容量 Wh")
    parser.add_argument("--max-weight", type=float, help="最大重量 kg")
    parser.add_argument("--min-price", type=float, help="最低公开价 USD")
    parser.add_argument("--max-price", type=float, help="最高公开价 USD")
    parser.add_argument("--min-margin", type=float, help="最低毛利率 %%")
    parser.add_argument("--min-market-capacity", type=float, help="最低市场容量 USD/月")
    parser.add_argument("--max-competition", type=float, help="最高竞争度 0-100")
    parser.add_argument("--min-score", type=float, help="最低综合机会分")
    parser.add_argument("--log-level", default="INFO", help="日志级别")
    parser.add_argument("--strict", action="store_true", help="无高潜力 SKU 时返回非零退出码")
    return parser


def _configure_stdio() -> None:
    """Windows GBK 控制台下强制 UTF-8，避免中文和符号输出失败。"""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def main(argv: Iterable[str] | None = None) -> int:
    _configure_stdio()
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        config = load_research_config(args.config)
        config = apply_overrides(
            config,
            mode=args.mode,
            output_dir=args.output_dir,
            fixture=args.fixture,
            top_n=args.top_n,
            min_wh=args.min_wh,
            max_wh=args.max_wh,
            max_weight=args.max_weight,
            min_margin=args.min_margin,
            min_market_capacity=args.min_market_capacity,
            max_competition=args.max_competition,
            min_score=args.min_score,
            min_price=args.min_price,
            max_price=args.max_price,
        )
    except (ResearchError, utils.UtilError) as exc:
        print(f"✗ 配置加载失败：{exc}", file=sys.stderr)
        return 1
    output_dir = config.resolve("output.dir")
    utils.ensure_dir(output_dir)
    utils.setup_logging(
        level=args.log_level,
        log_file=output_dir / "product_research.log",
        console=True,
        force=True,
    )
    try:
        summary = ProductResearchEngine(config).run(
            mode=args.mode,
            limit=args.limit,
            query=args.query,
        )
    except (ResearchError, CrawlError, utils.UtilError) as exc:
        logger.error("选品失败: %s", exc)
        print(f"✗ 选品失败：{exc}", file=sys.stderr)
        return 1

    print("")
    print("=" * 72)
    print(f"✓ 选品完成：{summary['run_id']}")
    print(f"  模式      : {summary['mode']}")
    print(f"  原始/清洗 : {summary['raw_records']} / {summary['cleaned_records']}")
    print(f"  高潜力 SKU: {summary['high_potential_records']}")
    print(
        f"  平均毛利  : {summary['quality'].get('avg_margin_pct', 0):.1f}%  |  "
        f"平均竞争度: {summary['quality'].get('avg_competition', 0):.1f}"
    )
    print(f"  Excel     : {summary['outputs']['excel']}")
    print(f"  CSV       : {summary['outputs']['csv']}")
    print(f"  JSON      : {summary['outputs']['summary']}")
    print("=" * 72)
    if summary["high_potential_records"] == 0 and args.strict:
        return 2
    return 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "product_research"))
````

## `prompts/compliance_review.md`

````markdown
# 合规复核提示词（人工复核辅助）

你是户外储能产品的合规初筛助手。请基于输入的市场、产品参数、认证清单和文案，
输出**风险提示**，而不是法律结论。

## 检查清单

1. 目标市场要求的认证是否齐全，证书范围是否覆盖具体型号。
2. 文案是否出现未经验证的认证、绝对化功效、虚假销量/评价、医疗或安全保证。
3. 是否包含续航/输出因设备而异的限制说明。
4. 是否包含锂电池运输法规提示。
5. 目标市场语言、单位、插头标准、能效标签是否需要本地化。
6. 是否缺少责任主体、保修条款、包装清单或警告语。

## 输出结构

```json
{
  "risk_level": "high|medium|low|clear",
  "issues": [
    {
      "code": "string",
      "severity": "high|medium|low",
      "field": "string",
      "message": "string",
      "suggestion": "string"
    }
  ],
  "human_review_required": true,
  "disclaimer": "string"
}
```

禁止把“建议补充”写成“已经合规”。所有结论都必须标注需要持证服务商复核。
````

## `prompts/listing_system.md`

````markdown
# Listing 生成系统提示词（DeepSeek V4.1-Flash）

你是欧美户外储能品类的资深跨境电商 Listing 运营。你的任务是把**结构化商品数据**
改写为清晰、可核验、可审阅的英文 Listing 草稿。

## 硬性约束

1. 只使用输入中给出的参数，不得编造容量、功率、重量、循环次数、认证、销量、评价。
2. 不得使用绝对化承诺：best、No.1、100% safe、unlimited、zero risk、guaranteed forever。
3. 认证状态必须与输入字段一致；缺失认证时写“under review”，不得写成“certified”。
4. 不得复制竞品文案；不得提及具体竞品品牌。
5. 必须包含输入中的 required_disclosures。
6. 电池产品必须提示运输法规限制；续航必须注明“因设备和条件而异”。
7. 输出严格 JSON，不要 Markdown 代码围栏。

## 输出结构

```json
{
  "title": "string, <= 200 chars",
  "bullets": ["string", "string", "string", "string", "string"],
  "description": "string, <= 2000 chars",
  "search_terms": "string, <= 250 bytes",
  "compliance_notes": ["string"],
  "claims_used": ["string"]
}
```

## 写作要求

- 标题：品牌/型号 + 容量 + 功率 + 场景，不堆砌关键词。
- 五点：参数、便携性、太阳能、场景、质保/电芯，每点一个卖点。
- 描述：先讲使用场景，再列参数，最后放披露与限制。
- 搜索词：只放真实相关词，不包含品牌词、竞品词、误导词。
````

## `report_generator.py`

````python
#!/usr/bin/env python3
"""经营报表自动化：广告日报、库存预警、月度利润。

所有经营数据为固定种子模拟，不接入真实店铺、广告或库存后台。
"""

from __future__ import annotations

import argparse
import math
import random
import re
import sys
from collections.abc import Iterable
from datetime import date, timedelta
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import utils  # noqa: E402

logger = utils.get_logger("report_generator")
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "report_generator.yaml"
DEFAULT_INPUT = PROJECT_ROOT / "outputs" / "research" / "high_potential_products.xlsx"
DEFAULT_OUTPUT = PROJECT_ROOT / "outputs" / "operations"


class ReportError(RuntimeError):
    """报表生成异常。"""


# ---------------------------------------------------------------------------
# 配置与选品表
# ---------------------------------------------------------------------------
class ReportConfig:
    def __init__(self, root: Path, path: Path, data: dict[str, Any]) -> None:
        self.root = root
        self.path = path
        self.data = data

    def get(self, dotted: str, default: Any = None) -> Any:
        return utils.deep_get(self.data, dotted, default)

    def resolve(self, dotted: str) -> Path:
        raw = self.get(dotted)
        if not raw:
            raise ReportError(f"缺少路径配置: {dotted}")
        path = Path(str(raw)).expanduser()
        return path if path.is_absolute() else (self.root / path).resolve()


def load_config(path: str | Path | None = None, *, root: str | Path | None = None) -> ReportConfig:
    project_root = Path(root).expanduser().resolve() if root else PROJECT_ROOT
    config_path = Path(path).expanduser() if path else project_root / "config" / "report_generator.yaml"
    if not config_path.is_absolute():
        config_path = (project_root / config_path).resolve()
    data = utils.read_yaml(config_path)
    if not isinstance(data, dict):
        raise ReportError(f"配置格式错误: {config_path}")
    if not data.get("input") or not data.get("output"):
        raise ReportError("配置缺少 input/output")
    return ReportConfig(project_root, config_path, data)


def _num(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(value or ""))
    return float(match.group(0).replace(",", "")) if match else default


def load_products(path: str | Path, sheet: str = "高潜力选品") -> list[dict[str, Any]]:
    source = Path(path).expanduser().resolve()
    if not source.exists():
        raise ReportError(f"选品表不存在: {source}")
    try:
        from openpyxl import load_workbook
    except ImportError as exc:  # pragma: no cover
        raise ReportError("读取选品表需要 openpyxl") from exc
    wb = load_workbook(source, read_only=True, data_only=True)
    ws = wb[sheet] if sheet in wb.sheetnames else wb[wb.sheetnames[0]]
    headers: list[str] = []
    header_row = 1
    for row_index, row in enumerate(ws.iter_rows(min_row=1, max_row=25, values_only=True), start=1):
        values = [str(cell or "").strip() for cell in row]
        if "SKU" in values or "sku" in values:
            headers = values
            header_row = row_index
            break
    products: list[dict[str, Any]] = []
    for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
        record = dict(zip(headers, row, strict=False))
        sku = str(record.get("SKU") or record.get("sku") or "").strip()
        if not sku:
            continue
        price = _num(record.get("零售基准价(USD)") or record.get("retail_price_usd") or record.get("公开价(USD)"))
        landed = _num(record.get("到岸成本(USD)") or record.get("landed_cost_usd"))
        gross = _num(record.get("毛利率(%)") or record.get("gross_margin_pct"))
        if price <= 0 or landed <= 0:
            logger.warning("跳过价格/成本缺失 SKU: %s", sku)
            continue
        if gross <= 0:
            gross = (price - landed) / price * 100.0
        products.append(
            {
                "sku": sku,
                "name": str(record.get("商品标题") or record.get("title") or sku),
                "platform": str(record.get("平台") or record.get("platform_label") or ""),
                "market": str(record.get("目标市场") or record.get("market") or "US"),
                "price": round(price, 2),
                "landed_cost": round(landed, 2),
                "gross_margin_pct": gross,
                "weight_kg": max(0.1, _num(record.get("重量(kg)") or record.get("weight_kg"), 1.0)),
                "capacity_wh": _num(record.get("容量(Wh)") or record.get("capacity_wh")),
                "market_capacity_usd": _num(record.get("市场容量(USD/月)") or record.get("market_capacity_usd")),
                "opportunity_score": _num(record.get("综合机会分") or record.get("opportunity_score")),
                "moq": int(_num(record.get("MOQ") or record.get("moq"), 1)),
            }
        )
    wb.close()
    if not products:
        raise ReportError("选品表中没有可用 SKU")
    return products


# ---------------------------------------------------------------------------
# 经营模拟
# ---------------------------------------------------------------------------
def _weekday_cn(value: date) -> str:
    return ("周一", "周二", "周三", "周四", "周五", "周六", "周日")[value.weekday()]


class OperationsSimulator:
    def __init__(self, config: ReportConfig, products: list[dict[str, Any]]) -> None:
        self.config = config
        self.products = products
        self.sim = config.data.get("simulation", {}) or {}
        self.cost = config.data.get("cost", {}) or {}
        self.seed = int(self.sim.get("seed", 20261021))
        self.days = max(1, int(self.sim.get("days", 30)))
        self.end = date.fromisoformat(str(self.sim.get("period_end") or "2026-09-30"))
        self.start = self.end - timedelta(days=self.days - 1)
        self.rng = random.Random(self.seed)

    def run(self) -> dict[str, Any]:
        ad_rows: list[dict[str, Any]] = []
        metrics: list[dict[str, Any]] = []
        for product in self.products:
            daily = self._daily_rows(product)
            ad_rows.extend(daily)
            metrics.append(self._aggregate(product, daily))
        ad_rows.sort(key=lambda row: (row["date"], row["sku"]))
        metrics.sort(key=lambda row: row["roi"], reverse=True)
        return {
            "ad_rows": ad_rows,
            "metrics": metrics,
            "summary": self._summary(metrics, ad_rows),
            "period": f"{self.start.isoformat()} ~ {self.end.isoformat()}",
            "days": self.days,
            "seed": self.seed,
        }

    def _daily_rows(self, product: dict[str, Any]) -> list[dict[str, Any]]:
        price = float(product["price"])
        gross_margin = max(0.05, min(0.75, float(product["gross_margin_pct"]) / 100.0))
        monthly_potential = float(product["market_capacity_usd"]) / price if price else 0
        target_share = float(self.sim.get("target_share", 0.08))
        base_daily = max(1.0, monthly_potential * target_share / self.days)
        ad_low, ad_high = [float(x) for x in self.sim.get("ad_order_share", [0.35, 0.65])]
        acos_low, acos_high = [float(x) for x in self.sim.get("target_acos_range", [0.12, 0.22])]
        ctr_low, ctr_high = [float(x) for x in self.sim.get("ctr_range", [0.004, 0.012])]
        cvr_low, cvr_high = [float(x) for x in self.sim.get("cvr_range", [0.04, 0.10])]
        rows: list[dict[str, Any]] = []
        for offset in range(self.days):
            day = self.start + timedelta(days=offset)
            daily_total = max(1, int(round(base_daily * self.rng.uniform(0.6, 1.4))))
            ad_orders = max(1, min(daily_total, int(round(daily_total * self.rng.uniform(ad_low, ad_high)))))
            organic_orders = max(0, daily_total - ad_orders)
            ad_sales = round(ad_orders * price, 2)
            target_acos = self.rng.uniform(acos_low, acos_high)
            spend = round(ad_sales * target_acos, 2)
            ctr = self.rng.uniform(ctr_low, ctr_high)
            cvr = self.rng.uniform(cvr_low, cvr_high)
            clicks = max(5, int(round(ad_orders / cvr)))
            cpc = spend / clicks if clicks else 0.0
            impressions = max(clicks, int(round(clicks / ctr)))
            ctr_actual = clicks / impressions if impressions else 0.0
            cvr_actual = ad_orders / clicks if clicks else 0.0
            acos = spend / ad_sales if ad_sales else 0.0
            roas = ad_sales / spend if spend else 0.0
            ad_profit = round(ad_sales * gross_margin - spend, 2)
            rows.append(
                {
                    "date": day.isoformat(),
                    "weekday": _weekday_cn(day),
                    "platform": product["platform"],
                    "sku": product["sku"],
                    "name": product["name"],
                    "market": product["market"],
                    "price": price,
                    "impressions": impressions,
                    "clicks": clicks,
                    "ctr": round(ctr_actual, 6),
                    "cpc": round(cpc, 2),
                    "spend": spend,
                    "ad_orders": ad_orders,
                    "cvr": round(cvr_actual, 6),
                    "ad_sales": ad_sales,
                    "acos": round(acos, 6),
                    "roas": round(roas, 4),
                    "ad_profit": ad_profit,
                    "gross_margin_pct": round(gross_margin * 100, 2),
                    "total_orders": daily_total,
                    "organic_orders": organic_orders,
                }
            )
        return rows

    def _aggregate(self, product: dict[str, Any], daily: list[dict[str, Any]]) -> dict[str, Any]:
        price = float(product["price"])
        landed = float(product["landed_cost"])
        weight = float(product["weight_kg"])
        units = sum(int(row["total_orders"]) for row in daily)
        ad_orders = sum(int(row["ad_orders"]) for row in daily)
        ad_sales = round(sum(float(row["ad_sales"]) for row in daily), 2)
        ad_spend = round(sum(float(row["spend"]) for row in daily), 2)
        revenue = round(units * price, 2)
        cogs = round(units * landed, 2)
        fee_rate = float(self.cost.get("platform_fee_rate", 0.15))
        platform_fee = round(revenue * fee_rate, 2)
        fulfillment = round(
            units
            * (
                float(self.cost.get("fulfillment_base_usd", 3.0))
                + weight * float(self.cost.get("fulfillment_per_kg_usd", 1.8))
            ),
            2,
        )
        refunds = round(revenue * float(self.cost.get("return_rate", 0.03)), 2)
        other = round(revenue * float(self.cost.get("other_rate", 0.01)), 2)
        avg_daily = round(units / self.days, 2) if self.days else 0.0
        begin_low, begin_high = [float(x) for x in self.sim.get("inventory_begin_cover_range", [30, 90])]
        onhand_low, onhand_high = [float(x) for x in self.sim.get("inventory_onhand_cover_range", [5, 95])]
        transit_low, transit_high = [float(x) for x in self.sim.get("inventory_intransit_cover_range", [0, 30])]
        begin_inventory = max(1, int(math.ceil(avg_daily * self.rng.uniform(begin_low, begin_high))))
        on_hand = max(0, int(math.ceil(avg_daily * self.rng.uniform(onhand_low, onhand_high))))
        in_transit = max(0, int(math.ceil(avg_daily * self.rng.uniform(transit_low, transit_high))))
        avg_inventory_units = round((begin_inventory + on_hand) / 2.0, 2)
        stock_value = round(on_hand * landed, 2)
        inventory_value = round(avg_inventory_units * landed, 2)
        storage = round(inventory_value * float(self.cost.get("storage_rate_month", 0.01)), 2)
        total_cost = round(cogs + platform_fee + fulfillment + ad_spend + refunds + storage + other, 2)
        gross_profit = round(revenue - cogs, 2)
        net_profit = round(revenue - total_cost, 2)
        roi = net_profit / total_cost if total_cost else 0.0
        net_margin = net_profit / revenue if revenue else 0.0
        gross_margin = gross_profit / revenue if revenue else 0.0
        turnover_days = avg_inventory_units / avg_daily if avg_daily else 0.0
        turnover_times = 365.0 / turnover_days if turnover_days else 0.0
        days_cover = (on_hand + in_transit) / avg_daily if avg_daily else 0.0
        lead_time = int(self.rng.choice(self.sim.get("lead_time_choices", [25, 30, 35, 40])))
        safety_days = int(self.sim.get("safety_days", 14))
        reorder_point = round(avg_daily * (lead_time + safety_days), 1)
        target_cover = int(self.sim.get("target_cover_days", 30))
        target_units = avg_daily * (lead_time + safety_days + target_cover)
        suggested_order = max(0, int(math.ceil(target_units - (on_hand + in_transit))))
        if days_cover < lead_time:
            status = "紧急补货"
            priority = "P1"
        elif days_cover < lead_time + safety_days:
            status = "关注"
            priority = "P2"
        elif days_cover > 90:
            status = "滞销"
            priority = "P3"
        else:
            status = "健康"
            priority = "P4"
        aging_units = (
            max(0, int(math.ceil(on_hand * self.rng.uniform(*self.sim.get("aging_ratio_range", [0, 0.3])))))
            if days_cover > 90
            else 0
        )
        return {
            **product,
            "units": units,
            "ad_orders": ad_orders,
            "ad_sales": ad_sales,
            "ad_spend": ad_spend,
            "revenue": revenue,
            "cogs": cogs,
            "gross_profit": gross_profit,
            "gross_margin": gross_margin,
            "platform_fee": platform_fee,
            "fulfillment": fulfillment,
            "refunds": refunds,
            "storage": storage,
            "other": other,
            "net_profit": net_profit,
            "net_margin": net_margin,
            "roi": roi,
            "total_cost": total_cost,
            "ad_acos": ad_spend / ad_sales if ad_sales else 0.0,
            "ad_roas": ad_sales / ad_spend if ad_spend else 0.0,
            "avg_daily_units": round(avg_daily, 2),
            "begin_inventory": begin_inventory,
            "on_hand": on_hand,
            "in_transit": in_transit,
            "avg_inventory_units": avg_inventory_units,
            "stock_value": stock_value,
            "inventory_value": inventory_value,
            "inventory_turnover_days": round(turnover_days, 1),
            "inventory_turnover_times": round(turnover_times, 2),
            "days_cover": round(days_cover, 1),
            "lead_time_days": lead_time,
            "safety_days": safety_days,
            "reorder_point": reorder_point,
            "suggested_order_qty": suggested_order,
            "aging_units": aging_units,
            "stock_status": status,
            "priority": priority,
        }

    def _summary(self, metrics: list[dict[str, Any]], ad_rows: list[dict[str, Any]]) -> dict[str, Any]:
        total_revenue = sum(item["revenue"] for item in metrics)
        total_cost = sum(item["total_cost"] for item in metrics)
        total_net = sum(item["net_profit"] for item in metrics)
        total_ad_spend = sum(item["ad_spend"] for item in metrics)
        total_ad_sales = sum(item["ad_sales"] for item in metrics)
        total_units = sum(item["units"] for item in metrics)
        inventory_alerts = [item for item in metrics if item["stock_status"] != "健康"]
        return {
            "ad_rows": len(ad_rows),
            "sku_count": len(metrics),
            "units": total_units,
            "revenue": round(total_revenue, 2),
            "cogs": round(sum(item["cogs"] for item in metrics), 2),
            "ad_spend": round(total_ad_spend, 2),
            "ad_sales": round(total_ad_sales, 2),
            "net_profit": round(total_net, 2),
            "net_margin": round(total_net / total_revenue * 100, 2) if total_revenue else 0.0,
            "roi": round(total_net / total_cost * 100, 2) if total_cost else 0.0,
            "ad_acos": round(total_ad_spend / total_ad_sales * 100, 2) if total_ad_sales else 0.0,
            "ad_roas": round(total_ad_sales / total_ad_spend, 2) if total_ad_spend else 0.0,
            "inventory_alerts": len(inventory_alerts),
            "urgent_alerts": sum(1 for item in metrics if item["stock_status"] == "紧急补货"),
            "slow_moving": sum(1 for item in metrics if item["stock_status"] == "滞销"),
            "top_roi": max(metrics, key=lambda item: item["roi"])["sku"] if metrics else "",
            "lowest_cover": min(metrics, key=lambda item: item["days_cover"])["sku"] if metrics else "",
        }


# ---------------------------------------------------------------------------
# Excel 输出
# ---------------------------------------------------------------------------
def _require_openpyxl() -> Any:
    try:
        import openpyxl
    except ImportError as exc:  # pragma: no cover
        raise ReportError("生成 Excel 需要 openpyxl") from exc
    return openpyxl


def _styles() -> dict[str, Any]:
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    return {
        "header_fill": PatternFill("solid", fgColor="1F4E78"),
        "header_font": Font(color="FFFFFF", bold=True, size=10),
        "border": Border(
            left=Side(style="thin", color="D9E2F3"),
            right=Side(style="thin", color="D9E2F3"),
            top=Side(style="thin", color="D9E2F3"),
            bottom=Side(style="thin", color="D9E2F3"),
        ),
        "alignment": Alignment(vertical="top", wrap_text=True),
    }


def _meta(ws: Any, title: str, subtitle: str, note: str, columns: int) -> None:
    from openpyxl.styles import Font, PatternFill

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=columns)
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=16, color="1F4E78")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=columns)
    ws["A2"] = subtitle
    ws["A2"].font = Font(size=9, color="595959")
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=columns)
    ws["A3"] = note
    ws["A3"].font = Font(size=9, color="7F6000")
    ws["A3"].fill = PatternFill("solid", fgColor="FFF2CC")
    ws.row_dimensions[1].height = 26


def _table(
    ws: Any,
    columns: list[tuple[str, str, int, str]],
    rows: list[dict[str, Any]],
    *,
    header_row: int = 6,
    status_key: str | None = None,
) -> None:
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    style = _styles()
    for index, (_key, header, width, _fmt) in enumerate(columns, start=1):
        cell = ws.cell(row=header_row, column=index, value=header)
        cell.fill = style["header_fill"]
        cell.font = style["header_font"]
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = style["border"]
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.row_dimensions[header_row].height = 34
    status_colors = {
        "紧急补货": "F4CCCC",
        "关注": "FFF2CC",
        "滞销": "D9D9D9",
        "健康": "D9EAD3",
    }
    for row_index, row in enumerate(rows, start=header_row + 1):
        for col_index, (key, _header, _width, fmt) in enumerate(columns, start=1):
            value = row.get(key)
            cell = ws.cell(row=row_index, column=col_index, value=value)
            cell.border = style["border"]
            cell.alignment = Alignment(vertical="top", wrap_text=key in {"name", "status", "action"})
            if fmt:
                cell.number_format = fmt
        if status_key:
            cell = ws.cell(row=row_index, column=next(i for i, c in enumerate(columns, start=1) if c[0] == status_key))
            fill = status_colors.get(str(row.get(status_key)))
            if fill:
                cell.fill = PatternFill("solid", fgColor=fill)
                cell.font = Font(bold=True)
    ws.freeze_panes = f"A{header_row + 1}"
    ws.sheet_view.showGridLines = False
    ws.auto_filter.ref = (
        f"A{header_row}:{get_column_letter(len(columns))}{header_row + len(rows)}"
    )


def _write_metric_sheet(ws: Any) -> None:
    from openpyxl.styles import Alignment, Font, PatternFill

    ws.append(["指标", "字段", "公式", "说明"])
    for cell in ws[1]:
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.font = Font(color="FFFFFF", bold=True)
    rows = [
        ("广告 CTR", "ctr", "点击 ÷ 展示", "广告点击率"),
        ("广告 CVR", "cvr", "广告订单 ÷ 点击", "广告转化率"),
        ("CPC", "cpc", "广告花费 ÷ 点击", "单次点击成本"),
        ("ACOS", "acos", "广告花费 ÷ 广告销售额", "广告成本占广告销售比"),
        ("ROAS", "roas", "广告销售额 ÷ 广告花费", "广告投入产出比"),
        ("广告贡献毛利", "ad_profit", "广告销售额 × 毛利率 - 广告花费", "广告口径的可变利润"),
        ("毛利率", "gross_margin", "毛利 ÷ 收入", "商品口径毛利，未扣平台佣金/履约/广告"),
        ("库存周转天数", "inventory_turnover_days", "平均库存件数 ÷ 日均销量", "30 天口径；越低周转越快"),
        ("库存周转次数", "inventory_turnover_times", "365 ÷ 库存周转天数", "年化周转次数"),
        ("库存覆盖天数", "days_cover", "(在库 + 在途) ÷ 日均销量", "含在途库存"),
        ("再订货点", "reorder_point", "日均销量 × (交期 + 安全天数)", "触发补货的库存水平"),
        ("建议补货量", "suggested_order_qty", "目标库存 - (在库 + 在途)", "目标覆盖 = 交期 + 安全 + 30 天"),
        ("ROI", "roi", "净利润 ÷ 总成本", "总成本=COGS+佣金+履约+广告+退款+仓储+其他"),
        ("净利率", "net_margin", "净利润 ÷ 收入", "含广告/退款/仓储等经营费用"),
    ]
    for row in rows:
        ws.append(row)
    widths = [16, 26, 48, 44]
    for index, width in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + index)].width = width
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    ws.freeze_panes = "A2"


def _save_with_properties(wb: Any, path: Path, title: str) -> None:
    wb.properties.title = title
    wb.properties.creator = "Outdoor ESS AI report_generator.py"
    wb.properties.description = "固定种子模拟经营数据；不接入真实后台。"
    utils.ensure_dir(path.parent)
    wb.save(path)
    logger.info("Excel 已生成: %s", path)


def write_ad_workbook(path: Path, ad_rows: list[dict[str, Any]], summary: dict[str, Any], run_id: str, period: str) -> None:
    _require_openpyxl()
    from openpyxl import Workbook
    from openpyxl.formatting.rule import ColorScaleRule

    wb = Workbook()
    ws = wb.active
    ws.title = "广告日报"
    columns = [
        ("date", "日期", 11, "yyyy-mm-dd"),
        ("weekday", "星期", 8, "@"),
        ("platform", "平台", 11, "@"),
        ("sku", "SKU", 20, "@"),
        ("name", "商品", 34, "@"),
        ("market", "市场", 8, "@"),
        ("impressions", "展示", 11, "#,##0"),
        ("clicks", "点击", 9, "#,##0"),
        ("ctr", "CTR", 8, "0.00%"),
        ("cpc", "CPC", 8, "$0.00"),
        ("spend", "广告花费", 12, "$#,##0.00"),
        ("ad_orders", "广告订单", 10, "#,##0"),
        ("cvr", "CVR", 8, "0.00%"),
        ("ad_sales", "广告销售额", 13, "$#,##0.00"),
        ("acos", "ACOS", 9, "0.00%"),
        ("roas", "ROAS", 8, "0.00"),
        ("ad_profit", "广告贡献毛利", 13, "$#,##0.00"),
        ("gross_margin_pct", "参考毛利率", 9, "0.0"),
    ]
    _meta(
        ws,
        "广告投放日报",
        f"运行：{run_id} ｜ 周期：{period} ｜ 记录：{len(ad_rows)} 条",
        "模拟数据：展示/点击/花费/订单均由固定种子生成；不接入广告后台。",
        len(columns),
    )
    _table(ws, columns, ad_rows)
    # 合计行
    total_row = 6 + len(ad_rows) + 1
    total = {
        "date": "合计",
        "platform": "",
        "sku": "",
        "name": "",
        "market": "",
        "impressions": sum(int(row["impressions"]) for row in ad_rows),
        "clicks": sum(int(row["clicks"]) for row in ad_rows),
        "spend": round(sum(float(row["spend"]) for row in ad_rows), 2),
        "ad_orders": sum(int(row["ad_orders"]) for row in ad_rows),
        "ad_sales": round(sum(float(row["ad_sales"]) for row in ad_rows), 2),
        "ad_profit": round(sum(float(row["ad_profit"]) for row in ad_rows), 2),
    }
    total["ctr"] = total["clicks"] / total["impressions"] if total["impressions"] else 0
    total["cvr"] = total["ad_orders"] / total["clicks"] if total["clicks"] else 0
    total["cpc"] = total["spend"] / total["clicks"] if total["clicks"] else 0
    total["acos"] = total["spend"] / total["ad_sales"] if total["ad_sales"] else 0
    total["roas"] = total["ad_sales"] / total["spend"] if total["spend"] else 0
    from openpyxl.styles import Font, PatternFill
    for index, (key, _header, _width, fmt) in enumerate(columns, start=1):
        cell = ws.cell(row=total_row, column=index, value=total.get(key, ""))
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="D9E2F3")
        if fmt:
            cell.number_format = fmt
    ws.auto_filter.ref = f"A6:R{6 + len(ad_rows)}"
    ws.conditional_formatting.add(
        f"O7:O{6 + len(ad_rows)}",
        ColorScaleRule(
            start_type="num", start_value=0, start_color="63BE7B",
            mid_type="num", mid_value=0.2, mid_color="FFEB84",
            end_type="num", end_value=0.5, end_color="F8696B",
        ),
    )
    metric_ws = wb.create_sheet("指标说明")
    _write_metric_sheet(metric_ws)
    _save_with_properties(wb, path, "广告投放日报")


def write_inventory_workbook(path: Path, metrics: list[dict[str, Any]], run_id: str, period: str) -> None:
    _require_openpyxl()
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "库存预警"
    rows = sorted(metrics, key=lambda item: item["days_cover"])
    columns = [
        ("sku", "SKU", 20, "@"),
        ("name", "商品", 32, "@"),
        ("platform", "平台", 11, "@"),
        ("market", "市场", 8, "@"),
        ("units", "30天销量", 10, "#,##0"),
        ("avg_daily_units", "日均销量", 10, "0.00"),
        ("begin_inventory", "期初库存", 10, "#,##0"),
        ("on_hand", "在库", 9, "#,##0"),
        ("in_transit", "在途", 9, "#,##0"),
        ("days_cover", "覆盖天数", 10, "0.0"),
        ("lead_time_days", "交期(天)", 9, "0"),
        ("safety_days", "安全天数", 9, "0"),
        ("reorder_point", "再订货点", 11, "0.0"),
        ("suggested_order_qty", "建议补货", 11, "#,##0"),
        ("stock_value", "库存金额", 13, "$#,##0.00"),
        ("aging_units", "库龄>90天", 11, "#,##0"),
        ("inventory_turnover_days", "周转天数", 10, "0.0"),
        ("inventory_turnover_times", "年化周转", 10, "0.00"),
        ("stock_status", "状态", 10, "@"),
        ("priority", "优先级", 9, "@"),
    ]
    _meta(
        ws,
        "库存预警表",
        f"运行：{run_id} ｜ 周期：{period} ｜ SKU：{len(metrics)}",
        "覆盖天数=(在库+在途)÷日均销量；周转天数=平均库存÷日均销量；模拟数据。",
        len(columns),
    )
    _table(ws, columns, rows, status_key="stock_status")
    ws.auto_filter.ref = f"A6:T{6 + len(rows)}"
    metric_ws = wb.create_sheet("指标说明")
    _write_metric_sheet(metric_ws)
    _save_with_properties(wb, path, "库存预警表")


def write_profit_workbook(path: Path, metrics: list[dict[str, Any]], summary: dict[str, Any], run_id: str, period: str) -> None:
    _require_openpyxl()
    from openpyxl import Workbook
    from openpyxl.formatting.rule import ColorScaleRule
    from openpyxl.styles import Alignment, Font, PatternFill

    wb = Workbook()
    dashboard = wb.active
    dashboard.title = "经营概览"
    _meta(
        dashboard,
        "月度经营概览",
        f"运行：{run_id} ｜ 周期：{period} ｜ SKU：{summary['sku_count']}",
        "模拟数据：收入/成本/广告/库存均由固定种子生成；不接入真实后台。",
        8,
    )
    dashboard["A5"] = "核心指标"
    dashboard["A5"].font = Font(bold=True, size=12, color="1F4E78")
    overview = [
        ("总销量", summary["units"], "#,##0"),
        ("总收入", summary["revenue"], "$#,##0.00"),
        ("总广告花费", summary["ad_spend"], "$#,##0.00"),
        ("总净利润", summary["net_profit"], "$#,##0.00"),
        ("净利率", summary["net_margin"] / 100, "0.00%"),
        ("整体 ROI", summary["roi"] / 100, "0.00%"),
        ("广告 ACOS", summary["ad_acos"] / 100, "0.00%"),
        ("广告 ROAS", summary["ad_roas"], "0.00"),
        ("库存预警 SKU", summary["inventory_alerts"], "#,##0"),
        ("紧急补货 SKU", summary["urgent_alerts"], "#,##0"),
    ]
    for index, (label, value, fmt) in enumerate(overview, start=6):
        dashboard.cell(row=index, column=1, value=label).font = Font(bold=True)
        cell = dashboard.cell(row=index, column=2, value=value)
        cell.number_format = fmt
        cell.alignment = Alignment(horizontal="right")
    dashboard["D5"] = "Top / 风险 SKU"
    dashboard["D5"].font = Font(bold=True, size=12, color="1F4E78")
    top_roi = next((item for item in metrics if item["sku"] == summary["top_roi"]), None)
    low_cover = next((item for item in metrics if item["sku"] == summary["lowest_cover"]), None)
    dashboard["D6"] = "最高 ROI"
    dashboard["E6"] = f"{top_roi['sku'] if top_roi else '-'} / {top_roi['roi'] * 100:.1f}%" if top_roi else "-"
    dashboard["D7"] = "最低覆盖"
    dashboard["E7"] = f"{low_cover['sku'] if low_cover else '-'} / {low_cover['days_cover']:.1f} 天" if low_cover else "-"
    dashboard["D8"] = "建议动作"
    dashboard["E8"] = "优先处理 P1 补货，复核滞销库存与广告 ACOS"
    dashboard.column_dimensions["A"].width = 22
    dashboard.column_dimensions["B"].width = 18
    dashboard.column_dimensions["D"].width = 22
    dashboard.column_dimensions["E"].width = 46

    ws = wb.create_sheet("月度利润")
    columns = [
        ("sku", "SKU", 20, "@"),
        ("name", "商品", 32, "@"),
        ("platform", "平台", 11, "@"),
        ("market", "市场", 8, "@"),
        ("units", "销量", 9, "#,##0"),
        ("revenue", "收入", 13, "$#,##0.00"),
        ("cogs", "COGS", 13, "$#,##0.00"),
        ("gross_profit", "毛利", 13, "$#,##0.00"),
        ("gross_margin", "毛利率(商品)", 11, "0.00%"),
        ("platform_fee", "平台佣金", 12, "$#,##0.00"),
        ("fulfillment", "履约", 11, "$#,##0.00"),
        ("ad_spend", "广告费", 11, "$#,##0.00"),
        ("refunds", "退款", 11, "$#,##0.00"),
        ("storage", "仓储", 10, "$#,##0.00"),
        ("other", "其他", 10, "$#,##0.00"),
        ("total_cost", "总成本", 13, "$#,##0.00"),
        ("net_profit", "净利润", 13, "$#,##0.00"),
        ("net_margin", "净利率", 10, "0.00%"),
        ("roi", "ROI", 9, "0.00%"),
        ("ad_acos", "广告 ACOS", 11, "0.00%"),
        ("ad_roas", "广告 ROAS", 10, "0.00"),
        ("avg_inventory_units", "平均库存", 11, "#,##0.00"),
        ("inventory_turnover_days", "库存周转天数", 12, "0.0"),
        ("inventory_turnover_times", "年化周转", 10, "0.00"),
        ("stock_value", "库存金额", 12, "$#,##0.00"),
    ]
    _meta(
        ws,
        "月度利润核算表",
        f"运行：{run_id} ｜ 周期：{period} ｜ 金额单位：USD",
        "ROI=净利润÷总成本；总成本=COGS+佣金+履约+广告+退款+仓储+其他；库存周转天数=平均库存÷日均销量。",
        len(columns),
    )
    _table(ws, columns, metrics)
    total_row = 6 + len(metrics) + 1
    totals = {
        "sku": "合计",
        "name": "",
        "platform": "",
        "market": "",
        "units": summary["units"],
        "revenue": summary["revenue"],
        "cogs": summary["cogs"],
        "gross_profit": round(summary["revenue"] - summary["cogs"], 2),
        "platform_fee": round(sum(item["platform_fee"] for item in metrics), 2),
        "fulfillment": round(sum(item["fulfillment"] for item in metrics), 2),
        "ad_spend": summary["ad_spend"],
        "refunds": round(sum(item["refunds"] for item in metrics), 2),
        "storage": round(sum(item["storage"] for item in metrics), 2),
        "other": round(sum(item["other"] for item in metrics), 2),
        "total_cost": round(sum(item["total_cost"] for item in metrics), 2),
        "net_profit": summary["net_profit"],
        "avg_inventory_units": round(sum(item["avg_inventory_units"] for item in metrics), 2),
        "stock_value": round(sum(item["stock_value"] for item in metrics), 2),
    }
    totals["gross_margin"] = totals["gross_profit"] / totals["revenue"] if totals["revenue"] else 0
    totals["net_margin"] = totals["net_profit"] / totals["revenue"] if totals["revenue"] else 0
    totals["roi"] = totals["net_profit"] / sum(item["total_cost"] for item in metrics) if metrics else 0
    totals["ad_acos"] = summary["ad_acos"] / 100
    totals["ad_roas"] = summary["ad_roas"]
    avg_daily_total = sum(item["avg_daily_units"] for item in metrics)
    totals["inventory_turnover_days"] = (
        round(sum(item["avg_inventory_units"] for item in metrics) / avg_daily_total, 1)
        if avg_daily_total
        else 0
    )
    totals["inventory_turnover_times"] = (
        round(365 / totals["inventory_turnover_days"], 2) if totals["inventory_turnover_days"] else 0
    )
    for index, (key, _header, _width, fmt) in enumerate(columns, start=1):
        cell = ws.cell(row=total_row, column=index, value=totals.get(key, ""))
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="D9E2F3")
        if fmt:
            cell.number_format = fmt
    ws.auto_filter.ref = f"A6:Y{6 + len(metrics)}"
    ws.conditional_formatting.add(
        f"S7:S{6 + len(metrics)}",
        ColorScaleRule(
            start_type="num", start_value=-0.2, start_color="F8696B",
            mid_type="num", mid_value=0.2, mid_color="FFEB84",
            end_type="num", end_value=0.6, end_color="63BE7B",
        ),
    )
    metric_ws = wb.create_sheet("指标说明")
    _write_metric_sheet(metric_ws)
    _save_with_properties(wb, path, "月度利润核算表")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _display(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="report_generator",
        description="模拟经营数据：广告日报、库存预警、月度利润报表",
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="报表配置")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="选品表")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT), help="输出目录")
    parser.add_argument("--seed", type=int, help="覆盖模拟种子")
    parser.add_argument("--period-end", help="报表截止日 YYYY-MM-DD")
    parser.add_argument("--days", type=int, help="报表周期天数")
    parser.add_argument("--log-level", default="INFO")
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
        config = load_config(args.config)
        if args.seed is not None:
            config.data.setdefault("simulation", {})["seed"] = args.seed
        if args.period_end:
            config.data.setdefault("simulation", {})["period_end"] = args.period_end
        if args.days is not None:
            config.data.setdefault("simulation", {})["days"] = args.days
        products = load_products(args.input, str(config.get("input.sheet", "高潜力选品")))
        output_dir = Path(args.output_dir).expanduser().resolve()
        utils.ensure_dir(output_dir)
        utils.setup_logging(
            level=args.log_level,
            log_file=output_dir / "report_generator.log",
            console=True,
            force=True,
        )
        simulator = OperationsSimulator(config, products)
        data = simulator.run()
        run_id = f"ops_{utils.utc_now().strftime('%Y%m%d_%H%M%S_%f')}"
        ad_path = output_dir / str(config.get("output.ad_file", "ad_daily_report.xlsx"))
        inventory_path = output_dir / str(config.get("output.inventory_file", "inventory_alert.xlsx"))
        profit_path = output_dir / str(config.get("output.profit_file", "monthly_profit.xlsx"))
        write_ad_workbook(ad_path, data["ad_rows"], data["summary"], run_id, data["period"])
        write_inventory_workbook(inventory_path, data["metrics"], run_id, data["period"])
        write_profit_workbook(profit_path, data["metrics"], data["summary"], run_id, data["period"])
        summary = {
            **data["summary"],
            "run_id": run_id,
            "generated_at": utils.utc_now_iso(),
            "period": data["period"],
            "days": data["days"],
            "seed": data["seed"],
            "notice": "固定种子模拟经营数据；不接入真实店铺/广告/库存后台。",
            "metrics": data["metrics"],
            "outputs": {
                "ad": _display(config.root, ad_path),
                "inventory": _display(config.root, inventory_path),
                "profit": _display(config.root, profit_path),
                "summary": _display(config.root, output_dir / str(config.get("output.summary_file", "report_summary.json"))),
            },
        }
        utils.write_json(output_dir / str(config.get("output.summary_file", "report_summary.json")), summary)
    except (ReportError, utils.UtilError, OSError, ValueError) as exc:
        logger.exception("报表生成失败: %s", exc)
        print(f"✗ 报表生成失败：{exc}", file=sys.stderr)
        return 1

    print("")
    print("=" * 72)
    print(f"✓ 经营报表生成完成：{run_id}")
    print(f"  周期    : {data['period']}（{data['days']} 天）")
    print(f"  收入    : ${data['summary']['revenue']:,.2f}")
    print(
        f"  净利润  : ${data['summary']['net_profit']:,.2f}  |  "
        f"ROI {data['summary']['roi']:.2f}%  |  ACOS {data['summary']['ad_acos']:.2f}%"
    )
    print(f"  库存预警: {data['summary']['inventory_alerts']} 个 SKU")
    print(f"  广告日报: {summary['outputs']['ad']}")
    print(f"  库存预警: {summary['outputs']['inventory']}")
    print(f"  月度利润: {summary['outputs']['profit']}")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "report_generator"))
````

## `scripts/check_syntax.py`

````python
#!/usr/bin/env python3
"""项目静态校验：Python AST/编译、YAML、JSON、JSONL 与目录结构。

用法：
    python scripts/check_syntax.py
    python scripts/check_syntax.py --root .
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SKIP_DIRS = {
    ".git",
    ".venv",
    ".vendor",
    "venv",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".ruff_cache",
    ".taste-skill",
}
REQUIRED_FILES = (
    "README.md",
    "requirements.txt",
    "main.py",
    "utils.py",
    "product_research.py",
    "listing_generator.py",
    "competitor_monitor.py",
    "compliance_check.py",
    "report_generator.py",
    "interview_demo.py",
    "error_guard.py",
    "app.py",
    "start_all.ps1",
    "start_all.sh",
    ".streamlit/config.toml",
    "config/settings.yaml",
    "config/product_research.yaml",
    "config/amazon_listing_profile.yaml",
    "config/listing_copy_rules.yaml",
    "config/competitor_monitor.yaml",
    "config/compliance_rules.yaml",
    "config/report_generator.yaml",
)
REQUIRED_DIRS = (
    "config",
    "data/mock",
    "docs",
    "ess_ai",
    "ess_ai/collectors",
    "ess_ai/processing",
    "ess_ai/analysis",
    "ess_ai/listing",
    "ess_ai/content",
    "ess_ai/compliance",
    "ess_ai/reporting",
    "ess_ai/pipelines",
    "ess_ai/integrations",
    "ess_ai/storage",
    "outputs",
    "prompts",
    "scripts",
    "tests",
)
PACKAGE_DIRS = (
    "ess_ai",
    "ess_ai/collectors",
    "ess_ai/processing",
    "ess_ai/analysis",
    "ess_ai/listing",
    "ess_ai/content",
    "ess_ai/compliance",
    "ess_ai/reporting",
    "ess_ai/pipelines",
    "ess_ai/integrations",
    "ess_ai/storage",
)


def _iter_files(root: Path, suffix: str) -> list[Path]:
    return sorted(
        path
        for path in root.rglob(f"*{suffix}")
        if path.is_file()
        and not any(part in SKIP_DIRS for part in path.parts)
        and not any(part.startswith(".pytest") or part == "_artifacts" for part in path.parts)
    )


def check_python(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    files = _iter_files(root, ".py")
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            compile(tree, str(path), "exec")
        except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{path.relative_to(root)}: {type(exc).__name__}: {exc}")
    return len(files), errors


def check_json(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    files = _iter_files(root, ".json")
    for path in files:
        try:
            with path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: JSON 解析失败: {exc}")
    return len(files), errors


def check_jsonl(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    files = _iter_files(root, ".jsonl")
    for path in files:
        line_no = 0
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line_no += 1
                    if line.strip():
                        json.loads(line)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: JSONL 解析失败（第 {line_no} 行）: {exc}")
    return len(files), errors


def check_yaml(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    files = _iter_files(root, ".yml") + _iter_files(root, ".yaml")
    try:
        import yaml
    except ImportError:
        return 0, ["PyYAML 未安装，跳过 YAML 校验（pip install PyYAML）"]
    for path in sorted(set(files)):
        try:
            with path.open("r", encoding="utf-8") as handle:
                yaml.safe_load(handle)
        except Exception as exc:  # YAML 异常类型较多，统一收集
            errors.append(f"{path.relative_to(root)}: YAML 解析失败: {exc}")
    return len(set(files)), errors


def check_structure(root: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (root / name).exists():
            errors.append(f"缺少必需文件: {name}")
    for name in REQUIRED_DIRS:
        if not (root / name).is_dir():
            errors.append(f"缺少必需目录: {name}")
    for name in PACKAGE_DIRS:
        init_file = root / name / "__init__.py"
        if not init_file.exists():
            errors.append(f"缺少包初始化文件: {name}/__init__.py")
    return errors


def _configure_stdio() -> None:
    """在 Windows GBK 控制台下强制 UTF-8，避免中文/符号输出失败。"""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="校验项目语法与结构")
    parser.add_argument("--root", default=".", help="项目根目录")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()

    results: dict[str, Any] = {}
    errors: list[str] = []

    py_count, py_errors = check_python(root)
    results["python_files"] = py_count
    errors.extend(py_errors)

    json_count, json_errors = check_json(root)
    results["json_files"] = json_count
    errors.extend(json_errors)

    jsonl_count, jsonl_errors = check_jsonl(root)
    results["jsonl_files"] = jsonl_count
    errors.extend(jsonl_errors)

    yaml_count, yaml_errors = check_yaml(root)
    results["yaml_files"] = yaml_count
    errors.extend(yaml_errors)

    structure_errors = check_structure(root)
    errors.extend(structure_errors)

    print("=" * 62)
    print("项目静态校验")
    print(f"根目录      : {root}")
    print(f"Python 文件 : {py_count}")
    print(f"JSON 文件   : {json_count}")
    print(f"JSONL 文件  : {jsonl_count}")
    print(f"YAML 文件   : {yaml_count}")
    print(f"结构检查    : {'通过' if not structure_errors else '失败'}")
    print("=" * 62)

    if errors:
        print(f"✗ 发现 {len(errors)} 个问题：")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("✓ 所有 Python 文件可解析、可编译；YAML/JSON 可解析；目录结构完整。")
    return 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "check_syntax"))
````

## `scripts/export_bundle.py`

````python
#!/usr/bin/env python3
"""把项目源码导出为单个可复制 Markdown 文件。

只导出源码、配置、文档与 mock 数据；不包含 outputs、日志、缓存、虚拟环境。
用法：
    python scripts/export_bundle.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

INCLUDE_SUFFIXES = {
    ".py",
    ".yaml",
    ".yml",
    ".toml",
    ".md",
    ".txt",
    ".ps1",
    ".sh",
    ".json",
}
INCLUDE_NAMES = {".env.example", "requirements.txt", "start.sh", "start.ps1"}
SKIP_DIRS = {
    ".git",
    ".venv",
    ".vendor",
    "venv",
    "__pycache__",
    "node_modules",
    "outputs",
    "logs",
    "raw",
    "processed",
    "external",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
    ".taste-skill",
    "htmlcov",
    "_artifacts",
}
SKIP_FILES = {"FULL_CODE.md"}
LANG = {
    ".py": "python",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".md": "markdown",
    ".json": "json",
    ".ps1": "powershell",
    ".sh": "bash",
}


def _selected(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return False
    if path.name in INCLUDE_NAMES:
        return True
    return path.suffix.lower() in INCLUDE_SUFFIXES


def _ordered_files(root: Path) -> list[Path]:
    priority = [
        "README.md",
        "requirements.txt",
        "main.py",
        "utils.py",
        "pyproject.toml",
        ".env.example",
        "start.ps1",
        "start.sh",
    ]
    all_files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and _selected(path)
        and not any(part in SKIP_DIRS or part.startswith(".pytest") for part in path.parts)
        and (path.name == ".env.example" or not path.name.startswith(".env."))
    ]
    ordered: list[Path] = []
    for name in priority:
        candidate = root / name
        if candidate in all_files:
            ordered.append(candidate)
    remainder = sorted(
        (path for path in all_files if path not in ordered),
        key=lambda p: (0 if p.parts[-1] == "__init__.py" else 1, str(p).lower()),
    )
    return ordered + remainder


def build(root: Path, output: Path) -> tuple[int, int]:
    files = _ordered_files(root)
    chunks = [
        "# 欧美轻量化户外储能全链路 AI 自动化系统 · 全量源码",
        "",
        "> 本文件由 `python scripts/export_bundle.py` 自动生成。",
        "> 所有代码均为离线模拟版，不接入任何电商平台真实店铺 API。",
        "",
        f"- 项目根目录：`{root}`",
        f"- 文件数量：{len(files)}",
        "",
        "## 文件索引",
        "",
    ]
    for path in files:
        chunks.append(f"- `{path.relative_to(root).as_posix()}`")
    chunks.extend(["", "---", ""])

    for path in files:
        relative = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        language = LANG.get(suffix, "")
        content = path.read_text(encoding="utf-8")
        chunks.extend(
            [
                f"## `{relative}`",
                "",
                f"````{language}",
                content.rstrip("\n"),
                "````",
                "",
            ]
        )
    text = "\n".join(chunks) + "\n"
    output.write_text(text, encoding="utf-8", newline="\n")
    return len(files), len(text.encode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="导出全量源码 Markdown")
    parser.add_argument("--root", default=".", help="项目根目录")
    parser.add_argument("--output", default="FULL_CODE.md", help="输出文件名")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    output = (root / args.output).resolve()
    count, size = build(root, output)
    print(f"✓ 已导出 {count} 个文件 -> {output}（{size / 1024:.1f} KB）")
    return 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "export_bundle"))
````

## `start_all.ps1`

````powershell
﻿# =============================================================================
# 全链路一键启动：检查环境 → 启动 Streamlit → 等待健康检查 → 打开浏览器
# 用法：
#   powershell -ExecutionPolicy Bypass -File .\start_all.ps1
#   powershell -ExecutionPolicy Bypass -File .\start_all.ps1 -Port 8501 -NoBrowser
# =============================================================================
param(
    [int]$Port = 8501,
    [switch]$SkipInstall,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
Set-Location -Path $Root
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$Runtime = Join-Path $Root ".runtime"
$Logs = Join-Path $Root "outputs\logs"
New-Item -ItemType Directory -Force -Path $Runtime, $Logs | Out-Null

function Resolve-Python {
    param([string]$Root, [bool]$SkipInstall)
    $venvPython = Join-Path $Root ".venv\Scripts\python.exe"
    if (Test-Path $venvPython) {
        return @{ Path = $venvPython; Mode = "venv" }
    }
    $vendorStreamlit = Join-Path $Root ".vendor\streamlit"
    if (Test-Path $vendorStreamlit) {
        $env:PYTHONPATH = (Join-Path $Root ".vendor")
        return @{ Path = "python"; Mode = "vendor" }
    }
    try {
        & python -c "import streamlit" 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return @{ Path = "python"; Mode = "system" }
        }
    } catch { }
    if ($SkipInstall) {
        throw "未找到可用的 Streamlit。请先运行 start_all.ps1（不带 -SkipInstall）或安装 requirements.txt。"
    }
    Write-Host "[1/4] 创建虚拟环境 .venv ..." -ForegroundColor Cyan
    & python -m venv (Join-Path $Root ".venv")
    $env:PYTHONPATH = ""
    return @{ Path = $venvPython; Mode = "venv" }
}

$pythonInfo = Resolve-Python -Root $Root -SkipInstall:$SkipInstall
$Python = $pythonInfo.Path
Write-Host "[2/4] 环境：$($pythonInfo.Mode) / $Python" -ForegroundColor DarkGray

if (-not $SkipInstall) {
    $needInstall = $false
    if ($pythonInfo.Mode -eq "venv") {
        & $Python -c "import streamlit" 2>$null | Out-Null
        $needInstall = ($LASTEXITCODE -ne 0)
    }
    if ($needInstall) {
        Write-Host "[3/4] 安装依赖（首次可能 1-3 分钟）..." -ForegroundColor Cyan
        & $Python -m pip install --upgrade pip
        & $Python -m pip install -r (Join-Path $Root "requirements.txt")
    } else {
        Write-Host "[3/4] 依赖已就绪" -ForegroundColor DarkGray
    }
} else {
    Write-Host "[3/4] 跳过依赖安装" -ForegroundColor Yellow
}

# 已运行则直接打开
try {
    $healthUrl = "http://127.0.0.1:$Port/_stcore/health"
    $existing = Invoke-WebRequest -UseBasicParsing -Uri $healthUrl -TimeoutSec 2
    if ($existing.StatusCode -eq 200) {
        Write-Host "[4/4] Streamlit 已在运行：http://127.0.0.1:$Port" -ForegroundColor Green
        if (-not $NoBrowser) { Start-Process "http://127.0.0.1:$Port" }
        exit 0
    }
} catch { }

# 初始化目录与日志
try { & $Python main.py init | Out-Host } catch { Write-Host "初始化提示：$($_.Exception.Message)" -ForegroundColor Yellow }

$stdout = Join-Path $Logs "streamlit.out.log"
$stderr = Join-Path $Logs "streamlit.err.log"
$pidFile = Join-Path $Runtime "streamlit.pid"
$arguments = @(
    "-m", "streamlit", "run", "app.py",
    "--server.address", "127.0.0.1",
    "--server.port", "$Port",
    "--server.headless", "true",
    "--global.developmentMode", "false",
    "--browser.gatherUsageStats", "false"
)
Write-Host "[4/4] 启动 Streamlit ..." -ForegroundColor Cyan
$process = Start-Process -FilePath $Python -ArgumentList $arguments -WorkingDirectory $Root `
    -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru -WindowStyle Hidden
$process.Id | Set-Content -Path $pidFile -Encoding ascii

$ready = $false
for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Seconds 1
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$Port/_stcore/health" -TimeoutSec 2
        if ($response.StatusCode -eq 200) { $ready = $true; break }
    } catch { }
}

if (-not $ready) {
    Write-Host "✗ Streamlit 启动失败或健康检查超时。" -ForegroundColor Red
    Write-Host "  查看: $stderr" -ForegroundColor Yellow
    if (Test-Path $stderr) { Get-Content $stderr -Tail 40 | Out-Host }
    try { Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue } catch { }
    exit 1
}

Write-Host ""
Write-Host "✓ 系统已启动：http://127.0.0.1:$Port" -ForegroundColor Green
Write-Host "  停止：powershell -ExecutionPolicy Bypass -File .\stop_all.ps1" -ForegroundColor DarkGray
Write-Host "  日志：$Logs" -ForegroundColor DarkGray
if (-not $NoBrowser) { Start-Process "http://127.0.0.1:$Port" }
exit 0
````

## `start_all.sh`

````bash
#!/usr/bin/env bash
# 全链路一键启动（macOS / Linux）
# 用法：./start_all.sh [--port 8501] [--skip-install] [--no-browser]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PORT=8501
SKIP_INSTALL=0
NO_BROWSER=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port) PORT="$2"; shift 2 ;;
    --skip-install) SKIP_INSTALL=1; shift ;;
    --no-browser) NO_BROWSER=1; shift ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

mkdir -p .runtime outputs/logs
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

PYTHON="python3"
if [ -x ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
elif [ -d ".vendor/streamlit" ]; then
  export PYTHONPATH="$ROOT/.vendor${PYTHONPATH:+:$PYTHONPATH}"
elif ! "$PYTHON" -c "import streamlit" >/dev/null 2>&1; then
  if [ "$SKIP_INSTALL" -eq 1 ]; then
    echo "未找到 Streamlit；请先安装 requirements.txt" >&2
    exit 1
  fi
  echo "[1/3] 创建 .venv ..."
  python3 -m venv .venv
  PYTHON=".venv/bin/python"
fi

if [ "$SKIP_INSTALL" -eq 0 ] && [ -x ".venv/bin/python" ]; then
  echo "[2/3] 安装依赖 ..."
  "$PYTHON" -m pip install --upgrade pip
  "$PYTHON" -m pip install -r requirements.txt
fi

open_browser() {
  if [ "$NO_BROWSER" -eq 1 ]; then
    return 0
  fi
  if command -v open >/dev/null 2>&1; then
    open "http://127.0.0.1:${PORT}"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://127.0.0.1:${PORT}" >/dev/null 2>&1 || true
  fi
}

if curl -fsS "http://127.0.0.1:${PORT}/_stcore/health" >/dev/null 2>&1; then
  echo "✓ Streamlit 已在运行：http://127.0.0.1:${PORT}"
  open_browser
  exit 0
fi

"$PYTHON" main.py init || true
nohup "$PYTHON" -m streamlit run app.py \
  --server.address 127.0.0.1 --server.port "$PORT" \
  --server.headless true --global.developmentMode false --browser.gatherUsageStats false \
  > outputs/logs/streamlit.out.log 2> outputs/logs/streamlit.err.log &
echo $! > .runtime/streamlit.pid

for i in $(seq 1 60); do
  if curl -fsS "http://127.0.0.1:${PORT}/_stcore/health" >/dev/null 2>&1; then
    echo "✓ 系统已启动：http://127.0.0.1:${PORT}"
    open_browser
    exit 0
  fi
  sleep 1
done

echo "✗ 启动超时，查看 outputs/logs/streamlit.err.log" >&2
exit 1
````

## `stop_all.ps1`

````powershell
﻿# 停止 start_all.ps1 启动的 Streamlit 进程
$ErrorActionPreference = "SilentlyContinue"
$Root = $PSScriptRoot
$pidFile = Join-Path $Root ".runtime\streamlit.pid"
if (Test-Path $pidFile) {
    $processId = Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($processId) {
        Stop-Process -Id ([int]$processId) -Force -ErrorAction SilentlyContinue
        Write-Host "✓ 已停止 Streamlit（PID $processId）" -ForegroundColor Green
    }
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
} else {
    Write-Host "未找到 .runtime/streamlit.pid；可能未启动或已停止。" -ForegroundColor Yellow
}
````

## `stop_all.sh`

````bash
#!/usr/bin/env bash
# 停止 start_all.sh 启动的 Streamlit
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$ROOT/.runtime/streamlit.pid"
if [ -f "$PID_FILE" ]; then
  PID="$(cat "$PID_FILE")"
  if kill -0 "$PID" >/dev/null 2>&1; then
    kill "$PID"
    echo "✓ 已停止 Streamlit（PID $PID）"
  fi
  rm -f "$PID_FILE"
else
  echo "未找到 .runtime/streamlit.pid；可能未启动或已停止。"
fi
````

## `tests/conftest.py`

````python
"""pytest 路径与临时项目夹具。"""

from __future__ import annotations

import re
import shutil
import sys
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ess_ai.config import Settings, load_settings  # noqa: E402


@pytest.fixture()
def workspace_tmp(request: pytest.FixtureRequest) -> Iterator[Path]:
    """在工作区内创建隔离目录。

    不使用 pytest 默认 ``tmp_path``，因为某些 Windows 沙箱/受限 ACL 环境
    不允许 pytest 对系统临时目录执行清理。这里保留产物、不自动删除。
    """

    safe_name = re.sub(r"[^\w.\-]+", "_", request.node.name)[:60]
    target = PROJECT_ROOT / "tests" / "_artifacts" / f"{safe_name}_{uuid.uuid4().hex[:8]}"
    target.mkdir(parents=True, exist_ok=True)
    yield target
    shutil.rmtree(target, ignore_errors=True)


@pytest.fixture()
def temp_settings(workspace_tmp: Path) -> Settings:
    """复制配置与 mock 数据到临时目录，避免污染真实 outputs。"""

    shutil.copytree(PROJECT_ROOT / "config", workspace_tmp / "config")
    shutil.copytree(PROJECT_ROOT / "data" / "mock", workspace_tmp / "data" / "mock")
    settings = load_settings(root=workspace_tmp)
    settings.ensure_directories()
    return settings
````

## `tests/test_competitor_monitor.py`

````python
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
````

## `tests/test_final_integration.py`

````python
"""最终整合：全局异常捕获、Streamlit 启动与入口文件测试。"""

from __future__ import annotations

from pathlib import Path

import pytest

import error_guard

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_error_guard_writes_human_and_jsonl(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(error_guard, "LOG_DIR", tmp_path)
    monkeypatch.setattr(error_guard, "HUMAN_LOG", tmp_path / "errors.log")
    monkeypatch.setattr(error_guard, "JSONL_LOG", tmp_path / "errors.jsonl")
    error_guard.log_exception(RuntimeError("demo failure"), app="test", context={"step": "unit"})
    assert "demo failure" in (tmp_path / "errors.log").read_text(encoding="utf-8")
    assert '"app": "test"' in (tmp_path / "errors.jsonl").read_text(encoding="utf-8")


def test_run_cli_catches_unhandled(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(error_guard, "LOG_DIR", tmp_path)
    monkeypatch.setattr(error_guard, "HUMAN_LOG", tmp_path / "errors.log")
    monkeypatch.setattr(error_guard, "JSONL_LOG", tmp_path / "errors.jsonl")

    def broken(_argv):
        raise RuntimeError("boom")

    assert error_guard.run_cli(broken, "broken_entry") == 1
    output = capsys.readouterr().err
    assert "未捕获异常" in output
    assert "boom" in (tmp_path / "errors.log").read_text(encoding="utf-8")


def test_streamlit_app_boots_without_exception() -> None:
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(PROJECT_ROOT / "app.py"), default_timeout=90)
    app.run()
    assert not app.exception
    nav = next(radio for radio in app.radio if "总览" in radio.options)
    assert nav.options == ["总览", "选品研究", "上架素材", "竞品监控", "合规校验", "经营报表", "面试演示"]
    assert "运行全链路" in [button.label for button in app.button]

    expected = {
        "选品研究": "运行选品",
        "上架素材": "生成 Listing",
        "竞品监控": "巡检竞品",
        "合规校验": "合规筛查",
        "经营报表": "生成报表",
        "面试演示": "生成演示脚本",
    }
    for page, action in expected.items():
        nav = next(radio for radio in app.radio if "总览" in radio.options)
        nav.set_value(page).run()
        assert not app.exception
        assert action in [button.label for button in app.button]
        if page == "经营报表":
            assert len(app.tabs) == 3
````

## `tests/test_listing_generator.py`

````python
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
````

## `tests/test_operations_reports.py`

````python
"""合规筛查与经营报表：公式、结构和 Excel 输出测试。"""

from __future__ import annotations

from pathlib import Path

from compliance_check import (
    DEFAULT_MASTER,
    DEFAULT_RULES,
    DEFAULT_SELECTION,
    ComplianceChecker,
    _load_selection,
    export_excel,
    load_master,
    load_rules,
)
from report_generator import (
    OperationsSimulator,
    load_config,
    load_products,
    write_ad_workbook,
    write_inventory_workbook,
    write_profit_workbook,
)


def test_compliance_rules_and_scores(workspace_tmp: Path) -> None:
    rules = load_rules(DEFAULT_RULES)
    products = load_master(DEFAULT_MASTER, _load_selection(DEFAULT_SELECTION))
    rows, findings = ComplianceChecker(rules).check(products)

    assert len(products) == 9
    assert len(rows) == 9
    assert findings
    assert any(item.standard_id == "EU_LVD" for item in findings)
    assert any(item.standard_id == "US_FCC15B" for item in findings)

    by_sku = {row["sku"]: row for row in rows}
    assert by_sku["1688-600000000005"]["eu_status"] == "PASS"
    assert by_sku["AMZ-B0DEMO0003"]["us_status"] == "PASS"
    assert by_sku["1688-600000000001"]["status"] == "FAIL"

    for row in rows:
        expected = max(
            0.0,
            100.0 - 25.0 * row["high"] - 10.0 * row["medium"] - 5.0 * row["low"],
        )
        assert abs(row["risk_score"] - round(expected, 1)) <= 0.05
        assert row["status"] in {"PASS", "CONDITIONAL", "FAIL"}

    output = workspace_tmp / "compliance.xlsx"
    export_excel(rows, findings, products, rules, output, run_id="test", generated_at="2026-10-21T00:00:00+00:00")
    import openpyxl

    wb = openpyxl.load_workbook(output, data_only=True)
    assert wb.sheetnames == ["合规汇总", "不符合项", "产品参数", "标准依据"]
    assert wb["合规汇总"].max_row == 6 + len(rows) - 1
    assert wb["不符合项"].max_row == 6 + len(findings) - 1
    assert [cell.value for cell in wb["合规汇总"][5]][:4] == ["SKU", "型号", "商品", "平台"]


def test_operations_formulas_and_excel(workspace_tmp: Path) -> None:
    config = load_config()
    products = load_products(config.resolve("input.selection"))
    data = OperationsSimulator(config, products).run()
    ad_rows = data["ad_rows"]
    metrics = data["metrics"]

    assert len(ad_rows) == 270
    assert len(metrics) == 9
    assert data["summary"]["units"] == sum(item["units"] for item in metrics)

    for row in ad_rows:
        assert abs(row["ctr"] - row["clicks"] / row["impressions"]) <= 1e-6
        assert abs(row["cvr"] - row["ad_orders"] / row["clicks"]) <= 1e-6
        assert abs(row["acos"] - row["spend"] / row["ad_sales"]) <= 1e-5
        assert abs(row["roas"] - row["ad_sales"] / row["spend"]) <= 0.01
        assert abs(
            row["ad_profit"]
            - round(row["ad_sales"] * row["gross_margin_pct"] / 100 - row["spend"], 2)
        ) <= 0.01

    for item in metrics:
        assert abs(item["revenue"] - item["units"] * item["price"]) <= 0.02
        assert abs(item["gross_profit"] - (item["revenue"] - item["cogs"])) <= 0.02
        assert abs(item["net_profit"] - (item["revenue"] - item["total_cost"])) <= 0.02
        assert abs(item["roi"] - item["net_profit"] / item["total_cost"]) <= 1e-9
        assert abs(item["net_margin"] - item["net_profit"] / item["revenue"]) <= 1e-9
        assert abs(
            item["inventory_turnover_days"]
            - round(item["avg_inventory_units"] / item["avg_daily_units"], 1)
        ) <= 0.06
        assert abs(item["days_cover"] - round((item["on_hand"] + item["in_transit"]) / item["avg_daily_units"], 1)) <= 0.06
        assert abs(item["reorder_point"] - round(item["avg_daily_units"] * (item["lead_time_days"] + item["safety_days"]), 1)) <= 0.06
        assert item["suggested_order_qty"] >= 0
        if item["days_cover"] < item["lead_time_days"]:
            assert item["stock_status"] == "紧急补货"
        elif item["days_cover"] < item["lead_time_days"] + item["safety_days"]:
            assert item["stock_status"] == "关注"
        elif item["days_cover"] > 90:
            assert item["stock_status"] == "滞销"
        else:
            assert item["stock_status"] == "健康"

    summary = data["summary"]
    total_cost = sum(item["total_cost"] for item in metrics)
    assert abs(summary["roi"] - summary["net_profit"] / total_cost * 100) <= 0.02
    assert abs(summary["net_margin"] - summary["net_profit"] / summary["revenue"] * 100) <= 0.02

    ad_path = workspace_tmp / "ad.xlsx"
    inventory_path = workspace_tmp / "inventory.xlsx"
    profit_path = workspace_tmp / "profit.xlsx"
    write_ad_workbook(ad_path, ad_rows, summary, "test", data["period"])
    write_inventory_workbook(inventory_path, metrics, "test", data["period"])
    write_profit_workbook(profit_path, metrics, summary, "test", data["period"])
    import openpyxl

    wb_ad = openpyxl.load_workbook(ad_path, data_only=True)
    assert wb_ad.sheetnames == ["广告日报", "指标说明"]
    assert wb_ad["广告日报"].max_row == 277
    assert wb_ad["广告日报"].cell(row=7, column=1).value is not None

    wb_inv = openpyxl.load_workbook(inventory_path, data_only=True)
    assert wb_inv.sheetnames == ["库存预警", "指标说明"]
    assert wb_inv["库存预警"].max_row == 15

    wb_profit = openpyxl.load_workbook(profit_path, data_only=True)
    assert wb_profit.sheetnames == ["经营概览", "月度利润", "指标说明"]
    assert wb_profit["月度利润"].max_row == 16
    assert wb_profit["经营概览"]["A1"].value.startswith("月度经营概览")
````

## `tests/test_pipeline.py`

````python
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
````

## `tests/test_product_research.py`

````python
"""选品模块：清洗、指标自洽性与 Excel 输出测试。"""

from __future__ import annotations

from pathlib import Path

import utils
from product_research import (
    Alibaba1688Adapter,
    AliExpressAdapter,
    AmazonAdapter,
    ProductCleaner,
    ProductResearchEngine,
    PublicFetcher,
    _extract_spec,
    apply_overrides,
    load_research_config,
)


def test_extract_spec_from_title() -> None:
    title = "300Wh Portable Power Station 300W 4.2kg"
    assert _extract_spec(title, "capacity_wh") == 300
    assert _extract_spec(title, "output_w") == 300
    assert _extract_spec(title, "weight_kg") == 4.2


def test_public_page_adapters_parse_minimal_cards() -> None:
    config = load_research_config()
    fetcher = PublicFetcher(config)
    platforms = dict(config.platform_items())

    amazon_html = """
    <div data-component-type="s-search-result" data-asin="B0TEST0001">
      <h2><a href="/dp/B0TEST0001"><span>Demo 300Wh Portable Power Station 300W</span></a></h2>
      <span class="a-price"><span class="a-offscreen">$299.00</span></span>
      <span class="a-icon-alt">4.5 out of 5 stars</span>
      <a href="/product-reviews/B0TEST0001"><span>1,234</span></a>
    </div>
    """
    amazon = AmazonAdapter("amazon", platforms["amazon"], fetcher).parse(
        amazon_html, "https://www.amazon.com/s?k=test"
    )
    assert amazon[0]["product_id"] == "B0TEST0001"
    assert amazon[0]["price_local"] == 299.0
    assert amazon[0]["review_count"] == 1234

    aliexpress_html = """
    <div class="search-item-card-wrapper-gallery">
      <a href="https://www.aliexpress.com/item/1005009999999.html">
        <h3>Demo 200Wh Portable Power Station 200W</h3>
        <div class="seo-optimized-price">US $139.00</div>
      </a>
    </div>
    """
    ali = AliExpressAdapter("aliexpress", platforms["aliexpress"], fetcher).parse(
        aliexpress_html, "https://www.aliexpress.com/w/wholesale-test.html"
    )
    assert ali[0]["product_id"] == "1005009999999"
    assert ali[0]["price_local"] == 139.0

    alibaba_html = """
    <div data-offer-id="600000009999">
      <a href="https://detail.1688.com/offer/600000009999.html">
        <div class="title-text">户外电源 300Wh 露营便携式储能电源</div>
        <div class="price">¥780.00</div>
      </a>
    </div>
    """
    alibaba = Alibaba1688Adapter("alibaba_1688", platforms["alibaba_1688"], fetcher).parse(
        alibaba_html, "https://s.1688.com/selloffer/offer_search.htm?keywords=test"
    )
    assert alibaba[0]["product_id"] == "600000009999"
    assert alibaba[0]["price_local"] == 780.0


def test_cleaner_filters_and_dedupes() -> None:
    config = load_research_config()
    cleaner = ProductCleaner(config)
    fixture = utils.read_json(config.resolve("fixture.path"))
    records = fixture["records"]
    duplicated = dict(records[0])
    duplicated["product_id"] = "DUPLICATE-ID"
    rows, stats = cleaner.clean([*records, duplicated])
    assert stats["clean_records"] == len(rows)
    assert all(100 <= row["capacity_wh"] <= 500 for row in rows)
    assert stats["dropped_by_reason"].get("capacity_out_of_range", 0) >= 4
    assert stats["dropped_by_reason"].get("duplicate_title", 0) >= 1


def test_full_research_run_and_metric_consistency(workspace_tmp: Path) -> None:
    config = load_research_config()
    config = apply_overrides(config, output_dir=str(workspace_tmp / "research"))
    summary = ProductResearchEngine(config).run(mode="offline")

    assert summary["raw_records"] == 26
    assert summary["cleaned_records"] == 20
    assert summary["high_potential_records"] >= 5
    assert summary["outputs"]["summary"].endswith("research_summary.json")

    rows = utils.read_csv(config.root / summary["outputs"]["csv"])
    assert len(rows) == summary["cleaned_records"]
    for row in rows:
        capacity = float(row["capacity_wh"])
        weight = float(row["weight_kg"])
        retail = float(row["retail_price_usd"])
        landed = float(row["landed_cost_usd"])
        fee = float(row["platform_fee_usd"])
        fulfillment = float(row["fulfillment_cost_usd"])
        gross = float(row["gross_profit_usd"])
        margin = float(row["gross_margin_pct"])
        market = float(row["market_capacity_usd"])
        monthly_units = int(float(row["monthly_units"]))
        competition = float(row["competition_score"])

        assert 100 <= capacity <= 500
        assert weight > 0
        assert retail > 0
        assert abs(gross - round(retail - landed - fee - fulfillment, 2)) <= 0.02
        assert abs(margin - round(gross / retail * 100, 2)) <= 0.05
        assert abs(market - round(monthly_units * retail, 2)) <= 0.02
        assert 0 <= competition <= 100

    passing = [row for row in rows if row["gate_status"] == "通过"]
    assert len(passing) == summary["high_potential_records"]
    for row in passing:
        assert float(row["gross_margin_pct"]) >= summary["filters"]["min_gross_margin_pct"]
        assert float(row["market_capacity_usd"]) >= summary["filters"]["min_market_capacity_usd"]
        assert float(row["competition_score"]) <= summary["filters"]["max_competition_score"]
        assert float(row["opportunity_score"]) >= summary["filters"]["min_opportunity_score"]


def test_excel_structure_and_headers(workspace_tmp: Path) -> None:
    config = load_research_config()
    config = apply_overrides(config, output_dir=str(workspace_tmp / "excel"))
    summary = ProductResearchEngine(config).run(mode="offline")
    workbook_path = config.root / summary["outputs"]["excel"]

    import openpyxl

    wb = openpyxl.load_workbook(workbook_path, data_only=True)
    assert wb.sheetnames == ["高潜力选品", "全部清洗数据", "指标说明", "筛选参数", "数据质量"]

    high_ws = wb["高潜力选品"]
    headers = [cell.value for cell in high_ws[6]]
    assert headers[:4] == ["排名", "平台", "商品标题", "品牌/供应商"]
    assert "毛利率(%)" in headers
    assert "市场容量(USD/月)" in headers
    assert "竞争度(越低越好)" in headers
    assert "综合机会分" in headers
    assert high_ws.max_row == 6 + summary["high_potential_records"]
    assert high_ws["A1"].value.startswith("户外露营轻量化储能")

    column = {name: index + 1 for index, name in enumerate(headers)}
    for row_index in range(7, high_ws.max_row + 1):
        retail = high_ws.cell(row=row_index, column=column["零售基准价(USD)"]).value
        landed = high_ws.cell(row=row_index, column=column["到岸成本(USD)"]).value
        fee = high_ws.cell(row=row_index, column=column["平台佣金(USD)"]).value
        fulfillment = high_ws.cell(row=row_index, column=column["履约成本(USD)"]).value
        gross = high_ws.cell(row=row_index, column=column["单件毛利(USD)"]).value
        margin = high_ws.cell(row=row_index, column=column["毛利率(%)"]).value
        market = high_ws.cell(row=row_index, column=column["市场容量(USD/月)"]).value
        units = high_ws.cell(row=row_index, column=column["预估月销量"]).value
        assert abs(gross - round(retail - landed - fee - fulfillment, 2)) <= 0.02
        assert abs(margin - round(gross / retail * 100, 2)) <= 0.05
        assert abs(market - round(units * retail, 2)) <= 0.02
        assert high_ws.cell(row=row_index, column=column["门槛状态"]).value == "通过"

    all_ws = wb["全部清洗数据"]
    assert all_ws.max_row == 1 + summary["cleaned_records"]
    assert all_ws.cell(row=2, column=1).value is not None

    assert wb["指标说明"].max_row >= 8
    assert wb["筛选参数"].max_row > 10
    assert wb["数据质量"].max_row > 5
````

## `tests/test_utils.py`

````python
"""公共工具模块测试。"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

import utils


def test_text_roundtrip_and_default(workspace_tmp: Path) -> None:
    target = workspace_tmp / "nested" / "note.txt"
    utils.write_text(target, "第一行\n第二行\n")
    assert utils.read_text(target) == "第一行\n第二行\n"
    assert utils.read_text(workspace_tmp / "missing.txt", default="fallback") == "fallback"
    with pytest.raises(utils.FileIOError):
        utils.read_text(workspace_tmp / "missing.txt")


def test_json_roundtrip_and_atomic(workspace_tmp: Path) -> None:
    target = workspace_tmp / "data.json"
    payload = {"name": "Nomad 600", "capacity": 600, "tags": ["露营", "solar"]}
    utils.write_json(target, payload)
    assert utils.read_json(target) == payload
    assert not list(workspace_tmp.glob("*.tmp"))


def test_jsonl_roundtrip(workspace_tmp: Path) -> None:
    target = workspace_tmp / "rows.jsonl"
    rows = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
    utils.write_jsonl(target, rows)
    assert utils.read_jsonl(target) == rows


def test_yaml_roundtrip(workspace_tmp: Path) -> None:
    target = workspace_tmp / "config.yaml"
    payload = {"project": {"name": "户外储能", "markets": ["US", "DE"]}}
    utils.write_yaml(target, payload)
    assert utils.read_yaml(target) == payload


def test_csv_roundtrip(workspace_tmp: Path) -> None:
    target = workspace_tmp / "rows.csv"
    rows = [{"market": "US", "price": 499}, {"market": "DE", "price": 541}]
    utils.write_csv(target, rows, fieldnames=["market", "price"])
    loaded = utils.read_csv(target)
    assert loaded[0]["market"] == "US"
    assert loaded[1]["price"] == "541"


def test_file_sha256_and_human_size(workspace_tmp: Path) -> None:
    target = workspace_tmp / "hash.txt"
    utils.write_text(target, "abc")
    assert len(utils.file_sha256(target)) == 64
    assert utils.human_size(2048) == "2.0 KB"


def test_deep_get_and_merge() -> None:
    data = {"a": {"b": [{"c": 3}]}}
    assert utils.deep_get(data, "a.b.0.c") == 3
    assert utils.deep_get(data, "a.missing", default=9) == 9
    merged = utils.deep_merge({"a": {"x": 1}, "keep": True}, {"a": {"y": 2}})
    assert merged == {"a": {"x": 1, "y": 2}, "keep": True}


def test_safe_filename() -> None:
    assert utils.safe_filename("US / Nomad: 600") == "US_Nomad_600"
    assert utils.safe_filename("   ") == "untitled"


def test_logging_writes_file(workspace_tmp: Path) -> None:
    log_file = workspace_tmp / "logs" / "app.log"
    utils.setup_logging(level="INFO", log_file=log_file, console=False, force=True)
    logger = utils.get_logger("test")
    logger.info("hello %s", "world")
    logging.getLogger(utils.APP_LOGGER_NAME).handlers[0].flush()
    content = log_file.read_text(encoding="utf-8")
    assert "hello world" in content
    assert "test" in content
    utils.setup_logging(level="WARNING", log_file=None, console=False, force=True)
````

