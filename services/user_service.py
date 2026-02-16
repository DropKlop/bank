from datetime import datetime, timezone, timedelta

import jwt
from fastapi import HTTPException, Response
from pydantic import EmailStr, BaseModel
from passlib.context import CryptContext

from database import Base
from services.base import BaseService
from schemas.users_schema import UserAdd, UserPatch, UserAuth, UserWithRoleAdd
from config import settings


class UserService(BaseService):
    password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.password_hash.hash(password)

    async def get_me(self, email: EmailStr):
        res = await self.db.user.get_one_or_none(email=email)
        return res

    async def get_all(self, limit, offset):
        res = await self.db.user.get_filtered(limit=limit, offset=offset)
        return res

    async def insert_data(self, data):
        user = await self.db.user.insert_data(data)
        await self.db.commit()
        return user

    async def delete_data(self, user_id: int):
        await self.db.user.delete_data(id=user_id)
        await self.db.commit()

    async def patch_data(self, user_id: int, data: UserPatch):
        await self.db.user.update_data(data, True, id=user_id)
        await self.db.commit()

    async def put_data(self, user_id: int, data: UserAdd):
        await self.db.user.update_data(data, False, id=user_id)
        await self.db.commit()

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        access_token = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": access_token})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    async def register_user(self, user_data: UserAdd) -> Base:
        hashed_pass = self.get_password_hash(user_data.password)
        user_data.password = hashed_pass
        data = await self.insert_data(data=user_data)
        try:
            user_role = UserWithRoleAdd(user_id=data.id, role="user")
            await self.db.user_role.insert_data(user_role)
            await self.db.commit()
        except Exception as e:
            print(f"{e=}")
        return data

    async def auth_user(self, user_data: UserAuth, response: Response):
        user = await self.get_me(email=user_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с такой почтой не найден")
        if not self.verify_password(user_data.password, user.password):
            raise HTTPException(status_code=401, detail="Указан неверный пароль")
        access_token = self.create_access_token({"id": user.id})
        response.set_cookie("current_session", access_token)
        return user

    async def logout(self, response: Response):
        response.delete_cookie("current_session")
