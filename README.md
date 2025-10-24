# Petit PrintBoard (PPB)

**A Local Network-Based Print Request System for Schools**

## 🎯 Overview

Petit PrintBoard is a lightweight, real-time web application that manages print requests between teachers and secretary staff. Built for schools with limited hardware resources, it eliminates the need for WhatsApp/internet dependency by running entirely on the local network.

## ✨ Features

- **Real-time Notifications**: Instant WebSocket-based alerts for new requests and completed prints
- **Teacher Dashboard**: Upload files, track requests, view history
- **Secretary Dashboard**: Organized print queue with deadline sorting and urgent highlighting
- **Responsive Design**: Works on phones, tablets, and desktops
- **Lightweight**: Runs smoothly on 2GB RAM hardware
- **Offline-Ready**: 100% local network operation (no internet required)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Redis server
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone or extract the project**

   ```bash
   cd ppb
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Redis** (if not already installed)

   **Windows:**

   - Download Redis from: https://github.com/microsoftarchive/redis/releases
   - Or use WSL: `sudo apt install redis-server`

   **Linux:**

   ```bash
   sudo apt update
   sudo apt install redis-server
   sudo systemctl start redis
   ```

5. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (Secretary account)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Create teacher accounts via Django admin**

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

   - Visit: http://localhost:8000/admin/
   - Login with superuser credentials
   - Go to Users → Add user
   - Create teacher accounts (leave "Staff status" unchecked for teachers)
   - Secretary accounts should have "Staff status" checked

8. **Start Redis server** (in a separate terminal)

   ```bash
   # Windows (if using native Redis)
   redis-server

   # Linux
   sudo systemctl start redis
   # or
   redis-server
   ```

9. **Start the development server**

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

10. **Access the application**
    - From the host machine: http://localhost:8000
    - From other devices on the network: http://[HOST_IP]:8000
    - Example: http://192.168.1.100:8000

## 👥 User Roles

### Teachers (Regular Users)

- Upload print requests with files
- Set deadlines and number of copies
- Add optional notes
- View request history
- Receive notifications when prints are completed
- **Staff status**: NO

### Secretary (Staff Users)

- View organized print queue (sorted by deadline)
- Receive instant notifications for new requests
- Download and print files
- Mark requests as printed
- View recently printed history
- **Staff status**: YES

## 📁 Project Structure

```
ppb/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── ppb_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── prints/
│   ├── __init__.py
│   ├── models.py          # PrintRequest model
│   ├── views.py           # Dashboard and action views
│   ├── forms.py           # Print request form
│   ├── urls.py            # URL routing
│   ├── consumers.py       # WebSocket consumers
│   ├── routing.py         # WebSocket routing
│   └── admin.py           # Django admin config
├── templates/
│   ├── base.html          # Base template
│   └── prints/
│       ├── login.html
│       ├── teacher_dashboard.html
│       └── secretary_dashboard.html
├── media/                 # Uploaded files
└── static/                # Static files (if any)
```

## 🔧 Configuration

### Network Setup

1. **Set a static IP** on the host machine (recommended)
   - Example: 192.168.1.100
2. **Configure firewall** to allow port 8000 on local network only

   **Windows Firewall:**

   ```powershell
   New-NetFirewallRule -DisplayName "PPB Print System" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

   **Linux (ufw):**

   ```bash
   sudo ufw allow 8000/tcp
   ```

3. **Update ALLOWED_HOSTS** in `ppb_project/settings.py` (optional)
   ```python
   ALLOWED_HOSTS = ['192.168.1.100', 'localhost', '127.0.0.1']
   ```

### Production Deployment

For production use with Gunicorn (recommended for better performance):

1. **Install Gunicorn** (already in requirements.txt)

2. **Run with Daphne** (for WebSocket support):

   ```bash
   daphne -b 0.0.0.0 -p 8000 ppb_project.asgi:application
   ```

3. **Or use the deployment script** (see below)

## 🖥️ Deployment Scripts

### Windows Deployment (Using NSSM)

1. **Download NSSM**: https://nssm.cc/download

2. **Create deployment script** `deploy_windows.bat`:

   ```batch
   @echo off
   echo Starting Petit PrintBoard...

   REM Start Redis
   start redis-server

   REM Wait for Redis
   timeout /t 3

   REM Start Daphne server
   cd /d %~dp0
   call venv\Scripts\activate
   daphne -b 0.0.0.0 -p 8000 ppb_project.asgi:application
   ```

3. **Install as Windows Service with NSSM**:
   ```bash
   nssm install PPB "C:\path\to\ppb\venv\Scripts\daphne.exe"
   nssm set PPB AppParameters "-b 0.0.0.0 -p 8000 ppb_project.asgi:application"
   nssm set PPB AppDirectory "C:\path\to\ppb"
   nssm start PPB
   ```

### Linux Deployment (Using Systemd)

Create `/etc/systemd/system/ppb.service`:

```ini
[Unit]
Description=Petit PrintBoard Django App
After=network.target redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/ppb
Environment="PATH=/opt/ppb/venv/bin"
ExecStart=/opt/ppb/venv/bin/daphne -b 0.0.0.0 -p 8000 ppb_project.asgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ppb
sudo systemctl start ppb
sudo systemctl status ppb
```

## 🔐 Security Considerations

1. **Change SECRET_KEY** in `settings.py` for production
2. **Set DEBUG = False** in production
3. **Use strong passwords** for all user accounts
4. **Restrict network access** to local LAN only
5. **Regular backups** of `db.sqlite3` and `media/` folder

## 📊 Maintenance

### Database Backup

```bash
# Backup
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Restore
python manage.py loaddata backup_20251024.json
```

### Clear Old Files (Optional)

Create a management command to delete files older than 30 days:

```bash
python manage.py shell
>>> from prints.models import PrintRequest
>>> from django.utils import timezone
>>> from datetime import timedelta
>>> old_date = timezone.now() - timedelta(days=30)
>>> old_requests = PrintRequest.objects.filter(status='printed', printed_at__lt=old_date)
>>> for req in old_requests:
...     req.file.delete()
...     req.delete()
```

## 🐛 Troubleshooting

### WebSocket Connection Issues

- Ensure Redis is running: `redis-cli ping` (should return "PONG")
- Check firewall allows port 6379 (Redis)
- Verify WebSocket URL in browser console

### File Upload Errors

- Check `media/` folder permissions (needs write access)
- Verify file size < 50MB
- Ensure file extension is allowed (.pdf, .doc, .docx, .txt)

### Server Won't Start

- Check if port 8000 is already in use
- Verify Python virtual environment is activated
- Run `python manage.py check` for configuration errors

## 📞 Support

For issues or questions:

1. Check Django logs: `python manage.py runserver`
2. Check Redis logs: `redis-cli monitor`
3. Review browser console for JavaScript errors

## 📄 License

This project is provided as-is for educational and internal use at Petit Seminaire St Leon Kabgayi.

## 🎓 Training

**For Teachers (5 minutes):**

1. Connect to school WiFi
2. Open browser → http://192.168.1.100:8000
3. Login with your credentials
4. Click upload → Select file → Set deadline → Submit
5. Check dashboard for status

**For Secretary (5 minutes):**

1. Login at startup
2. Listen for notification sounds
3. Click notification → Download → Print
4. Click green checkmark → Mark as printed

---

**Built with ❤️ for Petit Seminaire St Leon Kabgayi**
