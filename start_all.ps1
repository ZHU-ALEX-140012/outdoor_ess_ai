# =============================================================================
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
