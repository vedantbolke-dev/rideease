# 🚲 RideEase: Premium Bike Rental System

A high-end, feature-rich Django web application designed for seamless bike rentals, featuring role-based access control, an interactive analytics dashboard, live pricing estimation, automated PDF invoices, CSV/PDF data exports, and a modern dark/light theme.

---

[![Python](https://img.shields.io/badge/python-3.10+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap 5](https://img.shields.io/badge/bootstrap-5.3-7952b3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![SQLite](https://img.shields.io/badge/sqlite-3.0-07405e?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![MySQL](https://img.shields.io/badge/mysql-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

---

## 🛠️ Tech Stack & Architecture

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python 3.10+, Django 4.2 | Scalable MVC backend architecture. |
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Bootstrap 5 | Glassmorphic UI with local-storage dark/light toggle and custom animations. |
| **Database** | SQLite (Default fallback) / MySQL 8.0 | Dual-compatible database layer with automatic environment detection. |
| **Reports** | ReportLab (PDF), CSV Writer | Direct-to-client automated invoice generation and data exports. |
| **Charts** | Chart.js 4 | Interactive charts for administrator analytics dashboard. |

### System Architecture Diagram

```mermaid
graph TD
    classDef appNode fill:#ff5c00,stroke:#e04f00,stroke-width:2px,color:#fff;
    classDef dbNode fill:#07405e,stroke:#052e44,stroke-width:2px,color:#fff;
    classDef clientNode fill:#18181b,stroke:#27272a,stroke-width:2px,color:#a1a1aa;

    Client[Browser / Client UI] :::clientNode
    UsersApp[users app: CustomUser & Auth] :::appNode
    BikesApp[bikes app: Bike & Contacts] :::appNode
    BookingsApp[bookings app: Booking & Reviews] :::appNode
    DashboardApp[dashboard app: Analytics & Reports] :::appNode
    
    Database[(Database Layer: SQLite / MySQL)] :::dbNode

    Client -->|Interacts| UsersApp
    Client -->|Browse & Search| BikesApp
    Client -->|Rents & Reviews| BookingsApp
    Client -->|Controls & Export| DashboardApp

    UsersApp -->|Performs Auth| Database
    BikesApp -->|Saves Inventory| Database
    BookingsApp -->|Calculates Price & Logs| Database
    DashboardApp -->|Aggregates Analytics| Database
```

---

## ✨ Key Features

- **🌓 Obsidian Design System:** Premium dark and light mode toggle backed by local storage and an anti-flicker script.
- **🛡️ Role-Based Access Control:** Separate customer dashboard (active bookings, profiles, invoice histories) and administrator dashboard (fleet statistics, booking approvals, contact inbox).
- **🚴 Smart Booking Engine:** Real-time cost estimator on pickup/dropoff dates, including deposit calculations and automatic vehicle status lockouts.
- **📊 Business Intelligence Panel:** Interactive charts (sales growth line charts, vehicle category doughnuts, booking summaries) rendered via Chart.js.
- **📄 Instant PDF Invoicing:** Direct download of structured, beautifully typeset PDF booking receipts generated via ReportLab.
- **📥 Enterprise Data Exports:** Single-click exports of all bookings, vehicles, and user accounts in structured CSV or print-ready PDF formats.
- **📦 Dual-Database Support:** Defaults to an instant plug-and-play SQLite database for quick local reviews, with seamless configuration switches to production-ready MySQL.

---

## ⚡ Quick Start (10-Second SQLite Setup)

Review the project instantly with zero external database configuration:

### 1. Clone & Navigate
```bash
git clone https://github.com/yourusername/rideease.git
cd rideease
```

### 2. Create and Activate Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Server (SQLite is pre-populated out-of-the-box!)
Because a fully seeded SQLite database (`db.sqlite3`) is included in the project, you don't even need to run migrations or seed commands. Just launch the server:
```bash
python manage.py runserver
```
Navigate to **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 💾 Production-Ready Setup (MySQL)

For full relational database configurations:

### 1. Configure Environment Variables
Copy `.env.example` to `.env` and set `DB_ENGINE=mysql`:
```bash
cp .env.example .env
```
Update `.env` with your local MySQL credentials:
```ini
DB_ENGINE=mysql
DB_NAME=rideease_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### 2. Create MySQL Database
Run in your MySQL client:
```sql
CREATE DATABASE rideease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Run Migrations & Seed Mock Data
```bash
python manage.py migrate
python manage.py seed_data
```

---

## 🔑 Login Credentials

| Role | Username | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `Admin@123` | `/dashboard/` |
| **Customer** | `rahul_sharma` | `User@123` | `/users/dashboard/` |
| **Customer** | `priya_patil` | `User@123` | `/users/dashboard/` |

---

## 🎯 Important Endpoints

| Page | URL | Description |
| :--- | :--- | :--- |
| **Landing Page** | `/` | Responsive home page with category browsers and CTA triggers. |
| **Bike Fleet** | `/bikes/` | Fleet catalogs with search, category, and availability filters. |
| **Admin Analytics** | `/dashboard/` | Chart.js analytics dashboard, inbox, and fleet managers. |
| **Data Exports** | `/dashboard/export/bookings/pdf/` | Export system logs directly to print-ready PDF/CSV reports. |
| **Booking Invoice** | `/bookings/<id>/invoice/pdf/` | Generate dynamic PDF client invoices on-demand. |

---

## 📝 Developed By

- **Lead Developer:** [Vedant Bolke](https://github.com/vedantbolke-dev)
- **Institution:** Shri Dnyaneshwar Mahavidhalaya, Maharashtra
- **Academic Year:** 2025–2026
- **Specialization:** B.Sc. Computer Science (Web Technology Project)
