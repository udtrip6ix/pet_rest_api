from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, get_db
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("старт бд")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Tourism API", version="0.1.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok", "service": "tourism-api"}

@app.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT version()"))
    pg_version = result.scalar()
    return {
        "status": "connected",
        "database": "PostgreSQL",
        "version": pg_version
    }