# Architecture

## Table of contents

1. [Domain model](#1-domain-model)
2. [Database schema](#2-database-schema)
3. [Backend layering](#3-backend-layering)
4. [Auth & authorization flow](#4-auth--authorization-flow)
5. [API design decisions](#5-api-design-decisions)
6. [Frontend architecture](#6-frontend-architecture)
7. [Error handling strategy](#7-error-handling-strategy)
8. [Performance considerations](#8-performance-considerations)
9. [Security checklist](#9-security-checklist)
10. [Deployment topology](#10-deployment-topology)

---

## 1. Domain model

The core insight of the data model is that **enrollment is at the lesson level, not the class level**.

```
SchoolClass "9B - Spring 2026"
 ├── Lesson "Mathematics"  →  teacher_id: 1  →  enrolled: [student 3, 5, 7]
 ├── Lesson "Physics"      →  teacher_id: 2  →  enrolled: [student 3, 8, 9]
 └── Lesson "English"      →  teacher_id: 3  →  enrolled: [student 5, 7, 8]
```

Key consequences:
- A `SchoolClass` has **no direct student list** — a student's membership in a class is inferred by querying which of its lessons they are enrolled in.
- Multiple teachers teach within the same class (one per lesson). There is no "class teacher" concept in the data model; that can be a UI convention if needed.
- The same student can be in multiple lessons within the same class (partial enrollment is possible and valid).
- A teacher can teach lessons in multiple classes simultaneously.

---

## 2. Database schema

### Tables

```
users
  id              SERIAL PRIMARY KEY
  email           TEXT UNIQUE NOT NULL
  hashed_password TEXT NOT NULL
  role            VARCHAR(20) NOT NULL  -- 'admin' | 'teacher' | 'student'
  is_active       BOOLEAN DEFAULT TRUE
  created_at      TIMESTAMPTZ DEFAULT NOW()
  updated_at      TIMESTAMPTZ DEFAULT NOW()

teachers
  id              SERIAL PRIMARY KEY
  user_id         INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE
  first_name      TEXT NOT NULL
  last_name       TEXT NOT NULL
  phone           TEXT
  department      TEXT
  created_at      TIMESTAMPTZ DEFAULT NOW()
  updated_at      TIMESTAMPTZ DEFAULT NOW()

students
  id              SERIAL PRIMARY KEY
  user_id         INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE
  first_name      TEXT NOT NULL
  last_name       TEXT NOT NULL
  phone           TEXT
  grade           TEXT          -- e.g. "9", "10"
  created_at      TIMESTAMPTZ DEFAULT NOW()
  updated_at      TIMESTAMPTZ DEFAULT NOW()

school_classes
  id              SERIAL PRIMARY KEY
  name            TEXT NOT NULL        -- e.g. "9B"
  term            TEXT NOT NULL        -- e.g. "2026-Spring"
  description     TEXT
  created_at      TIMESTAMPTZ DEFAULT NOW()
  updated_at      TIMESTAMPTZ DEFAULT NOW()
  UNIQUE (name, term)                  -- same class can't exist twice in same term

lessons
  id              SERIAL PRIMARY KEY
  school_class_id INT NOT NULL REFERENCES school_classes(id) ON DELETE CASCADE
  teacher_id      INT NOT NULL REFERENCES teachers(id) ON DELETE RESTRICT
  subject         TEXT NOT NULL        -- e.g. "Mathematics"
  description     TEXT
  schedule_info   TEXT                 -- free-text e.g. "Mon/Wed 09:00-10:30"
  created_at      TIMESTAMPTZ DEFAULT NOW()
  updated_at      TIMESTAMPTZ DEFAULT NOW()

enrollments
  lesson_id       INT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE
  student_id      INT NOT NULL REFERENCES students(id) ON DELETE CASCADE
  enrolled_at     TIMESTAMPTZ DEFAULT NOW()
  PRIMARY KEY (lesson_id, student_id)  -- composite PK, no surrogate needed
```

### Indexes beyond PKs

```sql
CREATE INDEX ix_lessons_class   ON lessons (school_class_id);
CREATE INDEX ix_lessons_teacher ON lessons (teacher_id);
CREATE INDEX ix_enroll_student  ON enrollments (student_id);
```

The `enrollments` composite PK `(lesson_id, student_id)` is itself the unique constraint that bulk-enroll exploits with `INSERT … ON CONFLICT DO NOTHING`.

### Why `school_classes` and not `classes`?

`class` is a reserved keyword in Python, SQL, and JavaScript. Using `school_classes` everywhere (table name, model name, schema name) avoids escaping noise in every query and import.

---

## 3. Backend layering

```
HTTP request
     │
     ▼
api/v1/endpoints/*.py          ← HTTP only: parse request, call service or crud,
     │                            return response. No raw SQL, no business rules.
     ▼
services/*.py                  ← Business rules: multi-step operations, invariant
     │                            checks, cross-entity logic (e.g. bulk enroll,
     │                            conflict detection). Calls crud layer.
     ▼
crud/*.py                      ← DB access only: SELECT / INSERT / UPDATE / DELETE
     │                            via SQLAlchemy ORM. Returns ORM objects. No HTTP.
     ▼
models/*.py                    ← SQLAlchemy ORM model definitions. No methods,
                                  no business logic.
```

**Rule:** endpoints never call `db.execute()` for writes involving more than one table — those live in `services/`. Endpoints only call `crud.*` directly for simple single-table reads (GET by id, list with filters).

### CRUD base pattern

`crud/base.py` provides a generic typed `CRUDBase[ModelType, CreateSchema, UpdateSchema]` with `get`, `get_multi`, `create`, `update`, `remove`. Domain-specific CRUD classes inherit from it and add methods like `get_by_email` or `get_by_class`.

### Services

`services/enrollment_service.py` is the main business layer entry:
- `enroll(db, lesson_id, student_id)` — validates both IDs exist, then upserts
- `bulk_enroll(db, lesson_id, student_ids)` — batch insert via core `INSERT … ON CONFLICT DO NOTHING`
- `unenroll(db, lesson_id, student_id)` — hard delete with existence check
- `get_roster(db, lesson_id)` — returns full student list for a lesson

---

## 4. Auth & authorization flow

### Login flow

```
POST /api/v1/auth/login  { email, password }
         │
         ├─► crud.user.get_by_email(email)    → User or None
         ├─► security.verify_password(plain, hashed)
         └─► security.create_access_token(sub=str(user.id), role=user.role)
                        │
                        ▼
              { access_token: "eyJ...", token_type: "bearer" }
```

### Per-request auth (FastAPI dependency injection)

```python
# api/deps.py

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = security.decode_access_token(token)   # raises 401 if invalid/expired
    user = await crud.user.get(db, id=int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(401)
    return user


def require_role(*roles: str):
    async def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(403)
        return current_user
    return checker
```

Usage in endpoints:
```python
@router.get("/teachers", dependencies=[Depends(require_role("admin"))])
@router.get("/lessons/{id}", dependencies=[Depends(require_role("admin", "teacher"))])
```

### Token contents

```json
{ "sub": "42", "role": "teacher", "exp": 1751234567 }
```

No refresh token in v1 — 24h expiry is acceptable for a school internal tool. Add refresh tokens if the product requires "stay logged in" sessions.

---

## 5. API design decisions

### Versioning

All routes under `/api/v1/`. The prefix is configured in `core/config.py` so bumping to v2 is a one-line change + a new router file.

### Pagination

`GET /teachers`, `/students`, `/lessons`, `/classes` all accept `?skip=0&limit=50`. Default page size is 50. No cursor-based pagination in v1 (school sizes don't warrant it — even a large school has < 5000 students).

### Filtering

Lessons support `?class_id=` and `?teacher_id=` query params. Enrollments support `?lesson_id=` and `?student_id=`. All filters are AND-combined.

### Bulk enroll endpoint

```
POST /api/v1/enrollments/bulk
{
  "lesson_id": 12,
  "student_ids": [3, 5, 7, 9, 11]
}
```

Uses Postgres `INSERT INTO enrollments (lesson_id, student_id) VALUES …  ON CONFLICT DO NOTHING` — idempotent, safe to call repeatedly with overlapping lists (e.g. re-importing a roster CSV). Returns a count of newly-enrolled vs already-enrolled.

### 404 vs 403

The API returns 404 (not 403) when a teacher requests a lesson that exists but doesn't belong to them — this avoids leaking the existence of other teachers' lessons. Only admin sees all lessons.

---

## 6. Frontend architecture

### Stack

```
React 18  ·  TypeScript  ·  Vite  ·  React Query v5  ·  Axios  ·  React Router v6
```

### Feature-slice layout

```
features/
  classes/
    api.ts          axios calls for /classes — useClasses(), useClass(id)
    ClassCard.tsx   display component
    ClassForm.tsx   create/edit form
    ClassTable.tsx  admin list view
  lessons/
    api.ts
    LessonCard.tsx
    RosterTable.tsx  (student list for a lesson)
    LessonForm.tsx
  students/
    api.ts
    StudentBadge.tsx
    StudentForm.tsx
  teachers/
    api.ts
    TeacherCard.tsx
    TeacherForm.tsx
  enrollment/
    api.ts           bulk enroll, unenroll
    EnrollModal.tsx  modal to add students to a lesson
```

Each feature owns its own API calls and display components. Pages in `pages/` are thin — they import from features and compose the page layout.

### Data fetching

React Query v5 with a shared query client in `lib/query-client.ts`. Stale time: 30s for lists, 5min for single-record lookups. Mutations invalidate the relevant list query on success.

### Auth state

Zustand store in `store/auth.ts` holds `{ user, token, isAuthenticated }`. On login, the token is stored in `localStorage` and the Axios client interceptor attaches it as `Authorization: Bearer <token>` on every request. On 401 response, the interceptor clears the store and redirects to `/login`.

### Role-based routing

`ProtectedRoute.tsx` wraps routes that need auth. It accepts an optional `allowedRoles` prop:
```tsx
<ProtectedRoute allowedRoles={["admin"]}>
  <TeacherManagement />
</ProtectedRoute>
```

Teachers land on a filtered lessons view showing only their own lessons. Students land on their enrollment list.

### Design system

See `design-system/MASTER.md` for the full token reference. CSS custom properties are declared in `styles/tokens.css` and applied globally. Component primitives in `components/ui/` (Button, Card, Table, Badge, Modal, Input, Select) are all built to accept a `variant` prop that maps to design token values.

---

## 7. Error handling strategy

### Backend

Every possible error type has a registered FastAPI exception handler in `core/exceptions.py`:

| Exception              | HTTP status | Notes                                    |
| ---------------------- | ----------- | ---------------------------------------- |
| `NotFoundError`        | 404         | Raised by CRUD when `.get()` returns None |
| `ConflictError`        | 409         | Explicit business-rule conflicts         |
| `IntegrityError`       | 409         | DB unique constraint violations          |
| `RequestValidationError` | 422       | Pydantic schema validation fails         |
| `JWTError`             | 401         | Invalid or expired token                 |
| `Exception` (catch-all)| 500         | Logged, generic message to client        |

All error responses have the shape `{ "detail": "human-readable message" }`.

### Frontend

Axios interceptor in `lib/api-client.ts` handles:
- `401` → clear auth store, redirect to `/login`
- `403` → toast "You don't have permission for this action"
- `422` → surface field errors inline in forms (React Query's `error.response.data.detail`)
- `5xx` → toast "Something went wrong, try again"

---

## 8. Performance considerations

### Database

- Async SQLAlchemy 2.0 with `asyncpg` driver — no thread-per-request overhead
- `pool_pre_ping=True` — avoids stale connection errors after DB restarts
- Alembic-managed indexes on all foreign keys and common filter columns
- `INSERT … ON CONFLICT DO NOTHING` for bulk enrollment — single round-trip regardless of list size

### API

- FastAPI's async path handlers — never blocks the event loop on DB I/O
- Pagination on all list endpoints — no unbounded queries
- Python-jose JWT verification is synchronous but sub-millisecond — acceptable

### Frontend

- React Query caching eliminates redundant network calls
- Vite build with code-splitting per page route — teachers never download student-management code
- No global state for server data — only auth token and UI preferences live in the Zustand store

---

## 9. Security checklist

| Item                              | Status in v1 | Notes                                   |
| --------------------------------- | ------------ | --------------------------------------- |
| Passwords hashed with bcrypt      | ✅           | passlib, cost factor 12                 |
| JWT signed with HS256             | ✅           | Switch to RS256 if you add microservices|
| CORS restricted to known origins  | ✅           | `BACKEND_CORS_ORIGINS` env var          |
| Input validated at request boundary| ✅          | Pydantic schemas on every endpoint      |
| Role enforcement on every route   | ✅           | `require_role()` FastAPI dependency     |
| SQL injection impossible          | ✅           | ORM only — no raw string interpolation  |
| Secrets in environment variables  | ✅           | Never committed to repo                 |
| Rate limiting                     | ❌ (v2)      | Add `slowapi` or put Nginx in front     |
| HTTPS                             | ❌ (infra)   | Handled by reverse proxy (Nginx/Caddy)  |
| Refresh tokens                    | ❌ (v2)      | 24h expiry acceptable for internal tool |
| Audit log (who changed what)      | ❌ (v2)      | Add `audit_logs` table if required      |

---

## 10. Deployment topology

### Development (Docker Compose)

```
Browser → Vite dev server :5173 → (proxy /api/v1) → FastAPI :8000 → Postgres :5432
```

### Production (recommended)

```
Internet
  │
  ▼
Nginx / Caddy          (TLS termination, static file serving)
  ├── / → React build  (serve static files directly from Nginx)
  └── /api/v1 → FastAPI container :8000
                     │
                     ▼
               Postgres container   (or managed DB: RDS, Supabase, Neon)
                  volume: pgdata
```

Docker Compose for production:
- Add an `nginx` service with a `nginx.conf` that proxies `/api/v1` to `backend:8000` and serves the built frontend from `/usr/share/nginx/html`
- Build frontend: `npm run build` → copy `dist/` into the Nginx image
- Set `uvicorn --workers 4` (or use `gunicorn -k uvicorn.workers.UvicornWorker`)
- Mount Postgres data directory to a named volume, back it up with `pg_dump` on a cron schedule

### Environment parity

`ENVIRONMENT=development` enables:
- Swagger UI at `/docs` and `/redoc`
- `echo=True` on the SQLAlchemy engine (SQL in logs)
- Permissive CORS (`*` allowed in dev mode if desired)

`ENVIRONMENT=production` disables all of the above.
