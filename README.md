
# Fintech API

A comprehensive personal budgeting API built with Django REST Framework. This project demonstrates a wide range of backend development concepts, from basic CRUD operations and secure authentication to advanced features like asynchronous task processing, database seeding, and automated documentation.

## ✅ Features

#### Core API

  - **User Authentication**: Secure user registration and login system using **JWT**.
  - **CRUD Operations**: Full Create, Read, Update, and Delete functionality for:
      - Transactions
      - Categories
      - Budgets
  - **Custom Reporting**:
      - Endpoint for a monthly summary of income vs. expenses.
      - Endpoint that aggregates spending by category, formatted for data visualization.
  - **Data Export**: Functionality to export user transactions to a **CSV** file.

#### Advanced Architecture & Features

  - **Asynchronous Tasks**: Uses **Celery** and **Redis** (via Docker) to handle slow background tasks like sending email reports without blocking the user.
  - **Advanced Filtering & Search**:
      - Precise, field-based filtering on transactions (by date range, amount, type).
      - Full-text search across transaction descriptions and category names.
  - **Scalability & Security**:
      - **Pagination** to handle large datasets efficiently.
      - **Throttling** to protect the API from abuse.
  - **Automated Documentation**: Generates an interactive **Swagger UI** for the entire API using `drf-spectacular`.
  - **Database Seeding**: Includes a custom management command (`seed_db`) to populate the database with realistic fake data using the `Faker` library.

## 🛠️ Tech Stack

  - **Backend**: Django, Django REST Framework
  - **Database**: SQLite (Development), PostgreSQL (Production)
  - **Asynchronous Tasks**: Celery, Redis
  - **Authentication**: djangorestframework-simplejwt
  - **Tooling**: Docker, Gunicorn, `django-filter`, `drf-spectacular`

-----

## 📖 API Documentation

This project includes auto-generated, interactive API documentation. Once the server is running, you can access it at:

**`http://127.0.0.1:8000/api/schema/docs/`**

-----

## ⚙️ Local Installation and Setup

### Prerequisites

  - Python (3.11+)
  - Docker Desktop
  - Git

### 1\. Clone the Repository

```bash
git clone <your_repository_url>
cd <repository_folder>
```

### 2\. Set Up the Environment

```powershell
# Create and activate a virtual environment (on Windows)
python -m venv venv
.\venv\Scripts\activate

# Install all required packages
pip install -r requirements.txt
```

### 3\. Start Redis

Use Docker to start the Redis container in the background.

```bash
docker run -d --name my-redis-container -p 6379:6379 redis
```

*(To restart this container later, use `docker start my-redis-container`)*

### 4\. Set Up the Database

```powershell
# Create the database schema
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# (Optional) Populate the database with sample data
python manage.py seed_db
```

-----

## 🚀 Running the Application

To run the full application, you need **two separate terminals** (and the Redis Docker container running).

#### Terminal 1: Start the Django Server

```powershell
# Make sure your venv is active
python manage.py runserver
```

#### Terminal 2: Start the Celery Worker

```powershell
# Make sure your venv is active
celery -A fintech worker -P solo --loglevel=info
```

The API is now running at `http://127.0.0.1:8000/`.

-----

## Endpoints Overview

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/api/register/` | `POST` | Create a new user account. | No |
| `/api/token/` | `POST` | Log in and receive JWT tokens. | No |
| `/api/transactions/` | `GET`, `POST` | List or create transactions. | Yes |
| `/api/transactions/<id>/` | `GET`, `PUT`, `DELETE`| Retrieve, update, or delete a transaction. | Yes |
| `/api/budgets/` | `GET`, `POST` | List or create monthly budgets. | Yes |
| `/api/summary/` | `GET` | Get a summary of monthly income/expenses. | Yes |
| `/api/transactions/export/` | `GET` | Download a CSV file of transactions. | Yes |
| `/api/reports/email-summary/`| `POST` | Trigger a background task to email a report. | Yes |
