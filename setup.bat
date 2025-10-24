@echo off
echo ========================================
echo Petit PrintBoard - Complete Setup
echo ========================================
echo.
echo This script will set up everything you need.
echo.

REM Check Python
echo [1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
python --version

REM Create virtual environment
echo.
echo [2/8] Creating virtual environment...
if not exist "venv\" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo.
echo [3/8] Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo.
echo [4/8] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Create directories
echo.
echo [5/8] Creating necessary directories...
if not exist "media\" mkdir media
if not exist "static\" mkdir static
if not exist "staticfiles\" mkdir staticfiles

REM Run migrations
echo.
echo [6/8] Setting up database...
python manage.py migrate

REM Collect static files
echo.
echo [7/8] Collecting static files...
python manage.py collectstatic --noinput

REM Create sample users
echo.
echo [8/8] Creating sample users...
echo.
echo Do you want to create sample users for testing? (y/n)
set /p CREATE_SAMPLES=
if /i "%CREATE_SAMPLES%"=="y" (
    python manage.py create_sample_users
) else (
    echo.
    echo Skipping sample users. You can create them later with:
    echo   python manage.py create_sample_users
    echo.
    echo Or create a superuser with:
    echo   python manage.py createsuperuser
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure Redis is running (redis-server.exe)
echo 2. Run: start_server.bat
echo 3. Open browser: http://localhost:8000
echo.
echo Sample login (if created):
echo   Secretary: secretary / secretary123
echo   Teachers: teacher1, teacher2, teacher3 / teacher123
echo.
pause
