from pydantic import BaseModel
from sqlalchemy import select, insert, update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self):
        query = select(self.model)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_all(self):
        return await self.get_filtered()

    async def insert_data(self,data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        res = await self.session.execute(query)
        return res.scalars().one()

