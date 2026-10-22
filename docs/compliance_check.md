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
