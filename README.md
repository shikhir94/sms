# School Service (Python)

Production-style Python API for school management: **classes**, **subjects**, **teachers**, and **timetables**. Built with FastAPI, SQLAlchemy 2 (async), and PostgreSQL. Replaces the previous Spring Boot application with the same API surface.

## Requirements

- **Python 3.11+** (recommended 3.12)
- **PostgreSQL** (e.g. your existing Docker container on `localhost:5432`)
- **Pip** (or uv/poetry) to install dependencies

If Python is not installed on your machine, install it first (e.g. from [python.org](https://www.python.org/downloads/) or via your package manager) and confirm before proceeding.

## Setup

1. **Create a virtual environment** (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies** (do not run until you have Python and are ready to install):

   ```bash
   pip install -r requirements.txt
   ```

   Or install the project in editable mode:

   ```bash
   pip install -e .
   ```

3. **Environment**: Copy `.env.example` to `.env` and set `DATABASE_URL` if your PostgreSQL user/password/host/port differ from:

   - Host: `localhost`, Port: `5432`, User: `postgres`, Password: `password`, DB: `postgres`

4. **Database**: Ensure PostgreSQL is running (e.g. your Docker container). Then either:

   - **Option A – Migrations (recommended for production):**

     ```bash
     alembic upgrade head
     ```

   - **Option B – Auto-create tables (dev):** Tables are created on first app startup via `init_db()`.

## Run the application

From the project root (with virtualenv activated):

```bash
uvicorn school_service.main:app --host 0.0.0.0 --port 8000
```

- API: [http://localhost:8000](http://localhost:8000)
- OpenAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health: [http://localhost:8000/health](http://localhost:8000/health)

## API endpoints (same as former Spring Boot app)

| Method | Path | Description |
|--------|------|-------------|
| GET    | `/class` | List all classes |
| POST   | `/class` | Create a class |
| GET    | `/subject` | List all subjects |
| GET    | `/subject/{id}` | Get subject by id |
| POST   | `/subject` | Create subject |
| PUT    | `/subject` | Update subject (body must include `id`) |
| DELETE | `/subject/{id}` | Delete subject |
| GET    | `/teacher` | List all teachers |
| POST   | `/teacher` | Create teacher (JSON: `firstName`, `lastName`, `userName`) |
| GET    | `/timetable` | List all timetables |
| GET    | `/timetable/findByClass/{class_id}` | Timetables by class |
| GET    | `/timetable/findByTeacher/{teacher_id}` | Timetables by teacher |
| POST   | `/timetable` | Create timetable |

CORS is enabled for all origins (same as `@CrossOrigin` in Spring).

## Project layout

```
school-service/
├── src/
│   └── school_service/
│       ├── main.py           # FastAPI app
│       ├── config.py         # Settings from env
│       ├── database.py       # Async engine & session
│       ├── models/           # SQLAlchemy models
│       ├── schemas/          # Pydantic request/response
│       ├── repositories/    # Data access
│       └── routers/          # API routes
├── alembic/                  # Migrations
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## New dependencies / installing anything

If your machine does not have Python or you prefer not to install new tools without being asked: **confirm with me before running any install command** (e.g. `pip install`, `brew install python`, etc.). This README assumes you will install dependencies only after you are ready.
