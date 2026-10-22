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
