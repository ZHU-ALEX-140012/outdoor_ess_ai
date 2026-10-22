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
