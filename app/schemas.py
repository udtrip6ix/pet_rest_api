from pydantic import BaseModel, Field

class CountryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    iso_code: str = Field(..., min_length=2, max_length=2, description="Двухбуквенный код (RU, TR, EG)")

class CountryCreate(CountryBase):
    pass
class CountryResponse(CountryBase):
    id: int

    class Config:
        from_attributes = True