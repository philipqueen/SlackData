from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Path
from sqlmodel import select

from slack_data.database import SessionDep
from slack_data.models.webbing import Webbing, WebbingCreate, WebbingUpdate

webbing_router = APIRouter(
    prefix="/webbing",
    tags=["webbing"],
    responses={404: {"description": "Not found"}}
)

@webbing_router.post("/", response_model=Webbing)
def create_webbing(webbing: WebbingCreate, session: SessionDep):
    db_webbing = Webbing.model_validate(webbing)
    session.add(db_webbing)
    session.commit()
    session.refresh(db_webbing)
    return db_webbing

@webbing_router.get("/", response_model=list[Webbing])
def read_webbings(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    heroes = session.exec(
        select(Webbing).offset(offset).limit(limit)
    ).all()
    return heroes

@webbing_router.get("/{webbing_id}", response_model=Webbing)
def read_webbing(webbing_id: Annotated[int, Path(gt=0)], session: SessionDep):
    webbing = session.get(Webbing, webbing_id)
    if not webbing:
        raise HTTPException(status_code=404, detail=f"Webbing {webbing_id} not found")
    return webbing

@webbing_router.patch("/{webbing_id}", response_model=Webbing)
def update_webbing(
    webbing_id: Annotated[int, Path(gt=0)],
    webbing: WebbingUpdate,
    session: SessionDep
):
    db_webbing = session.get(Webbing, webbing_id)
    if not db_webbing:
        raise HTTPException(status_code=404, detail=f"Webbing {webbing_id} not found")
    
    webbing_data = webbing.model_dump(exclude_unset=True)
    for key, value in webbing_data.items():
        setattr(db_webbing, key, value)
    
    session.add(db_webbing)
    session.commit()
    session.refresh(db_webbing)
    return db_webbing

@webbing_router.delete("/{webbing_id}")
def delete_webbing(webbing_id: Annotated[int, Path(gt=0)], session: SessionDep):
    db_webbing = session.get(Webbing, webbing_id)
    if not db_webbing:
        raise HTTPException(status_code=404, detail=f"Webbing {webbing_id} not found")
    
    session.delete(db_webbing)
    session.commit()
    return {"ok": True}
