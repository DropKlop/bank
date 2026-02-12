from models.users_model import UserOrm
from repos.base import BaseRepository

from sqlalchemy import select


class UsersRepository(BaseRepository):
    model = UserOrm

    async def get_filtered(self, limit: int, offset: int,  **filter_by):
        query = (select(self.model)
                 .filter_by(**filter_by)
                 .limit(limit)
                 .offset(offset)
                 )
        res = await self.session.execute(query)
        return res.scalars().all()

