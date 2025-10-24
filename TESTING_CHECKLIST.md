# 🧪 Petit PrintBoard - Testing Checklist

## Pre-Testing Setup

- [ ] Python 3.8+ installed
- [ ] Redis server installed and running
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database migrated (`python manage.py migrate`)
- [ ] Sample users created or superuser created

---

## 1️⃣ Installation Testing

### Automated Setup

- [ ] Run `setup.bat` (Windows) or `setup.sh` (Linux)
- [ ] No errors during dependency installation
- [ ] Database created successfully
- [ ] Static files collected
- [ ] Sample users created (if chosen)

### Manual Verification

- [ ] `db.sqlite3` file exists
- [ ] `media/` folder exists
- [ ] `staticfiles/` folder exists
- [ ] `venv/` folder exists

---

## 2️⃣ Server Startup Testing

### Start Services

- [ ] Redis starts: `redis-cli ping` returns "PONG"
- [ ] Server starts: Run `start_server.bat` or `start_server.sh`
- [ ] No errors in console
- [ ] Server accessible at http://localhost:8000

### Network Access

- [ ] Find local IP with `ipconfig` (Windows) or `hostname -I` (Linux)
- [ ] Access from another device: http://[YOUR_IP]:8000
- [ ] Page loads correctly on mobile device

---

## 3️⃣ Authentication Testing

### Login Page

- [ ] Navigate to http://localhost:8000
- [ ] Login page displays correctly
- [ ] Logo and branding visible
- [ ] Form fields present (username, password)

### Valid Login (Secretary)

- [ ] Enter: `secretary` / `secretary123`
- [ ] Click "Login"
- [ ] Redirects to secretary dashboard
- [ ] Welcome message shows: "Hello, Marie Mukamana"

### Valid Login (Teacher)

- [ ] Logout and login as: `teacher1` / `teacher123`
- [ ] Redirects to teacher dashboard
- [ ] Welcome message shows: "Hello, Jean Baptiste"

### Invalid Login

- [ ] Try wrong password
- [ ] Error message displays
- [ ] No redirect occurs
- [ ] Can retry login

### Logout

- [ ] Click "Logout" button
- [ ] Redirects to login page
- [ ] Cannot access dashboard without login

---

## 4️⃣ Teacher Dashboard Testing

### Page Load

- [ ] Login as teacher1
- [ ] Dashboard loads completely
- [ ] Statistics cards visible (Pending/Printed counts)
- [ ] Upload form visible
- [ ] Request history table visible

### File Upload - Valid Request

- [ ] Click file input, select a PDF file (< 50MB)
- [ ] Set deadline: Tomorrow's date and time
- [ ] Set copies: 5
- [ ] Add notes: "Test print request"
- [ ] Click "Submit Request"
- [ ] Success message appears
- [ ] Request appears in history table
- [ ] Pending count increases by 1

### File Upload - Validation

- [ ] Try uploading file > 50MB → Error message
- [ ] Try uploading .exe file → Error message
- [ ] Try setting copies > 50 → Form validation error
- [ ] Leave deadline empty → Validation error

### Request History Table

- [ ] Request shows correct filename
- [ ] Deadline displayed correctly
- [ ] Copies number correct
- [ ] Status shows "Pending" badge (orange)
- [ ] Download button visible and functional

### Real-Time Notifications (Test Later)

- [ ] Keep dashboard open
- [ ] Secretary marks request as printed
- [ ] Notification popup appears (top-right)
- [ ] Sound plays
- [ ] Page updates automatically (status changes to "Printed")

---

## 5️⃣ Secretary Dashboard Testing

### Page Load

- [ ] Login as secretary
- [ ] Dashboard loads completely
- [ ] Statistics cards visible
- [ ] Pending queue table visible
- [ ] Recently printed table visible (if any printed requests)

### Pending Queue

- [ ] All pending requests visible
- [ ] Sorted by deadline (earliest first)
- [ ] Teacher names displayed correctly
- [ ] File names shown
- [ ] Deadline dates visible
- [ ] Copy counts visible
- [ ] Notes displayed (if any)

### Urgent Highlighting

- [ ] Create request with deadline < 2 hours from now
- [ ] Request row highlighted in red
- [ ] "URGENT" badge visible and pulsing

### Download File

- [ ] Click download button (blue icon)
- [ ] File downloads successfully
- [ ] Opens correctly (PDF viewer, Word, etc.)
- [ ] File content is correct

### Mark as Printed

- [ ] Click green checkmark button
- [ ] Success message appears
- [ ] Request disappears from pending queue
- [ ] Appears in "Recently Printed" table
- [ ] Pending count decreases by 1
- [ ] Printed count increases by 1
- [ ] Printed timestamp shown

### Real-Time Notifications

- [ ] Keep secretary dashboard open
- [ ] Login as teacher in another browser/tab
- [ ] Submit new print request
- [ ] Notification popup appears on secretary screen
- [ ] Sound plays
- [ ] Notification shows: teacher name and filename
- [ ] Page updates automatically (new request appears)

---

## 6️⃣ WebSocket Testing

### Teacher WebSocket

- [ ] Open browser console (F12)
- [ ] Login as teacher
- [ ] Look for WebSocket connection: `ws://localhost:8000/ws/notifications/teacher/[ID]/`
- [ ] No connection errors
- [ ] Secretary marks request as printed
- [ ] Message received in console
- [ ] Notification displays

### Secretary WebSocket

- [ ] Open browser console (F12)
- [ ] Login as secretary
- [ ] Look for WebSocket connection: `ws://localhost:8000/ws/notifications/secretary/`
- [ ] No connection errors
- [ ] Teacher submits request
- [ ] Message received in console
- [ ] Notification displays

### WebSocket Reconnection

- [ ] Keep dashboard open
- [ ] Restart Redis server
- [ ] WebSocket reconnects automatically within 5 seconds
- [ ] Or page reloads automatically

---

## 7️⃣ Responsive Design Testing

### Desktop (1920x1080)

- [ ] All elements visible
- [ ] Two columns for stat cards
- [ ] Tables display fully
- [ ] No horizontal scrolling

### Tablet (768px width)

- [ ] Layout adapts smoothly
- [ ] Cards stack vertically
- [ ] Tables remain readable
- [ ] Navigation responsive

### Mobile (375px width)

- [ ] Login page centered
- [ ] Dashboard cards stacked
- [ ] Tables scroll horizontally if needed
- [ ] Buttons appropriately sized
- [ ] Touch targets > 44px
- [ ] Notifications fit screen

### Different Browsers

- [ ] Chrome: All features work
- [ ] Firefox: All features work
- [ ] Edge: All features work
- [ ] Safari (if available): All features work

---

## 8️⃣ File Management Testing

### Supported File Types

- [ ] Upload .pdf file → Success
- [ ] Upload .doc file → Success
- [ ] Upload .docx file → Success
- [ ] Upload .txt file → Success

### Unsupported File Types

- [ ] Upload .jpg file → Error
- [ ] Upload .zip file → Error
- [ ] Upload .exe file → Error

### File Size Limits

- [ ] Upload 1MB file → Success
- [ ] Upload 25MB file → Success
- [ ] Upload 60MB file → Error message

### File Storage

- [ ] Check `media/uploads/` folder
- [ ] Files organized by date (YYYY/MM/DD)
- [ ] Filenames preserved
- [ ] No file corruption

---

## 9️⃣ Security Testing

### Authorization

- [ ] Teacher cannot access `/admin/`
- [ ] Teacher cannot mark others' requests as printed
- [ ] Teacher can only download own files
- [ ] Secretary can download all files
- [ ] Secretary can mark any request as printed
- [ ] Non-logged-in users redirect to login

### CSRF Protection

- [ ] Forms include CSRF token
- [ ] Requests without token fail
- [ ] Token refreshes on new session

### File Access

- [ ] Cannot access files directly via URL without login
- [ ] File paths not guessable
- [ ] No directory listing in media folder

---

## 🔟 Performance Testing

### Load Time

- [ ] Login page loads < 2 seconds
- [ ] Dashboard loads < 2 seconds
- [ ] File upload completes < 10 seconds (10MB file)

### Memory Usage

- [ ] Server uses < 150MB RAM
- [ ] Redis uses < 50MB RAM
- [ ] No memory leaks after 1 hour

### Concurrent Users

- [ ] 5 teachers logged in simultaneously
- [ ] 3 file uploads at same time
- [ ] All notifications delivered
- [ ] No server crashes

### Database Performance

- [ ] 100 print requests in database
- [ ] Dashboard still loads quickly
- [ ] Queries complete < 1 second

---

## 1️⃣1️⃣ Production Readiness

### Configuration

- [ ] SECRET_KEY changed from default
- [ ] DEBUG set to False for production
- [ ] ALLOWED_HOSTS configured with server IP
- [ ] Redis configured correctly
- [ ] Media folder has write permissions

### Deployment

- [ ] Windows service installed (if Windows)
- [ ] Systemd service installed (if Linux)
- [ ] Auto-starts on boot
- [ ] Auto-restarts on crash
- [ ] Firewall configured (port 8000 open)

### Backup

- [ ] Database backup works: `python manage.py dumpdata > backup.json`
- [ ] Media files can be copied
- [ ] Restore process tested

### Monitoring

- [ ] Logs accessible
- [ ] Redis monitoring: `redis-cli monitor`
- [ ] Error tracking functional

---

## 1️⃣2️⃣ User Acceptance Testing

### Teacher Workflow

- [ ] Teacher can login easily
- [ ] Upload process intuitive
- [ ] Status updates clear
- [ ] Notifications helpful
- [ ] History easy to navigate

### Secretary Workflow

- [ ] Queue organization clear
- [ ] Urgent items stand out
- [ ] Download process smooth
- [ ] Mark printed is quick
- [ ] Notifications not intrusive

### Overall Experience

- [ ] UI is attractive
- [ ] Navigation is intuitive
- [ ] No confusing elements
- [ ] Errors are user-friendly
- [ ] Fast and responsive

---

## ✅ Final Checklist

Before deploying to production:

- [ ] All tests passed
- [ ] Documentation complete
- [ ] Users trained (5-minute guide)
- [ ] Backup procedures established
- [ ] Support contact defined
- [ ] Network configuration verified
- [ ] Server has static IP
- [ ] Auto-start configured
- [ ] Monitoring in place

---

## 🎉 Testing Complete!

**Date Tested**: ******\_******

**Tested By**: ******\_******

**Result**: ⭐ PASS / ❌ FAIL

**Notes**:

```
_______________________________________
_______________________________________
_______________________________________
```

---

**Petit PrintBoard is ready for deployment! 🚀**
