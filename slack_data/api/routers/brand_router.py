from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Path
from sqlmodel import select

from slack_data.database import SessionDep
from slack_data.models.brands import Brand, BrandCreate, BrandPublic, BrandUpdate

brand_router = APIRouter(
    prefix="/brand",
    tags=["brand"],
    responses={404: {"description": "Not found"}}
)

@brand_router.post("/", response_model=BrandPublic)
def create_brand(brand: BrandCreate, session: SessionDep):
    db_brand = Brand.model_validate(brand)
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand

@brand_router.get("/", response_model=list[BrandPublic])
def read_brands(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    heroes = session.exec(
        select(Brand).offset(offset).limit(limit)
    ).all()
    return heroes

@brand_router.get("/{brand_id}", response_model=BrandPublic)
def read_brand(brand_id: Annotated[int, Path(gt=0)], session: SessionDep):
    brand = session.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail=f"brand {brand_id} not found")
    return brand

@brand_router.patch("/{brand_id}", response_model=BrandPublic)
def update_brand(
    brand_id: Annotated[int, Path(gt=0)],
    brand: BrandUpdate,
    session: SessionDep
):
    db_brand = session.get(Brand, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail=f"brand {brand_id} not found")
    
    brand_data = brand.model_dump(exclude_unset=True)
    for key, value in brand_data.items():
        setattr(db_brand, key, value)
    
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand

@brand_router.delete("/{brand_id}")
def delete_brand(brand_id: Annotated[int, Path(gt=0)], session: SessionDep):
    db_brand = session.get(Brand, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail=f"brand {brand_id} not found")
    
    session.delete(db_brand)
    session.commit()
    return {"ok": True}
