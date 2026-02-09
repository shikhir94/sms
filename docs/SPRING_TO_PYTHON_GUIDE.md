# Spring Boot → Python/FastAPI: Concepts & Request Flow

A guide for developers with a Spring Boot / Java background. It maps Spring concepts to this project and walks through how a request becomes a response.

---

## 1. Module / Package Purpose (What Lives Where)

### Spring Boot vs This Project

| Spring Boot (Java) | This Project (Python) | Purpose |
|--------------------|------------------------|---------|
| **Application entry** | | |
| `@SpringBootApplication` class + `main()` | `main.py` + `uvicorn school_service.main:app` | Bootstrap: create app, wire config, start server. |
| **Configuration** | | |
| `application.properties` / `application.yml` | `config.py` + `.env` | DB URL, app name, debug, etc. Loaded once, used everywhere. |
| **Data layer** | | |
| `@Entity` classes (JPA) | `models/` (SQLAlchemy) | Table definitions: columns, relationships, table names. |
| `JpaRepository<T, ID>` | `repositories/` (plain classes) | CRUD and custom queries. No magic interface; you write methods that use the session. |
| **HTTP layer** | | |
| `@RestController` + `@GetMapping` etc. | `routers/` (FastAPI) | URL → handler. Define path, method, and call service/repository. |
| **Request/response shapes** | | |
| Same entity as JSON (or DTOs) | `schemas/` (Pydantic) | Validation of incoming JSON and serialization of outgoing JSON. Explicit request/response models. |
| **Dependency injection** | | |
| Constructor injection (`@Autowired`) | FastAPI `Depends(get_db)` and similar | “Give me a `AsyncSession` for this request.” Same idea: request-scoped dependencies. |

So in one sentence: **routers** handle HTTP and call **repositories**; **repositories** use the **database session** and **models**; **schemas** define what goes in and out of the API; **config** and **database** are set up at startup.

---

## 2. Request/Response Flow (Step by Step)

### One Request: `POST /teacher` with body `{"firstName":"Jane","lastName":"Doe","userName":"jdoe"}`

```
  Client
    │
    │  POST /teacher  +  JSON body
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  1. FastAPI receives the request                                         │
│     - Matches path/method to router (teacher_router.create_teacher)      │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  2. Dependency injection (like Spring’s constructor injection)           │
│     - FastAPI sees: db: AsyncSession = Depends(get_db)                   │
│     - It calls get_db() → yields one AsyncSession for this request       │
│     - Same idea as Spring giving you a @Transactional EntityManager     │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  3. Request body validation (like @Valid @RequestBody)                   │
│     - body: TeacherCreate → Pydantic parses JSON into TeacherCreate      │
│     - Validates fields (required, types); 422 if invalid                 │
│     - TeacherCreate uses alias: firstName → first_name, etc.              │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  4. Your handler runs                                                    │
│     - repo = TeacherRepository(db)                                       │
│     - entity = Teacher(first_name=body.first_name, ...)                   │
│     - return await repo.save(entity)                                      │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  5. Repository uses the session                                          │
│     - self._session.add(entity)                                          │
│     - await self._session.flush()  → INSERT, get ID                      │
│     - await self._session.refresh(entity)                                │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  6. get_db() finishes (after handler returns)                            │
│     - await session.commit()  → transaction committed                    │
│     - session closed                                                     │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  7. Response serialization (like HttpMessageConverter)                   │
│     - Handler returned Teacher (ORM model)                               │
│     - response_model=TeacherRead → FastAPI builds TeacherRead from       │
│       the entity (from_attributes=True) and serializes to JSON           │
│     - TeacherRead has serialize_by_alias=True → JSON uses firstName,     │
│       lastName, userName                                                 │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
  Client gets 200 + JSON { "id": 1, "firstName": "Jane", "lastName": "Doe", "userName": "jdoe" }
```

So: **Router** → **Depends(get_db)** → **Pydantic body** → **Repository** → **Session commit** → **Pydantic response model** → JSON. No separate “service” layer in this small app, but you’d add one the same way you do in Spring (controller → service → repository).

---

## 3. Compare & Contrast: Key Behaviors

### 3.1 Startup and “Application context”

- **Spring:** `SpringApplication.run()` loads `application.properties`, creates the “application context,” scans for `@Component` / `@Repository` / `@Service` / `@RestController`, creates beans, and wires them (e.g. injects `JpaRepository` into your controller).
- **This project:** `uvicorn` imports `school_service.main:app`. That runs `main.py`, which creates the `FastAPI` app, calls `init_db()` in the lifespan, and registers routers. There is no global “context” of beans; instead, **dependencies are resolved per request** via `Depends(get_db)` and (if you add them) `Depends(get_teacher_repository)` etc. So “wiring” is explicit and request-scoped.

### 3.2 Configuration

- **Spring:** `@Value("${spring.datasource.url}")` or `@ConfigurationProperties`. Properties come from `application.properties` / env / profiles.
- **This project:** `config.py` defines a Pydantic `Settings` class with `pydantic-settings`; it loads from `.env` and environment variables. You call `get_settings()` (or inject it with `Depends(get_settings)`) instead of `@Value`. One process-wide settings object, no profiles in this small app (you could add them via env vars or extra `.env` files).

### 3.3 Entities vs Models

- **Spring:** `@Entity` with `@Id`, `@GeneratedValue`, `@ManyToOne`, etc. Hibernate turns that into SQL and manages the session. Table/column names often derived from field names (e.g. snake_case).
- **This project:** SQLAlchemy **models** in `models/` with `Mapped[...]`, `mapped_column()`, `relationship()`. You define the table name explicitly (e.g. `__tablename__ = "class"`) and column names. No “session” in the controller; you pass `AsyncSession` from `get_db()` into repositories. So: **same idea** (ORM, entities ≈ models), **different API** (explicit session, no JpaRepository interface).

### 3.4 Repositories

- **Spring:** `interface ClassRepository extends JpaRepository<Class, Long>` — you get `findAll()`, `save()`, etc. for free. Spring generates implementation and injects it.
- **This project:** **Concrete classes** in `repositories/`, e.g. `ClassRepository(session)`. You implement `find_all()`, `save()` using `self._session.execute(select(...))`, `self._session.add()`, etc. So: **same role** (data access), **no interface** — just a class you instantiate with the request’s session.

### 3.5 Controllers vs Routers

- **Spring:** `@RestController` + `@GetMapping("/class")` etc. Method parameters: `@RequestBody`, `@PathVariable`, `@RequestParam`. Return type can be the entity or `ResponseEntity<T>`.
- **This project:** **Routers** in `routers/` with `@router.get("")`, `@router.post("")`, etc. Parameters: typed path/query params and a body type (e.g. `body: TeacherCreate`). Return type is the object; FastAPI uses `response_model=` to convert it to JSON. So: **same idea** (map HTTP to a function), with **explicit request/response models** (Pydantic) instead of raw entities.

### 3.6 Request/response bodies (DTOs vs Schemas)

- **Spring:** Often you use the same entity for request and response, or separate DTOs. Validation via `@Valid` and Bean Validation annotations.
- **This project:** **Pydantic schemas** in `schemas/`: e.g. `TeacherCreate` (request), `TeacherRead` (response). Validation is “parse JSON into this model”; if it fails, FastAPI returns 422. Response is built from the returned object using `response_model=TeacherRead` and `from_attributes=True` (so ORM → schema). So: **explicit input/output models** and **automatic validation/serialization** without Bean Validation.

### 3.7 Dependency injection and transaction scope

- **Spring:** `@Transactional` on service/controller or method. One transaction per request; repository uses the same transaction.
- **This project:** `get_db()` is a **dependency** that yields one `AsyncSession` per request. The router (and any repository it uses) gets that same session. After the handler returns, `get_db()` commits (or rolls back on exception) and closes the session. So: **one session ≈ one transaction per request**, similar to Spring’s default transactional request.

### 3.8 CORS and global config

- **Spring:** `@CrossOrigin` on controller or global CORS config in a `WebMvcConfigurer`.
- **This project:** `app.add_middleware(CORSMiddleware, ...)` in `main.py` with `allow_origins=["*"]` — same effect as per-controller `@CrossOrigin` for development.

---

## 4. Where Things Live in This Repo

```
src/school_service/
├── main.py              # FastAPI app, lifespan (init_db), CORS, router includes
├── config.py            # Settings from .env (like application.properties)
├── database.py          # Engine, session factory, get_db(), init_db()
├── models/               # SQLAlchemy entities (like @Entity)
├── schemas/              # Pydantic request/response (like DTOs + @Valid)
├── repositories/         # Data access (like JpaRepository impls, but explicit)
└── routers/              # HTTP endpoints (like @RestController)
```

So: **routers** = controllers, **repositories** = repository layer, **models** = entities, **schemas** = DTOs + validation, **config** + **database** = app and DB wiring. Once you map that, the flow (request → router → repo → session → commit → response schema → JSON) should feel familiar coming from Spring.
