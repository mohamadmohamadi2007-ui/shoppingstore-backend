# ShoppingStore Backend

FastAPI backend for the ShoppingStore project. See `docs/ROADMAP.md` and `docs/FastAPI-Roadmap.html` for the learning plan, and `../docs/` for product-level roadmap and decisions.

## Week 1 setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Postgres (not yet wired into the app, just getting it running)
docker compose up -d

# run the API
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
