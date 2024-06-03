@echo off

setlocal
set "python_exe=python"

REM Check if Python executable exists
where %python_exe% >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed on this device.
    goto :eof
)

REM Get Python version
for /f "tokens=*" %%v in ('%python_exe% -V 2^>^&1') do set "python_version=%%v"
echo Python Version: %python_version%

endlocal