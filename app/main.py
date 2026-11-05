from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import countries

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Инициализация базы данных...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Tourism API", version="0.1.0", lifespan=lifespan)

app.include_router(countries.router)

@app.get("/")
async def root():
    return {"status": "ok", "service": "tourism-api"}