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
