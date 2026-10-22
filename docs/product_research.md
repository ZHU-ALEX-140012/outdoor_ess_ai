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
