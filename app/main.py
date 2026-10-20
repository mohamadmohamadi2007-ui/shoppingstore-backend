from fastapi import FastAPI

app = FastAPI(title="ShoppingStore Backend")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/hello_world")
def health() -> dict[str, str]:
    return {
        "message": "Hello Mohammad"
        }
