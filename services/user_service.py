from services.base import BaseService
from schemas.users_schema import UserAdd, UserPatch


class UserService(BaseService):
    async def get_me(self):
        res = await self.db.user.get_one()
        return {"status": "OK", "data": res}

    async def get_all(self, limit, offset):
        res = await self.db.user.get_filtered(limit=limit, offset=offset)
        return {"status": "OK", "data": res}

    async def insert_data(self, data: UserAdd):
        user = await self.db.user.insert_data(data)
        await self.db.commit()
        return {"status": "OK", "new_data": user}

    async def delete_data(self, user_id: int):
        await self.db.user.delete_data(id=user_id)
        await self.db.commit()

    async def patch_data(self, user_id: int, data: UserPatch):
        await self.db.user.update_data(data, True, id=user_id)
        await self.db.commit()

    async def put_data(self, user_id: int, data: UserAdd):
        await self.db.user.update_data(data, False, id=user_id)
        await self.db.commit()
