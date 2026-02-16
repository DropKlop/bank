from models.users_model import UserOrm, UserRoleOrm
from repos.base import BaseRepository

from sqlalchemy import select

from schemas.users_schema import User, UserWithRole


class UsersRepository(BaseRepository):
    model = UserOrm
    schema = User

    async def get_filtered(self, limit: int, offset: int,  **filter_by):
        query = (select(self.model)
                 .filter_by(**filter_by)
                 .limit(limit)
                 .offset(offset)
                 )
        res = await self.session.execute(query)
        return res.scalars().all()

class UsersRoleRepository(BaseRepository):
    model = UserRoleOrm
    schema = UserWithRole
