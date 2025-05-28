from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class BaseWebbing(SQLModel):
    """
    Base class for webbing version.
    """
    name: str = Field(index=True)
    brand: str = Field(index=True)
    release_date: str | None = None
    material: str # TODO: Will Enum work here? List of Enums?
    width: int
    weight: int | None = None # g/m
    breaking_strength: float | None = None # kN
    stretch: str | None = None # like [{"kn":0, "percent": 0.0}, {"kn": 10, "percent": 14.97}]
    isa_certified: bool = False
    classification: str | None = None # TODO: Enum for type A+, A, B, C
    colors: str | None = None # Comma separated list of colors
    description: str | None = None
    notes: str | None = None

class Webbing(BaseWebbing, table=True):
    id: int | None = Field(default=None, primary_key=True)

class WebbingCreate(BaseWebbing):
    """
    Model for creating a new webbing entry.
    """
    pass

class WebbingUpdate(BaseWebbing):
    """
    Model for updating an existing webbing entry.
    """
    pass


    