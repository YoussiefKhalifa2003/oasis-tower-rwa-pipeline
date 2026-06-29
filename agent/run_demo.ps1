# Run Oasis Tower RWA pipeline (mock). Usage: .\run_demo.ps1
Set-Location $PSScriptRoot
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
} else {
    py -3 orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
}
Write-Host "`nSample output: sample_outputs/oasis_tower_rwa.output.json" -ForegroundColor Green
