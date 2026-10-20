# Backend Roadmap

This roadmap maps the 20-week personal FastAPI learning curriculum
(`docs/FastAPI-Roadmap.html`) onto building the real Shopping Store backend.
Each week of the curriculum becomes a concrete piece of this project —
the "exercise" is never a toy, it's the next slice of the real API.

Curriculum rule carries over: **Weeks 1–9 — no AI, you write the code.
Weeks 10–20 — AI can write it, you review it.**

## Status
- ✅ Week 1 — done (committed `642b0cb`)
- ▶ Week 2 — next

## Phase 0 — Foundations (Weeks 1–4, no AI)

- **Week 1 · Environment & Python** — ✅ Done. FastAPI skeleton, Docker
  Compose Postgres container, venv, `/health` endpoint, env-based DB
  credentials.
- **Week 2 · Git & Teamwork** — Practice the branch → PR → merge workflow
  on this repo: create a feature branch, make a small real change (e.g. a
  `/version` endpoint), open a PR, merge it. Document the branching
  convention in `DECISIONS.md`.
- **Week 3 · How the Web Works** — Inspect the request/response cycle by
  hand with `curl -v` against `/health` (headers, status codes, methods)
  before adding any new routes.
- **Week 4 · Your First Endpoint** — Build the first real domain endpoint
  by hand: `GET /products` returning a hardcoded in-memory list (no DB
  yet — that comes in Week 13).
- 🏁 Phase 0 self-check after Week 4.

## Phase 1 — Writing It Ourselves (Weeks 5–9, no AI)

- **Week 5 · Pydantic & Input** — Define `ProductCreate` / `ProductUpdate`
  Pydantic schemas with validation for `POST /products`.
- **Week 6 · Full CRUD** — Full in-memory CRUD for Products (Create, Read,
  Update, Delete) — still no DB, the goal is FastAPI routing fluency.
- **Week 7 · Responses & Data Leaks** — Separate input vs. output schemas
  with `response_model` (e.g. hide internal cost price, expose only sale
  price).
- **Week 8 · Errors & Status Codes** — Proper `HTTPException` handling:
  404 for missing product, 422 for bad input, consistent error shape.
- **Week 9 · The Client Contract** — Consistent response envelope,
  pagination, and a stable API contract for the Products endpoint.
- 🏁 Review exam #1 after Week 9.

## Phase 2 — Structure & Data (Weeks 10–15, AI reviews)

- **Week 10 · Testing** — pytest + `TestClient` tests for the Products API.
- **Week 11 · Layering & Refactor** — Split `main.py` into
  `app/api/`, `app/services/`, `app/schemas/`.
- **Week 12 · DI & Resource Lifecycle** — `Depends()` for DB sessions and
  settings/config injection.
- **Week 13 · SQLAlchemy & Data Model** — Replace the in-memory Products
  store with real SQLAlchemy models backed by the Postgres container
  from Week 1 — first real DB wiring.
- **Week 14 · N+1 & Transactions** — Add Orders/OrderItems relations,
  fix N+1 queries, wrap checkout in a DB transaction.
- **Week 15 · Migrations & Secrets** — Introduce Alembic migrations;
  formalize secrets handling (building on the `.env` pattern already set
  up in Week 1).
- 🏁 Review exam #2 after Week 15.

## Phase 3 — Behaviour Under Pressure (Weeks 16–20, AI reviews)

- **Week 16 · Authentication** — JWT auth: register/login, password
  hashing.
- **Week 17 · Authorization & IDOR** — Role-based access (customer vs.
  admin/panel), prevent users from accessing other customers' orders.
- **Week 18 · Concurrency** — Safe concurrent stock decrement during
  checkout (race condition handling).
- **Week 19 · Background & Idempotency** — Background tasks for order
  notifications; idempotent checkout/payment endpoint. Natural landing
  spot for the Phase 2 product feature: customer support ticketing.
- **Week 20 · Observability & Performance** — Logging, basic metrics,
  performance pass before wrapping the curriculum.

## See also
- `DECISIONS.md` — reasoning behind choices made along the way.
- `HOW-TO-RUN.md` — how to run the project locally.
- `FastAPI-Roadmap.html` — the full personal learning curriculum this
  roadmap is built on.
