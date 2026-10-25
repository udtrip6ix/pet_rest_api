from fastapi import FastAPI

app = FastAPI(title="Tourism API", version="0.1.0")

@app.get("/")
async def root():
    return {"status": "ok", "service": "tourism-api"}