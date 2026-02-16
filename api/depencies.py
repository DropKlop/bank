from typing import Annotated

from pydantic import BaseModel

from db_manager import DBManager
from fastapi import Depends, Query

from database import async_session

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(3, ge=1)]

PaginationDep = Annotated[PaginationParams, Depends()]

def get_db_manager():
    return DBManager(session_factory=async_session)

async def get_db():
    async with get_db_manager() as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]