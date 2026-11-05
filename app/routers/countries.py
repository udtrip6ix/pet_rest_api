from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import Country
from app.schemas import CountryCreate, CountryResponse

router = APIRouter(prefix="/countries", tags=["Countries"])

@router.post("/", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
async def create_country(country_in: CountryCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).where(Country.iso_code == country_in.iso_code))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Страна с таким ISO-кодом уже существует")
    
    new_country = Country(**country_in.model_dump())
    db.add(new_country)
    await db.commit()
    await db.refresh(new_country)
    
    return new_country

@router.get("/", response_model=List[CountryResponse])
async def get_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country))
    countries = result.scalars().all()
    return countries

@router.get("/{country_id}", response_model=CountryResponse)
async def get_country(country_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    return country

@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(country_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    
    await db.delete(country)
    await db.commit()
    return None