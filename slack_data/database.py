from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

DATABASE_ENGINE: Optional[Engine] = None


def create_db_and_tables():
    global DATABASE_ENGINE
    if DATABASE_ENGINE is not None:
        raise RuntimeError("`create_db_and_tables` called, but database already created.")
    DATABASE_ENGINE = create_engine(
        sqlite_url, connect_args=connect_args, echo=True
    )
    SQLModel.metadata.create_all(DATABASE_ENGINE)


def get_session():
    global DATABASE_ENGINE
    if DATABASE_ENGINE is None:
        raise RuntimeError("Database engine not created. Call `create_db_and_tables` first.")
    with Session(DATABASE_ENGINE) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
