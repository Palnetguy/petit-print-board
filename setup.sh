#!/bin/bash

echo "========================================"
echo "Petit PrintBoard - Complete Setup"
echo "========================================"
echo
echo "This script will set up everything you need."
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}[1/8]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed!"
    echo "Please install Python 3.8+ with: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi
python3 --version

# Create virtual environment
echo
echo -e "${BLUE}[2/8]${NC} Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo
echo -e "${BLUE}[3/8]${NC} Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo
echo -e "${BLUE}[4/8]${NC} Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
echo
echo -e "${BLUE}[5/8]${NC} Creating necessary directories..."
mkdir -p media static staticfiles

# Run migrations
echo
echo -e "${BLUE}[6/8]${NC} Setting up database..."
python manage.py migrate

# Collect static files
echo
echo -e "${BLUE}[7/8]${NC} Collecting static files..."
python manage.py collectstatic --noinput

# Create sample users
echo
echo -e "${BLUE}[8/8]${NC} Creating sample users..."
echo
read -p "Do you want to create sample users for testing? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py create_sample_users
else
    echo
    echo "Skipping sample users. You can create them later with:"
    echo "  python manage.py create_sample_users"
    echo
    echo "Or create a superuser with:"
    echo "  python manage.py createsuperuser"
fi

# Make start script executable
chmod +x start_server.sh

echo
echo "========================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================"
echo
echo "Next steps:"
echo "1. Make sure Redis is running: sudo systemctl start redis"
echo "2. Run: ./start_server.sh"
echo "3. Open browser: http://localhost:8000"
echo
echo "Sample login (if created):"
echo "  Secretary: secretary / secretary123"
echo "  Teachers: teacher1, teacher2, teacher3 / teacher123"
echo
