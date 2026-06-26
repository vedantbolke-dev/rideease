# 🚲 RideEase — Bike Rental Management System

A full-stack web application for managing bike rentals with role-based access, real-time booking management, and an analytics dashboard. Built with **Django**, **MySQL**, and **Bootstrap 5**.

> Built by [Vedant Bolke](https://github.com/vedantbolke-dev)
> 
> 🌐 **Live Demo**: [vedantbolkedev.pythonanywhere.com](https://vedantbolkedev.pythonanywhere.com)
> 🔑 **Demo Admin Login**: Username: `admin` | Password: `Admin@123`

---

## ⚡ Tech Stack

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

---

## 📸 Screenshots

### 🏠 Customer Portal

#### Homepage
![Homepage](ride_easy%20images/Screenshot%202026-04-04%20113841.png)

<details>
<summary><b>🔍 View More Customer Pages (Bike Listings, Booking, Dashboard)</b></summary>
<br>

#### Bike Listings & Search
![Bike Listings](ride_easy%20images/Screenshot%202026-04-04%20114112.png)

#### Bike Details & Booking
![Bike Details](ride_easy%20images/Screenshot%202026-04-04%20114329.png)

#### User Dashboard
![User Dashboard](ride_easy%20images/Screenshot%202026-04-04%20114419.png)
</details>

### 🔧 Admin Dashboard

#### Revenue & Bookings Analytics
![Admin Dashboard](ride_easy%20images/Screenshot%202026-04-04%20114455.png)

<details>
<summary><b>⚙️ View More Admin Pages (Manage Bikes, Manage Bookings)</b></summary>
<br>

#### Manage Bikes
![Manage Bikes](ride_easy%20images/Screenshot%202026-04-04%20120128.png)

#### Manage Bookings & Users
![Manage Bookings](ride_easy%20images/Screenshot%202026-04-04%20120734.png)
</details>

---

## 🎯 Key Features

### 👤 Customer Portal
- **User Authentication** — Register, login, logout with Django's auth system
- **Smart Bike Search** — Filter by category, availability, fuel type & transmission
- **Booking System** — Date-based booking with automatic cost calculation (rate × days + helmet deposit)
- **Double-Booking Prevention** — Date overlap validation ensures no conflicts
- **Booking Lifecycle** — Track status (Pending → Confirmed → Completed / Cancelled)
- **Profile Management** — Update personal details, upload driving license

### 🔧 Admin Dashboard
- **Revenue Analytics** — Chart.js powered graphs (revenue, bookings trend, category breakdown)
- **Bike Management** — Full CRUD with image upload & featured bike selection
- **Booking Control** — Approve, reject, or complete bookings with admin notes
- **User Management** — Block/unblock users, view user activity
- **Inbox Messages** — View and respond to contact inquiries

---

## 🏗️ Architecture

```
rideease/
├── apps/
│   ├── bikes/          # Bike listings, category filter, search
│   ├── bookings/       # Booking CRUD, invoice PDF, star reviews
│   ├── dashboard/      # Admin analytics, charts, CSV/PDF exports
│   └── users/          # Auth, custom user profiles
├── rideease/           # Django project settings & URL routing
├── templates/          # HTML templates & layouts
├── static/             # CSS stylesheets & JS scripts
├── media/              # Uploaded profile & bike assets
├── manage.py
├── requirements.txt
└── .env.example
```
