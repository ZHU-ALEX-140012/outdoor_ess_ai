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
