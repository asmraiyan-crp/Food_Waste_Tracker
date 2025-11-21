# 🍏 FoodTracker - Innovatex Hackathon (Part 1)

### SDG 2: Zero Hunger \| SDG 12: Responsible Consumption

**FoodTracker** is a full-stack web application designed to help
individuals and households reduce food waste. By tracking inventory
expiry dates and providing sustainable consumption tips, we aim to
promote mindful food planning and security.

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Backend:** Python 3.13, Django 5.x
-   **Database:** PostgreSQL (Production-ready)
-   **Frontend:** HTML5, Bootstrap 4, CSS (Responsive)
-   **Architecture:** Model-View-Template (MVT)

------------------------------------------------------------------------

## ✨ Part 1 Features (Pre-Hack Requirements)

1.  **Authentication:** Secure User Registration & Login
    (Session-based).
2.  **Smart Inventory:** Track food items with expiry
    dates, categories, and quantity.
3.  **Visual Alerts:** Color-coded status logic
    (Red=Expired, Yellow=Expiring Soon, Green=Safe).
4.  **Sustainability Resources:** Educational tips mapped
    to your inventory categories (e.g., Dairy tips for Milk) 
5.  **Seed Data Script:** Automated population of 20+
    items and resources for testing].
6.  **Image Upload:** Interface for receipt scanning (UI
    implementation for future AI integration).

------------------------------------------------------------------------

## ⚙️ System Setup (Arch Linux & PostgreSQL)

Since this project uses PostgreSQL on Arch Linux, follow these specific
steps to configure your environment.

### 1. Install System Dependencies

``` bash
# Install PostgreSQL
sudo pacman -S postgresql

# Initialize the database engine
sudo -u postgres initdb -D /var/lib/postgres/data

# Start and Enable the service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Project Setup

``` bash
# Clone the repository
git clone <your-repo-url>
cd expiry_tracker

# Create Virtual Environment
python -m venv venv
source venv/bin/activate

# Install Python Dependencies
pip install django psycopg2-binary pillow django-crispy-forms crispy-bootstrap4
sudo pacman -S tesseract tesseract-data-eng
```

### 3. Database Configuration

The project requires a PostgreSQL database named innovatex_db.

``` bash
# Create the database (Arch Linux method)
sudo -u postgres createdb innovatex_db

# Set the password for the postgres user (Must match settings.py)
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'your_password';"
```

Note: Ensure expiry_tracker/settings.py has the matching password in the
DATABASES section.

------------------------------------------------------------------------

## 🚀 Running the Application

### 1. Apply Migrations

Initialize the database schema:

``` bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Seed Demo Data (Important)

Populate the database with the 20 required items and resources:

``` bash
python manage.py seed
```

Demo User Created: **demo_user**\
Password: **password123**

### 3. Start the Server

``` bash
python manage.py runserver
```

### 4. Access the App

URL: http://127.0.0.1:8000/

Login:
  username:demo_user
  password:password123

------------------------------------------------------------------------

## 📂 Project Structure

    expiry_tracker/
    ├── manage.py
    ├── expiry_tracker/        # Project Settings (Postgres config) & URLs
    ├── tracker/               # Main App
    │   ├── models.py          # DB Schemas (FoodItem, Resource, Profile) [cite: 22, 40]
    │   ├── views.py           # Tracking Logic & Controllers [cite: 61]
    │   ├── urls.py            # App Routes
    │   ├── management/
    │   │   └── commands/
    │   │       └── seed.py    # Data Seeding Script (Part 1 Req)
    │   └── templates/
    │       └── tracker/       # HTML Views (Dashboard, Login, Register)
    └── media/                 # User uploaded images (Receipts)
