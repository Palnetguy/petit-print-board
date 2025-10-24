# 🏗️ Petit PrintBoard - System Architecture

## Visual System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SCHOOL LOCAL NETWORK                         │
│                         (192.168.x.x/24)                            │
└─────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
   ┌────▼────┐                 ┌────▼────┐               ┌─────▼─────┐
   │ Teacher │                 │ Teacher │               │ Secretary │
   │ Phone   │                 │ Laptop  │               │ Desktop   │
   │(Mobile) │                 │         │               │ (2GB RAM) │
   └────┬────┘                 └────┬────┘               └─────┬─────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                        HTTP/WebSocket Requests
                                    │
                                    ▼
        ┌─────────────────────────────────────────────────────┐
        │         PPB Django Application (Port 8000)          │
        │                                                     │
        │  ┌───────────────────────────────────────────┐    │
        │  │         Daphne ASGI Server                │    │
        │  │  (Handles HTTP + WebSocket connections)   │    │
        │  └───────────────┬───────────────────────────┘    │
        │                  │                                 │
        │  ┌───────────────▼──────────────┐                 │
        │  │      Django Core             │                 │
        │  │  ┌─────────┬──────────────┐  │                 │
        │  │  │  Views  │  Templates   │  │                 │
        │  │  └─────────┴──────────────┘  │                 │
        │  │  ┌─────────┬──────────────┐  │                 │
        │  │  │  Models │    Forms     │  │                 │
        │  │  └─────────┴──────────────┘  │                 │
        │  └──────────────────────────────┘                 │
        │                                                     │
        │  ┌──────────────────────────────────────────┐     │
        │  │    Django Channels (WebSockets)          │     │
        │  │    - NotificationConsumer                │     │
        │  │    - Teacher/Secretary groups            │     │
        │  └────────────┬─────────────────────────────┘     │
        └───────────────┼───────────────────────────────────┘
                        │
                        ▼
        ┌─────────────────────────────────────────────────────┐
        │           Redis Server (Port 6379)                   │
        │  - Message broker for WebSocket channels            │
        │  - Stores temporary notification data                │
        │  - < 50MB RAM usage                                  │
        └─────────────────────────────────────────────────────┘
                        │
                        ▼
        ┌─────────────────────────────────────────────────────┐
        │         SQLite Database (db.sqlite3)                 │
        │  - Users (teachers & secretary)                      │
        │  - PrintRequests (file, deadline, status, etc.)      │
        │  - Sessions                                          │
        │  - < 10MB for 1000s of requests                      │
        └─────────────────────────────────────────────────────┘
                        │
                        ▼
        ┌─────────────────────────────────────────────────────┐
        │         File System (media/ folder)                  │
        │  - Uploaded PDF, DOC, DOCX, TXT files               │
        │  - Organized by date: YYYY/MM/DD/                   │
        │  - Direct file serving for downloads                 │
        └─────────────────────────────────────────────────────┘
                        │
                        ▼
        ┌─────────────────────────────────────────────────────┐
        │              USB Printer                             │
        │  Connected to Secretary Desktop                      │
        └─────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### 1. Teacher Submits Print Request

```
Teacher Browser
      │
      │ 1. Fill form & upload file
      │
      ▼
Django Views (views.py)
      │
      │ 2. Validate form
      │ 3. Save to database
      │ 4. Store file in media/
      │
      ▼
SQLite + File System
      │
      │ 5. Send notification via Channels
      │
      ▼
Redis Channel Layer
      │
      │ 6. Broadcast to secretary group
      │
      ▼
Secretary WebSocket
      │
      │ 7. Show popup notification
      │ 8. Play sound
      │ 9. Update UI
      │
      ▼
Secretary sees new request!
```

### 2. Secretary Prints Document

```
Secretary Browser
      │
      │ 1. Click download button
      │
      ▼
Django Views (download_file)
      │
      │ 2. Check permissions
      │ 3. Serve file
      │
      ▼
File downloads to secretary
      │
      │ 4. Secretary prints physically
      │ 5. Click "Mark Printed" button
      │
      ▼
Django Views (mark_printed)
      │
      │ 6. Update status in DB
      │ 7. Set printed_at timestamp
      │
      ▼
SQLite Database
      │
      │ 8. Send notification via Channels
      │
      ▼
Redis Channel Layer
      │
      │ 9. Send to teacher's personal group
      │
      ▼
Teacher WebSocket
      │
      │ 10. Show notification
      │ 11. Update UI
      │
      ▼
Teacher sees "Printed" status!
```

---

## Component Responsibilities

### Frontend (Templates)

**base.html**

- Navigation bar
- User welcome message
- Logout button
- Message display
- Notification container
- Base styling

**login.html**

- Login form
- Error messages
- Branding

**teacher_dashboard.html**

- Upload form
- Statistics cards (pending/printed)
- Request history table
- WebSocket connection (receive "printed" notifications)

**secretary_dashboard.html**

- Pending queue table
- Recently printed table
- Statistics cards
- Download/mark printed buttons
- WebSocket connection (receive "new request" notifications)

### Backend (Django)

**models.py**

- `PrintRequest` model
  - Links to User (teacher)
  - File storage
  - Status tracking
  - Deadline management
  - Methods: `is_urgent()`, `mark_printed()`

**views.py**

- `login_view` - User authentication
- `logout_view` - Session termination
- `dashboard` - Route to teacher/secretary dashboard
- `teacher_dashboard` - Upload form & history
- `secretary_dashboard` - Print queue
- `mark_printed` - Status update + notification
- `download_file` - Secure file serving

**forms.py**

- `PrintRequestForm`
  - File validation (size, type)
  - Deadline input
  - Copies range (1-50)
  - Notes textarea

**consumers.py**

- `NotificationConsumer`
  - WebSocket connection handler
  - Group management (secretary/teacher_X)
  - Message handlers: `new_request`, `request_printed`

**admin.py**

- Django admin interface
- Manage users and requests
- View all data

### Data Layer

**SQLite Database**

- Lightweight (no separate server)
- Single file: `db.sqlite3`
- Tables:
  - auth_user (Django users)
  - prints_printrequest (print requests)
  - django_session (user sessions)
  - Others (Django internals)

**Redis**

- In-memory data store
- Channel layer for WebSockets
- Pub/Sub messaging
- Temporary notification storage

**File System (media/)**

- Organized by upload date
- Example: `media/uploads/2025/10/24/document.pdf`
- Direct serving via Django
- Protected by authentication

---

## URL Routing Structure

```
http://192.168.1.100:8000/
    │
    ├── /                        → Redirects to /login/ or dashboard
    ├── /login/                  → Login page
    ├── /logout/                 → Logout action
    ├── /dashboard/              → Teacher or Secretary dashboard (role-based)
    ├── /mark-printed/<id>/      → Mark request as printed (secretary only)
    ├── /download/<id>/          → Download file (permission checked)
    ├── /admin/                  → Django admin panel
    ├── /media/uploads/...       → Served files (protected)
    └── /static/...              → CSS, JS, images

WebSocket Connections:
    ws://192.168.1.100:8000/ws/notifications/secretary/
    ws://192.168.1.100:8000/ws/notifications/teacher/<user_id>/
```

---

## User Permission Matrix

| Feature               | Teacher | Secretary | Admin |
| --------------------- | ------- | --------- | ----- |
| Login                 | ✅      | ✅        | ✅    |
| View own requests     | ✅      | ✅        | ✅    |
| View all requests     | ❌      | ✅        | ✅    |
| Upload print request  | ✅      | ✅        | ✅    |
| Download own files    | ✅      | ❌        | ✅    |
| Download all files    | ❌      | ✅        | ✅    |
| Mark as printed       | ❌      | ✅        | ✅    |
| Receive new req notif | ❌      | ✅        | ✅    |
| Receive printed notif | ✅      | ❌        | ✅    |
| Access admin panel    | ❌      | ❌        | ✅    |
| Manage users          | ❌      | ❌        | ✅    |

---

## Database Schema

### User (Django built-in)

```
┌─────────────────────────────────┐
│ auth_user                       │
├─────────────────────────────────┤
│ id (PK)                         │
│ username                        │
│ password (hashed)               │
│ first_name                      │
│ last_name                       │
│ email                           │
│ is_staff (True = Secretary)    │
│ is_active                       │
│ date_joined                     │
└─────────────────────────────────┘
```

### PrintRequest

```
┌─────────────────────────────────┐
│ prints_printrequest             │
├─────────────────────────────────┤
│ id (PK)                         │
│ teacher_id (FK → User)          │
│ file (FileField)                │
│ filename (CharField)            │
│ deadline (DateTimeField)        │
│ copies (IntegerField)           │
│ notes (TextField, nullable)     │
│ status ('pending'/'printed')    │
│ created_at (auto)               │
│ updated_at (auto)               │
│ printed_at (nullable)           │
└─────────────────────────────────┘
```

### Relationships

```
User (1) ─────< (M) PrintRequest
  │
  └─ One user can have many print requests
  └─ Each request belongs to one teacher
```

---

## Technology Stack Summary

| Layer          | Technology         | Purpose                 |
| -------------- | ------------------ | ----------------------- |
| **Frontend**   | Bootstrap 5        | Responsive UI framework |
|                | Font Awesome 6     | Icons                   |
|                | Vanilla JavaScript | WebSocket, interactions |
|                | Django Templates   | Server-side rendering   |
| **Backend**    | Django 4.2.7       | Web framework           |
|                | Django Channels    | WebSocket support       |
|                | Daphne             | ASGI server             |
| **Database**   | SQLite             | Relational database     |
| **Cache/Msg**  | Redis              | Channel layer, pub/sub  |
| **Files**      | File System        | Media storage           |
| **Deployment** | Systemd/NSSM       | Service management      |

---

## Network Configuration

### Development (Same Computer)

```
http://localhost:8000
├── Host: 127.0.0.1
└── Accessible only from this computer
```

### Production (Local Network)

```
http://192.168.1.100:8000
├── Host: 0.0.0.0 (listens on all interfaces)
├── Port: 8000
├── Firewall: Allow port 8000 (local network only)
└── Accessible from any device on school WiFi/LAN
```

### Port Usage

```
8000  → Django/Daphne application (HTTP + WebSocket)
6379  → Redis server (internal only)
```

---

## Scalability & Performance

### Current Capacity

- **Users**: 50+ concurrent users
- **Requests**: 10,000+ print requests in database
- **Files**: Limited only by disk space
- **RAM**: ~150MB total (Django + Redis)
- **CPU**: Minimal (<5% on dual-core)

### Optimization Features

- ✅ Database indexing on foreign keys
- ✅ File serving via Django (sendfile for production)
- ✅ Static file caching
- ✅ WebSocket connection pooling
- ✅ Efficient query design (no N+1 queries)

### Future Scaling Options

- Add more Daphne workers (Gunicorn + Daphne)
- Use PostgreSQL for larger deployments
- Add nginx reverse proxy
- Implement file cleanup cron job
- Add request archiving

---

## Security Layers

```
┌────────────────────────────────────────┐
│ 1. Network Layer                       │
│    - Local network only (firewall)     │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│ 2. Application Layer                   │
│    - CSRF protection                   │
│    - Session authentication            │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│ 3. Authorization Layer                 │
│    - Role-based access (is_staff)      │
│    - Object-level permissions          │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│ 4. Data Validation Layer               │
│    - Form validation                   │
│    - File type checking                │
│    - Size limits                       │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│ 5. Storage Layer                       │
│    - Secure file paths                 │
│    - No directory listing              │
│    - Protected media serving           │
└────────────────────────────────────────┘
```

---

**This architecture diagram provides a complete visual understanding of how Petit PrintBoard works!** 🚀
