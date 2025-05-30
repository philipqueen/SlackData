from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import select, text

from slack_data.database import get_session, create_db_and_tables
from slack_data.load_webbings import load_webbings
from slack_data.api.routers.webbing_router import webbing_router
from slack_data.models.webbing import Webbing



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with next(get_session()) as session:
        existing_webbings = session.exec(select(Webbing)).first()
        if existing_webbings is None: # Only load from `webbings.json` if the database is empty
            print("Loading webbing data into the database...")
            load_webbings(session=session)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(webbing_router)

@app.get("/")
def root():
    return {"message": "Welcome to SlackData"}


