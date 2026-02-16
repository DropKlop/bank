from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return self.schema.model_validate(res.scalars().one_or_none(), from_attributes=True)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return self.schema.model_validate(res.scalars().one(), from_attributes=True)

    async def get_filtered(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return [self.schema.model_validate(row, from_attributes=True) for row in res.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def insert_data(self,data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        res = await self.session.execute(query)
        return self.schema.model_validate(res.scalars().one(), from_attributes=True)

    async def delete_data(self, **filter_by):
        query = delete(self.model).filter_by(**filter_by)
        await self.session.execute(query)

    async def update_data(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(query)
