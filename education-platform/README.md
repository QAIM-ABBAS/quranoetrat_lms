# Education Platform

A production-ready school management system for managing teachers, classes, lessons, and student enrollment — built with **FastAPI**, **React**, and **PostgreSQL**.

## Domain model in one look

```
SchoolClass "9B - Spring 2026"
 ├── Lesson "Mathematics"  →  Teacher: Ahmed Hassan
 ├── Lesson "Physics"      →  Teacher: Leila Rahimi
 └── Lesson "English"      →  Teacher: Mark Evans

Students in this class: [Sara, Ali, Yusuf, ...]
```

A class is the enrollment boundary. Students are enrolled directly into a class, and lessons belong to that class. Each lesson has exactly one teacher, but the class roster is the source of truth for which students belong to the class.

---

## Tech stack

| Layer        | Technology                                                  |
| ------------ | ----------------------------------------------------------- |
| Backend API  | FastAPI 0.115 · async SQLAlchemy 2.0 · Alembic              |
| Database     | PostgreSQL 16                                               |
| Auth         | JWT (python-jose) · bcrypt (passlib)                       |
| Frontend     | React 18 · TypeScript · Vite · React Query v5 · Axios      |
| Design       | ui-ux-pro-max: Minimalism/Swiss style · B2B Navy palette    |
| Containers   | Docker · Docker Compose (single `up --build` to run it all) |
| CI           | GitHub Actions (backend lint+test, frontend build)          |

---

## Quick start — Docker (recommended)

```bash
# 1. Clone and enter
git clone <your-repo-url> education-platform
cd education-platform

# 2. Copy and edit env (only POSTGRES_PASSWORD and SECRET_KEY need changing for local)
cp backend/.env.example backend/.env

# 3. Boot everything
docker compose up --build

# 4. Seed the first admin user
docker compose exec backend python scripts/seed.py
```

| Service  | URL                          |
| -------- | ---------------------------- |
| Frontend | http://localhost:5173        |
| API      | http://localhost:8000/api/v1 |
| Swagger  | http://localhost:8000/docs   |
| ReDoc    | http://localhost:8000/redoc  |

Default admin after seeding: `admin@school.local` / `admin123`

---

## Local development (without Docker)

### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL 16 running locally (or Docker for just the DB)

### Backend

```bash
# Spin up just the DB if you want
docker compose up db -d

cd backend

# Install in editable mode with dev extras
pip install -e ".[dev]"

# Configure
cp .env.example .env
# Edit .env: set POSTGRES_HOST=localhost and a real SECRET_KEY

# Run migrations (generates the first migration automatically)
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

# Seed admin user
python scripts/seed.py

# Start the dev server (hot reload)
uvicorn app.main:app --reload --port 8000
```

> **Note:** No Alembic migration file is committed in the repo intentionally — generate it fresh after install so it reflects your exact SQLAlchemy/Alembic version. This avoids migration drift in teams.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_BASE_URL=http://localhost:8000/api/v1
npm run dev            # http://localhost:5173
```

---

## Running tests

```bash
cd backend
pytest -v

# With coverage
pytest --cov=app --cov-report=term-missing
```

---

## Environment variables

### Backend (`backend/.env`)

| Variable                      | Default               | Description                              |
| ----------------------------- | --------------------- | ---------------------------------------- |
| `ENVIRONMENT`                 | `development`         | `development` or `production`            |
| `POSTGRES_HOST`               | `db`                  | DB host (use `localhost` for local dev)  |
| `POSTGRES_PORT`               | `5432`                |                                          |
| `POSTGRES_USER`               | `postgres`            |                                          |
| `POSTGRES_PASSWORD`           | `postgres`            | **Change this in production**            |
| `POSTGRES_DB`                 | `education_platform`  |                                          |
| `SECRET_KEY`                  | `change-me`           | **Change this in production** (64+ char) |
| `ALGORITHM`                   | `HS256`               | JWT signing algorithm                    |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440`                | 24 hours                                 |
| `BACKEND_CORS_ORIGINS`        | `["http://localhost:5173"]` | JSON array of allowed origins      |

### Frontend (`frontend/.env`)

| Variable              | Default                         |
| --------------------- | ------------------------------- |
| `VITE_API_BASE_URL`   | `http://localhost:8000/api/v1`  |

---

## API overview

All endpoints live under `/api/v1`. Prefix every path below with that.

| Method | Path                                  | Auth required | Description                              |
| ------ | ------------------------------------- | ------------- | ---------------------------------------- |
| POST   | `/auth/login`                         | No            | Get JWT token                            |
| POST   | `/auth/register`                      | Admin         | Create user (admin/teacher/student)      |
| GET    | `/teachers`                           | Admin         | List all teachers                        |
| POST   | `/teachers`                           | Admin         | Create teacher                           |
| GET    | `/teachers/{id}`                      | Admin/Teacher | Get teacher detail                       |
| PUT    | `/teachers/{id}`                      | Admin         | Update teacher                           |
| DELETE | `/teachers/{id}`                      | Admin         | Delete teacher                           |
| GET    | `/students`                           | Admin         | List all students                        |
| POST   | `/students`                           | Admin         | Create student                           |
| GET    | `/students/{id}`                      | Admin/Teacher | Get student detail                       |
| GET    | `/classes`                            | Admin         | List all classes                         |
| POST   | `/classes`                            | Admin         | Create class                             |
| GET    | `/classes/{id}`                       | Admin/Teacher | Get class with its lessons               |
| GET    | `/lessons`                            | Admin/Teacher | List lessons (filtered by class/teacher) |
| POST   | `/lessons`                            | Admin         | Create lesson (assign teacher + class)   |
| GET    | `/lessons/{id}`                       | Admin/Teacher | Lesson detail with enrollment list       |
| GET    | `/enrollments`                        | Admin         | List enrollments                         |
| POST   | `/enrollments`                        | Admin         | Enroll a student in a class              |
| POST   | `/enrollments/bulk`                   | Admin         | Bulk-enroll a list of students into a class |
| DELETE | `/enrollments/{class_id}/{student_id}` | Admin       | Remove a student from a class            |

Full interactive docs at `/docs` (Swagger) or `/redoc`.

---

## Roles

| Role      | What they can do                                              |
| --------- | ------------------------------------------------------------- |
| `admin`   | Everything — CRUD on all resources                            |
| `teacher` | View their own lessons and enrolled students. Read-only else. |
| `student` | View lessons for the classes they are enrolled in. Nothing else. |

---

## Project structure

```
education-platform/
├── backend/                    FastAPI application
│   ├── alembic/                DB migration scripts (generate, don't edit)
│   ├── app/
│   │   ├── core/               Config, security (JWT/bcrypt), logging, exceptions
│   │   ├── db/                 Engine, session factory, declarative base
│   │   ├── models/             SQLAlchemy ORM models
│   │   ├── schemas/            Pydantic request/response schemas
│   │   ├── crud/               DB access layer (no business logic)
│   │   ├── services/           Business rules (bulk enroll, schedule conflict checks)
│   │   └── api/v1/endpoints/   FastAPI routers
│   ├── tests/                  pytest suite
│   └── scripts/                seed.py, wait_for_db.sh
├── frontend/                   React + Vite app
│   ├── src/
│   │   ├── components/ui/      Shared UI components (Button, Card, Table, Badge…)
│   │   ├── features/           Feature slices (classes/, lessons/, students/…)
│   │   ├── pages/              Route-level page components
│   │   ├── hooks/              Custom React hooks
│   │   ├── store/              Auth/session state (Zustand or Context)
│   │   └── styles/             Design tokens CSS + globals
│   └── design-system/MASTER.md Design token reference (from ui-ux-pro-max)
├── docker-compose.yml
├── .github/workflows/          CI: lint+test backend, build frontend
└── docs/
    └── architecture.md         Deep-dive on decisions and data model
```

---

## Production checklist

- [ ] Set `SECRET_KEY` to a random 64+ char string (`openssl rand -hex 32`)
- [ ] Set `POSTGRES_PASSWORD` to something strong
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `BACKEND_CORS_ORIGINS` to your real frontend domain
- [ ] Put Nginx (or Caddy) in front — don't expose uvicorn raw on port 8000
- [ ] Enable Postgres SSL (`sslmode=require` in DATABASE_URL)
- [ ] Set up backups for the `pgdata` Docker volume
- [ ] Rotate the admin password from `admin123` after first login

---

## Contributing

1. Branch off `main`
2. Backend changes: run `ruff check .` before pushing (CI enforces it)
3. Any model change: `alembic revision --autogenerate -m "description"`
4. Open a PR — CI runs automatically