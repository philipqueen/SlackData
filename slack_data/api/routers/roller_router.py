from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Path
from sqlmodel import select

from slack_data.database import SessionDep
from slack_data.models.rollers import Roller, RollerCreate, RollerPublic, RollerUpdate

roller_router = APIRouter(
    prefix="/roller",
    tags=["roller"],
    responses={404: {"description": "Not found"}}
)

@roller_router.post("/", response_model=RollerPublic)
def create_roller(roller: RollerCreate, session: SessionDep):
    db_roller = Roller.model_validate(roller)
    session.add(db_roller)
    session.commit()
    session.refresh(db_roller)
    return db_roller

@roller_router.get("/", response_model=list[RollerPublic])
def read_rollers(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    heroes = session.exec(
        select(Roller).offset(offset).limit(limit)
    ).all()
    return heroes

@roller_router.get("/{roller_id}", response_model=RollerPublic)
def read_roller(roller_id: Annotated[int, Path(gt=0)], session: SessionDep):
    roller = session.get(Roller, roller_id)
    if not roller:
        raise HTTPException(status_code=404, detail=f"roller {roller_id} not found")
    return roller

@roller_router.patch("/{roller_id}", response_model=RollerPublic)
def update_roller(
    roller_id: Annotated[int, Path(gt=0)],
    roller: RollerUpdate,
    session: SessionDep
):
    db_roller = session.get(Roller, roller_id)
    if not db_roller:
        raise HTTPException(status_code=404, detail=f"roller {roller_id} not found")
    
    roller_data = roller.model_dump(exclude_unset=True)
    for key, value in roller_data.items():
        setattr(db_roller, key, value)
    
    session.add(db_roller)
    session.commit()
    session.refresh(db_roller)
    return db_roller

@roller_router.delete("/{roller_id}")
def delete_roller(roller_id: Annotated[int, Path(gt=0)], session: SessionDep):
    db_roller = session.get(Roller, roller_id)
    if not db_roller:
        raise HTTPException(status_code=404, detail=f"roller {roller_id} not found")
    
    session.delete(db_roller)
    session.commit()
    return {"ok": True}
