# 🎫 TiketQ API

**TiketQ API** is a simple backend service built with Flask that allows you to manage event tickets. It provides RESTful endpoints for creating, retrieving, updating, and deleting ticket records.

Each ticket includes event details and a usage status. The API ensures clean code structure, validation, and error handling best practices.

---

## 📚 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Ticket Schema](#ticket-schema)
- [Testing](#testing)
- [Postman Collection](#postman-collection)
- [Project Structure](#project-structure)
- [License](#license)

---

## 🌟 Features

- ✅ Full CRUD operations for tickets
- ✅ Input validation with custom validation logic
- ✅ Proper HTTP error handling (400, 404, 500)
- ✅ SQLAlchemy ORM with PostgreSQL
- ✅ Modular Flask app structure
- ✅ Postman collection for testing
- ✅ Docker & `.env` ready (optional)

---

## ⚙️ Prerequisites

- Python 3.11+
- PostgreSQL installed and running
- [uv](https://docs.astral.sh/uv/) (recommended for dependency management)
- `flask` CLI (comes with the app’s dependencies)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ferianai/ticket_api_be.git
cd ticket_api_be
```

### 2. Install dependencies

Using `uv` (recommended):

```bash
uv init
```

Or manually with `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root folder:

```env
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tiketq_db

JWT_SECRET_KEY=your_jwt_secret_key
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=604800
```

### 4. Set up the database

Ensure PostgreSQL is running, then create the database:

```bash
createdb tiketq_db
```

Run migrations:

```bash
flask --app app db init
flask --app app db migrate -m "Initial migration"
flask --app app db upgrade
```

---

## 🏃 Running the Application

Using Taskipy (`uv run task fr`):

```bash
uv run task fr
```

Or using Flask CLI directly:

```bash
flask --app app run --port 8000 --reload --debug
```

> The app will be available at: [http://localhost:8000](http://localhost:8000)

---

## 🔌 API Endpoints

### General

- `GET /` — Health check / Welcome message

### Tickets

| Method | Endpoint        | Description             |
| ------ | --------------- | ----------------------- |
| GET    | `/tickets`      | Retrieve all tickets    |
| POST   | `/tickets`      | Create a new ticket     |
| GET    | `/tickets/<id>` | Retrieve a ticket by ID |
| PATCH  | `/tickets/<id>` | Mark a ticket as used   |
| DELETE | `/tickets/<id>` | Delete a ticket         |

### 📝 Input Validation (on POST)

- `event_name`: required
- `location`: required
- `time`: required in ISO 8601 format (e.g., `2025-08-15T19:30:00`)

---

## ✅ Ticket Schema

Example JSON response from `/tickets`:

```json
{
  "id": 1,
  "event_name": "Music Festival",
  "location": "Jakarta Convention Center",
  "time": "2025-08-15T19:30:00",
  "is_used": false
}
```

> Note: Unique constraint on (`event_name`, `location`, `time`)

---

## 🧪 Testing

Run all tests using:

```bash
uv run pytest
```

Or directly:

```bash
pytest
```

Test cases are located in the `tests/` folder and include:

- Ticket creation
- Get ticket by ID
- Update and delete logic

---

## 📬 Postman Collection

Test and explore the API using this public Postman documentation:

🔗 [TiketQ API — Postman Docs](https://documenter.getpostman.com/view/44239234/2sB3BAMXxQ)

---

## 📁 Project Structure

```
ticket_api_be/
├── app.py                  # Entry point
├── config/                 # App configuration
├── instance/               # DB instance folder
├── models/                 # SQLAlchemy models
├── repo/                   # Repository layer
├── route/                  # Flask routes/blueprints
├── services/               # Business logic
├── shared/                 # Common utils
├── migrations/             # Alembic migration history
├── tests/                  # Pytest test suite
├── pyproject.toml          # Dependencies and config
├── README.md
└── .env                    # Environment variables
```

---

## 📦 Optional Docker Setup (Bonus)

To run the app via Docker:

### Dockerfile (simplified)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8000"]
```

You can add `docker-compose.yml` if needed for DB and service orchestration.

---

## 📜 License

This project is licensed under the **MIT License**.
See the [LICENSE](./LICENSE) file for full terms.
