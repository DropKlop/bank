from services.base import BaseService

class UserService(BaseService):
    async def get_me(self):
        res = await self.db.user.get_one_or_none()
        return {"status": "OK", "data": res}
