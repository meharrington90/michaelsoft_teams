@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "PYTHON_DIR=%SCRIPT_DIR%python"
set "VENV_DIR=%SCRIPT_DIR%.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "UV_DIR=%SCRIPT_DIR%.tools\uv\bin"
set "UV_BIN=%UV_DIR%\uv.exe"

if not exist "%VENV_PY%" (
  call :ensure_runtime
  if errorlevel 1 goto runtime_failed
)

call "%VENV_PY%" -c "import ccl_chromium_reader" >nul 2>nul
if errorlevel 1 (
  echo Installing dependencies...
  call "%VENV_PY%" "%PYTHON_DIR%\bootstrap_dependencies.py"
  if errorlevel 1 goto install_failed
)

call "%VENV_PY%" "%PYTHON_DIR%\run_teams_pipeline.py" --open-browser %*
set "STATUS=%ERRORLEVEL%"
echo.
exit /b %STATUS%

:ensure_runtime
where py >nul 2>nul
if not errorlevel 1 (
  echo Creating runtime with local Python...
  call py -3 -m venv "%VENV_DIR%"
  if not errorlevel 1 exit /b 0
)

where python >nul 2>nul
if not errorlevel 1 (
  echo Creating runtime with local Python...
  call python -m venv "%VENV_DIR%"
  if not errorlevel 1 exit /b 0
)

echo Python was not found. Creating a self-contained runtime...
call :ensure_uv
if errorlevel 1 exit /b 1
call "%UV_BIN%" venv "%VENV_DIR%" --python 3.12
if errorlevel 1 exit /b 1
exit /b 0

:ensure_uv
if exist "%UV_BIN%" exit /b 0
if not exist "%UV_DIR%" mkdir "%UV_DIR%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference = 'Stop'; $env:UV_UNMANAGED_INSTALL = '%UV_DIR%'; $env:UV_NO_MODIFY_PATH = '1'; irm https://astral.sh/uv/install.ps1 | iex"
if errorlevel 1 exit /b 1
if exist "%UV_BIN%" exit /b 0
exit /b 1

:runtime_failed
echo Runtime creation failed.
echo This launcher can use a local Python install or create a self-contained
echo runtime with uv when Python is not available.
echo.
exit /b 1

:install_failed
echo Dependency installation failed.
echo This launcher installs ccl_chromium_reader from GitHub source archives.
echo Network access to github.com and codeload.github.com is required.
echo.
exit /b 1
