@echo off
cd /d "%~dp0web"
echo Open http://localhost:8123
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python -m http.server 8123
) else (
  py -3 -m http.server 8123
)
