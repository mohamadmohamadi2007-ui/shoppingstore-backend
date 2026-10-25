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

## 2026-10-24 — Schema v2 and API contract v1 confirmed

`docs/schema-v2-draft.html` and `docs/api-contract-v1-draft.html` are locked
as the table design and backend/frontend data contract (see product-level
`../../docs/DECISIONS.md` for the full note). The "-draft" filenames are kept
as-is so existing links don't break; "confirmed" status is tracked here, not
in the filename.

## 2026-10-26 — Step 20 auth: OTP stays mocked, JWT via PyJWT, Customer table added

Three choices made for the OTP/JWT authentication step:

- **OTP delivery is mocked for now.** No SMS gateway is wired up (that's
  step 25 — payment/courier/notification integrations are grouped there).
  `POST /auth/otp/request` generates and hashes (SHA-256) a 6-digit code with
  a 5-minute expiry, and echoes it back as `debug_otp` in the response body
  whenever `ENVIRONMENT != "production"`. This must be removed (or the
  `ENVIRONMENT` check must actually be set to `production`) before any real
  deploy — flagging it here so step 27 (security hardening pass) catches it
  if it's somehow missed.
- **JWT via PyJWT**, not `python-jose` — more actively maintained, no
  outstanding CVEs at the time of writing. Single access token (HS256,
  7-day expiry by default, configurable via `JWT_EXPIRE_MINUTES`), no
  refresh-token flow yet — not needed until there's a reason to shorten
  access-token lifetime, which isn't the case pre-launch.
- **`Customer` table added**, since none existed — `Order.customer_id` and
  `Cart.customer_id` were previously bare, unconstrained integers. Both now
  carry a real FK to `customer.id` (migration `eff697875deb`). Cart/Order
  creation still accept a client-supplied `customer_id` directly; wiring
  them to the authenticated identity from the JWT instead of a trusted
  client value is step 21's job (authorization/IDOR), not this one's.
