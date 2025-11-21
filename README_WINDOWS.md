# 🍏 FoodTracker -- Innovatex Hackathon (Part 1)

**Windows Setup Guide (PostgreSQL + Django)**\
SDG 2: Zero Hunger \| SDG 12: Responsible Consumption

FoodTracker is a full-stack Django web application that helps users
reduce food waste by tracking expiry dates and providing sustainability
tips.

------------------------------------------------------------------------

## ⚙️ Windows System Setup (PostgreSQL + Django)

### ✅ 1. Install PostgreSQL (Windows)

1.  Download PostgreSQL Installer:\
    https://www.postgresql.org/download/windows/
2.  Install with default settings:
    -   **User:** postgres\
    -   **Password:** (Use same password in `settings.py`)\
    -   **Port:** 5432\
    -   Install pgAdmin (optional but helpful)
3.  Verify PostgreSQL service is running:
    -   Press `Win + R` → type `services.msc`
    -   Find **postgresql-x.x**
    -   Ensure it is **Running**

------------------------------------------------------------------------

### ✅ 2. Create Database (Windows)

#### **Method A -- Using pgAdmin**

1.  Open **pgAdmin**\
2.  Login using your postgres password\
3.  Right‑click **Databases → Create → Database**\
4.  Name it: **innovatex_db**\
5.  Save

#### **Method B -- Using SQL Shell (psql)**

    CREATE DATABASE innovatex_db;
    ALTER USER postgres WITH PASSWORD 'your_password';

> Make sure this password matches the one in **settings.py**

------------------------------------------------------------------------

## ✅ 3. Project Setup (Windows CMD / PowerShell)

### Clone Repository

    git clone <your-repo-url>
    cd expiry_tracker

### Create Virtual Environment

    python -m venv venv
    venv\Scripts\activate

### Install Dependencies

    pip install django psycopg2-binary pillow django-crispy-forms crispy-bootstrap4

------------------------------------------------------------------------

## 🔧 4. Configure Database in settings.py

Inside `expiry_tracker/settings.py`:

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'innovatex_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

------------------------------------------------------------------------

## 🚀 5. Running the Application

### Apply Migrations

    python manage.py makemigrations
    python manage.py migrate

### Seed Demo Data

    python manage.py seed

Demo account:\
- **Username:** demo_user\
- **Password:** password123

### Start Server

    python manage.py runserver

Visit:\
http://127.0.0.1:8000/

------------------------------------------------------------------------

## 📂 Project Structure

    expiry_tracker/
    ├── manage.py
    ├── expiry_tracker/
    │   ├── settings.py
    │   ├── urls.py
    ├── tracker/
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── management/
    │   │   └── commands/
    │   │       └── seed.py
    │   └── templates/
    │       └── tracker/
    └── media/

------------------------------------------------------------------------

## ⭐ Windows Troubleshooting

### ❗ Password authentication failed

Run:

    ALTER USER postgres WITH PASSWORD 'newpassword';

Update `settings.py` to match.

### ❗ psycopg2 fails to install

    pip install psycopg2-binary

### ❗ Cannot connect to server

-   PostgreSQL service not running\
-   Wrong password\
-   Port 5432 blocked

------------------------------------------------------------------------

## ✔️ All Done!

Your Django + PostgreSQL FoodTracker project is now fully configured on
Windows.
