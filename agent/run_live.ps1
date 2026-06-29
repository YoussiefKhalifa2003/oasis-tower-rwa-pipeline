# Live Kimi run (requires KIMI_API_KEY in environment). Usage: .\run_live.ps1
Set-Location $PSScriptRoot
if (-not $env:KIMI_API_KEY) {
    Write-Host "Set KIMI_API_KEY first: `$env:KIMI_API_KEY='sk-...'" -ForegroundColor Red
    exit 1
}
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --live --redact --yes `
      --out sample_outputs/oasis_tower_rwa.live.json
} else {
    py -3 orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --live --redact --yes `
      --out sample_outputs/oasis_tower_rwa.live.json
}
Write-Host "`nLive output: sample_outputs/oasis_tower_rwa.live.json" -ForegroundColor Green
