# Backend Decisions Log

Records decisions made while building the backend, with date and reasoning. Product-level decisions (shared across repos) live in `../../docs/DECISIONS.md`.

## 2026-10-21 — Backend roadmap follows the personal FastAPI learning curriculum

The 20-week personal FastAPI curriculum (`docs/FastAPI-Roadmap.html`) is used
as the project's build order instead of a separate feature-driven roadmap.
Each curriculum week maps to a real Shopping Store feature (see
`docs/ROADMAP.md`) so the learning exercise and the production code are the
same artifact, not a throwaway.

**Why:** the goal of this repo is learning FastAPI from scratch, not just
shipping fastest. Reusing the curriculum's ordering also carries over its
AI-usage rule: weeks 1–9 are written by hand (no AI), weeks 10–20 are
AI-assisted with human review.

**Consequence:** the DB (started in Week 1) isn't actually wired into the
app with SQLAlchemy until Week 13 — Products/Orders live in-memory until
then. This is intentional, not an oversight.
