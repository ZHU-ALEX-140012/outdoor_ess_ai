#!/usr/bin/env bash
# 停止 start_all.sh 启动的 Streamlit
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$ROOT/.runtime/streamlit.pid"
if [ -f "$PID_FILE" ]; then
  PID="$(cat "$PID_FILE")"
  if kill -0 "$PID" >/dev/null 2>&1; then
    kill "$PID"
    echo "✓ 已停止 Streamlit（PID $PID）"
  fi
  rm -f "$PID_FILE"
else
  echo "未找到 .runtime/streamlit.pid；可能未启动或已停止。"
fi
