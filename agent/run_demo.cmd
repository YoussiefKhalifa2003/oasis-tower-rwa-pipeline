@echo off
cd /d "%~dp0"
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
) else (
  py -3 orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
)
echo.
echo Sample output: sample_outputs\oasis_tower_rwa.output.json
pause
