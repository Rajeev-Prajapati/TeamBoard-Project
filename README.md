# TeamBoard Backend

A Django REST Framework backend implementing JWT Authentication, Company Management, Knowledge Base Search, Query Logging, and an Admin Usage Dashboard.

---

# Tech Stack

- Python 3
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Simple JWT

---

# Features

- User Registration
- User Login
- JWT Authentication
- Company Auto Creation using Signals
- Secure API Key Generation
- Knowledge Base Search
- Query Logging
- Admin Usage Summary

---

# Project Structure

```
teamboard/
│
├── api/
├── teamboard/
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── README.md
└── .env.example
```

---

# Database Setup

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/TeamBoard-Project.git
cd TeamBoard-Project
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key

DB_NAME=teamboard_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

DEBUG=True
```

---

## 5. Start PostgreSQL Using Docker

```bash
docker compose up -d
```

Verify that the PostgreSQL container is running:

```bash
docker ps
```

---

# Apply Migrations

Create database tables:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

---

# Run the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

---

# Seed Knowledge Base Entries

You can seed the `KBEntry` table in one of the following ways:

- Using pgAdmin
- Using the Django shell
- Using a custom Django management command

### Example using Django Shell

```bash
python manage.py shell
```

```python
from api.models import KBEntry

KBEntry.objects.create(
    question="What is JWT?",
    answer="JSON Web Token is used for authentication.",
    category="api"
)

KBEntry.objects.create(
    question="What is select_related()?",
    answer="select_related performs SQL joins for related objects.",
    category="framework"
)
```

Create at least **10 knowledge base entries** before testing the query endpoint.

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/register/` | Register a company |
| POST | `/api/auth/login/` | Login and receive JWT |
| POST | `/api/kb/query/` | Search the knowledge base |
| GET | `/api/admin/usage-summary/` | View usage summary (Admin only) |

---

# Authentication

Protected endpoints require a JWT Access Token.

Example header:

```
Authorization: Bearer <access_token>
```

---

# Postman Collection

The repository includes:

```
TeamBoard_API.postman_collection.json
```

containing all required test scenarios.

---

# Author

Rajeev Prajapati
