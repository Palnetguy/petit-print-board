#!/bin/bash

echo "========================================"
echo "Petit PrintBoard - Linux Deployment"
echo "========================================"
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}[ERROR]${NC} Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "[1/6] Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "[2/6] Checking dependencies..."
if ! pip show django &> /dev/null; then
    echo -e "${YELLOW}[INFO]${NC} Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if Redis is running
echo "[3/6] Checking Redis..."
if ! redis-cli ping &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} Redis is not running!"
    echo "Starting Redis..."
    sudo systemctl start redis 2>/dev/null || redis-server --daemonize yes
    sleep 2
fi

# Run migrations
echo "[4/6] Running database migrations..."
python manage.py migrate

# Collect static files
echo "[5/6] Collecting static files..."
python manage.py collectstatic --noinput

# Get local IP address
IP=$(hostname -I | awk '{print $1}')

echo
echo "========================================"
echo "PPB is starting..."
echo "========================================"
echo -e "Local access:    ${GREEN}http://localhost:8000${NC}"
echo -e "Network access:  ${GREEN}http://$IP:8000${NC}"
echo
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo

# Start the server
echo "[6/6] Starting Daphne server..."
daphne -b 0.0.0.0 -p 8000 ppb_project.asgi:application
