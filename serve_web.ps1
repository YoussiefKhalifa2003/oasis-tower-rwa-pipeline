# Serve landing page locally. Usage: .\serve_web.ps1
Set-Location (Join-Path $PSScriptRoot "web")
Write-Host "Open http://localhost:8123" -ForegroundColor Green
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    python -m http.server 8123
} else {
    py -3 -m http.server 8123
}
