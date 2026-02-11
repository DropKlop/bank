from typing import Annotated

from db_manager import DBManager
from fastapi import Depends

from database import async_session


def get_db_manager():
    return DBManager(session_factory=async_session)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]