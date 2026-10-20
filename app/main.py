from fastapi import FastAPI

app = FastAPI(title="ShoppingStore Backend")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
