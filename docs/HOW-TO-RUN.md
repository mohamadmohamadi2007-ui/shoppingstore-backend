# How to Run the Project

## 1. Activate the virtual environment
```bash
source .venv/bin/activate
```

## 2. Install dependencies (only needed if requirements.txt changed)
```bash
pip install -r requirements.txt
```

## 3. Start Postgres (Docker)
```bash
docker compose up -d
```
Check it's running: `docker compose ps`

## 4. Run the API
```bash
uvicorn app.main:app --reload
```

## 5. Verify
- Health check: http://127.0.0.1:8000/health
- Interactive docs: http://127.0.0.1:8000/docs

## Stop
```bash
docker compose down   # stops Postgres
# Ctrl+C                stops uvicorn
```
