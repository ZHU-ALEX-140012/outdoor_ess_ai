# Compatibility alias: old start.ps1 now launches the full Streamlit console.
& "$PSScriptRoot\start_all.ps1" @args
exit $LASTEXITCODE
