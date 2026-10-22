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



