@echo off
cd /d "%~dp0"
if "%KIMI_API_KEY%"=="" (
  echo Set KIMI_API_KEY first: set KIMI_API_KEY=sk-...
  exit /b 1
)
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --live --redact --yes --out sample_outputs/oasis_tower_rwa.live.json
) else (
  py -3 orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --live --redact --yes --out sample_outputs/oasis_tower_rwa.live.json
)
echo.
echo Live output: sample_outputs\oasis_tower_rwa.live.json
