# 停止 start_all.ps1 启动的 Streamlit 进程
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
