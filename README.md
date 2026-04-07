# 🏥 Innovation Management Platform — منصة إدارة الابتكار

> **Seha Virtual Hospital** — An internal innovation management platform for tracking challenges, initiatives, and workshops across hospital departments.

---

## 📋 Table of Contents

- [Overview](#overview)
- Features
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Running the Project](#running-the-project)
- [Available Pages](#available-pages)
- [Project Structure](#project-structure)

---

## 🔍 Overview

This is a **Django-based web application** that serves as an Innovation Management Platform for Seha Virtual Hospital (مستشفى الصحة الافتراضي). It allows departments to submit challenges and initiatives, track them on an interactive workshop board, and view analytics through a dashboard.

---

## ✨ Features

| Feature                       | Description                                                        |
| ----------------------------- | ------------------------------------------------------------------ |
| **Dashboard**           | Analytics dashboard with charts showing submissions per department |
| **Submissions**         | View all submitted challenges and initiatives                      |
| **Workshop Board**      | Kanban-style board with Define → Ideate → Prototype stages       |
| **Excel Export**        | Export all submissions to an Excel (.xlsx) file                    |
| **Power BI Page**       | Dedicated page for Power BI report embedding                       |
| **Department Tracking** | Track submissions across 14 hospital departments                   |

---

## 🛠 Tech Stack

- **Backend:** Python 3.x, Django 6.0
- **Database:** SQLite3
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Export:** openpyxl (Excel generation)
- **Data:** pandas, numpy

---

## 📦 Prerequisites

Before you begin, make sure you have the following installed on your system:

- **Python 3.10+** — [Download Python](https://www.python.org/downloads/)
- **pip** — comes bundled with Python
- **Git** *(optional)* — for cloning the repository

To verify Python is installed, open a terminal and run:

```bash
python --version
```

---

## 🚀 Getting Started

### 1. Clone or Download the Project

```bash
# If using Git:
git clone <repository-url>
cd innovation-platform

# Or simply extract the project folder and navigate into it.
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser *(Optional — for Admin panel access)*

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

---

## ▶️ Running the Project

Start the Django development server:

```bash
python manage.py runserver
```

The server will start at:

```
http://127.0.0.1:8000/
```

Open your browser and navigate to any of the available pages listed below.

---

## 🗂 Available Pages

| URL               | Page           | Description                                              |
| ----------------- | -------------- | -------------------------------------------------------- |
| `/dashboard/`   | Dashboard      | Main analytics dashboard with department charts          |
| `/submissions/` | Submissions    | List of all challenges and initiatives                   |
| `/board/`       | Workshop Board | Interactive Kanban board (Define → Ideate → Prototype) |
| `/excel/`       | Excel Export   | Downloads an Excel report of all submissions             |
| `/powerbi/`     | Power BI       | Power BI report embedding page                           |
| `/admin/`       | Admin Panel    | Django admin interface (requires superuser)              |

---

## 📁 Project Structure

```
innovation-platform/
│
├── config/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Main settings (DB, apps, templates, etc.)
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
│
├── core/                    # Main application
│   ├── admin.py             # Admin panel registration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models (Submission, BoardItem)
│   ├── views.py             # View functions (dashboard, board, etc.)
│   ├── urls.py              # App-level URL routes
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   ├── base.HTML        # Base layout template
│   │   ├── dashboard.html   # Dashboard page
│   │   ├── submissions.html # Submissions list page
│   │   ├── board.html       # Workshop board page
│   │   ├── powerbi.html     # Power BI page
│   │   └── excel.html       # Excel export page
│   └── static/              # Static files (CSS, JS, images)
│       └── images/          # Image assets
│
├── db.sqlite3               # SQLite database file
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## ⚠️ Notes

- The project uses **SQLite** by default, which requires no additional database setup.
- The `DEBUG = True` setting in `settings.py` is intended for development only. Set it to `False` before deploying to production.
- Make sure to keep the `SECRET_KEY` in `settings.py` private in production environments.

---

## 📄 License

This project is for internal use by Seha Virtual Hospital.
