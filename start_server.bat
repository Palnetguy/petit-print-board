@echo off
echo ========================================
echo Petit PrintBoard - Windows Deployment
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    exit /b 1
)

REM Activate virtual environment
echo [1/5] Activating virtual environment...
call venv\Scripts\activate

REM Check if dependencies are installed
echo [2/5] Checking dependencies...
pip show django >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
)

REM Run migrations
echo [3/5] Running database migrations...
python manage.py migrate

REM Collect static files
echo [4/5] Collecting static files...
python manage.py collectstatic --noinput

REM Start Redis (check if installed)
echo [5/5] Starting services...
echo.
echo Checking Redis...
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Redis is not running!
    echo Please start Redis server manually:
    echo   - Download from: https://github.com/microsoftarchive/redis/releases
    echo   - Or use WSL: sudo service redis-server start
    echo.
    pause
)

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    goto :done
)
:done
set IP=%IP:~1%

echo.
echo ========================================
echo PPB is starting...
echo ========================================
echo Local access:    http://localhost:8000
echo Network access:  http://%IP%:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the server
daphne -b 0.0.0.0 -p 8000 ppb_project.asgi:application
