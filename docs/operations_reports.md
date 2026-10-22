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
