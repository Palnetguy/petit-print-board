# Petit PrintBoard - Quick Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Python

- Download Python 3.8+ from https://python.org
- **Important**: Check "Add Python to PATH" during installation

### Step 2: Install Redis

**Windows:**

- Download: https://github.com/microsoftarchive/redis/releases
- Extract and run `redis-server.exe`

**Linux:**

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

### Step 3: Setup Project

```bash
# Navigate to project folder
cd ppb

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin account (Secretary)
python manage.py createsuperuser
```

### Step 4: Create Teacher Accounts

```bash
# Start server temporarily
python manage.py runserver

# Open browser: http://localhost:8000/admin/
# Login with superuser credentials
# Click "Users" → "Add user"
# Create teacher accounts (uncheck "Staff status")
# For secretary accounts, check "Staff status"
```

### Step 5: Start Application

**Easy Way (Recommended):**

```bash
# Windows:
start_server.bat

# Linux:
chmod +x start_server.sh
./start_server.sh
```

**Manual Way:**

```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Django
python manage.py runserver 0.0.0.0:8000
```

### Step 6: Access the System

- **From host computer**: http://localhost:8000
- **From other devices**: http://[YOUR_IP]:8000
- Example: http://192.168.1.100:8000

## 👥 Default Login

**Secretary (Admin):**

- Username: (your superuser username)
- Password: (your superuser password)

**Teachers:**

- Created via admin panel
- Username/password set during creation

## 📋 Daily Operations

**For Teachers:**

1. Login → Click "Submit New Print Request"
2. Upload file → Set deadline → Enter copies
3. Click "Submit Request"
4. Wait for notification when printed

**For Secretary:**

1. Login → See pending requests
2. Click download icon → Print file
3. Click green checkmark → Mark as printed
4. Teacher gets automatic notification

## 🔧 Troubleshooting

**Problem:** "Port 8000 already in use"

```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F

# Linux:
sudo lsof -t -i:8000 | xargs kill -9
```

**Problem:** "Redis connection failed"

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not, start Redis:
# Windows: redis-server.exe
# Linux: sudo systemctl start redis
```

**Problem:** "File upload failed"

- Check file size < 50MB
- Verify file type: PDF, DOC, DOCX, TXT only
- Ensure media/ folder exists and is writable

## 📱 Network Setup

**Find your computer's IP address:**

Windows:

```bash
ipconfig
# Look for "IPv4 Address"
```

Linux:

```bash
hostname -I
```

**Share with teachers:**

- Tell teachers to connect to school WiFi
- Give them the URL: http://[YOUR_IP]:8000
- Example: http://192.168.1.100:8000

## 🎯 Best Practices

1. **Backup database weekly:**

   ```bash
   python manage.py dumpdata > backup_$(date +%Y%m%d).json
   ```

2. **Keep server running:**

   - Use deployment scripts for auto-restart
   - Set up as Windows Service or Linux Systemd

3. **Regular maintenance:**
   - Clear old files monthly
   - Update Python packages quarterly

## 📞 Need Help?

1. Check logs: Look at terminal output
2. Test Redis: `redis-cli ping`
3. Check migrations: `python manage.py showmigrations`
4. Verify firewall allows port 8000

---

**System is now ready! Teachers can start submitting print requests.**
