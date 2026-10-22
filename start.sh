#!/usr/bin/env bash
# Compatibility alias: old start.sh now launches the full Streamlit console.
exec "$(cd "$(dirname "$0")" && pwd)/start_all.sh" "$@"
