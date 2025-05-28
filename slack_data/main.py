from contextlib import asynccontextmanager
from fastapi import FastAPI

from slack_data.database import create_db_and_tables
from slack_data.api.routers.webbing_router import webbing_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # cleanup goes here

app = FastAPI(lifespan=lifespan)

app.include_router(webbing_router)

@app.get("/")
def root():
    return {"message": "Welcome to SlackData"}


