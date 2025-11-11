# 🧩 XMP Filter Storage

**XMP Filter Storage** is a secure, web-based application built for **freelance photo editors** to efficiently manage, store, and track **XMP files**.
Developed with **Django**, **Tailwind CSS**, and **DaisyUI**, the system features **role-based access**, **Clockify integration**, and an **Editors Log** for attendance tracking — all secured with **GPG-encrypted environment variables**.

---

## 🚀 Features

- **Admin Dashboard** – Manage users, assign roles, and control system settings.
- **Editors Log (Attendance Tracking)** – Record login sessions and daily editor activity.
- **Clockify Integration** – Sync workspace, project, and time entries from the Clockify API.
- **Role-Based Access Control (RBAC)** – Assign permissions for Admin, Senior, and Junior Editors.
- **Encrypted Configuration** – Protect credentials and environment data using `env.gpg`.
- **Secure XMP File Management** – Upload, view, and store XMP metadata securely.
- **Modern, Responsive Interface** – Built with **Tailwind CSS** and **DaisyUI** for clean UX/UI.
- **Scalable Architecture** – Ready for deployment in production with PostgreSQL and API support.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django (Python Framework) |
| **Frontend** | Tailwind CSS, DaisyUI |
| **Database** | SQLite (Development) → PostgreSQL (Recommended for Production) |
| **Authentication** | Django’s Built-in Authentication System |
| **Security** | GPG-Encrypted Environment Variables (`env.gpg`) |
| **Integrations** | Clockify API for workspace and time tracking |

---

## 📦 Requirements

Below are the main dependencies used in this project:

```txt
Django>=5.2.5
python-dotenv>=1.0.0
django-crispy-forms>=2.0
crispy-tailwind>=0.5.0
Pillow>=10.0.0  # For image handling
django-widget-tweaks>=1.4.12
djangorestframework>=3.16.1
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## 🌍 Getting Started

### ✅ Prerequisites

Install the following on your system:
- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (for Tailwind CSS)
- [Git](https://git-scm.com/) (for version control)
- [GnuPG (GPG)](https://gnupg.org/) (to decrypt `.env.gpg`)

---

### ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/xmp-filter-storage.git
cd xmp-filter-storage

# Decrypt environment variables (requires GPG key)
gpg --decrypt env.gpg > .env

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # (use venv\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install
```

---

### 🧠 Run the Application

```bash
# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Then open your browser and visit:
👉 **http://127.0.0.1:8000/**

---

## 🔐 User Roles

| Role | Description |
|------|--------------|
| **Admin** | Full access to manage users, roles, attendance, and integrations. |
| **Senior Editor** | Can upload, edit, and manage XMP files; access attendance of all Senior Editor. |
| **Junior Editor** | Can view and download assigned files; access attendance of all Junior Editor . |

---

## ⏱️ Integrations & Modules

### **Editors Log (Attendance System)**
- Tracks editor attendance and login activity.
- Displays daily summaries for monitoring productivity.

### **Clockify Integration**
- Connects directly to the **Clockify API**.
- Syncs workspace, project, and user time entry data.
- Stores records locally for analytics and reports.

---

## 🔒 Security

- Sensitive credentials are encrypted in **`.env.gpg`**.
- Only authorized users with the correct **GPG key** can decrypt environment variables.
- Adheres to Django and GPG best practices for secure configuration management.

---

## 📊 Future Enhancements

- Cloud storage integration (AWS S3 or Google Cloud Storage)
- Activity analytics and reporting dashboard
- File versioning and collaboration tracking
- Dark mode and advanced accessibility support

