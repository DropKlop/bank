from fastapi import APIRouter, HTTPException
from database import async_session
from repos.users_repos import UsersRepository
from schemas.users_schema import User

router = APIRouter(prefix="/user", tags=["Пользователь"])


@router.get("/me", description="получить информацию о себе")
async def get_about_user():
    async with async_session() as session:
        res = await UsersRepository(session).get_one_or_none()
        if res:
            return {"status":"OK", "data": res}
        raise HTTPException(status_code=404, detail="user not found")


@router.post("/auth")
async def auth_user():
    pass


@router.get("", description="получить всех пользователей")
async def get_all_users():
    async with async_session() as session:
        res = await UsersRepository(session).get_all()
        return {"status": "OK", "data": res}


@router.post("/register", description="регистрация нового пользователя")
async def register_user(user_data: User):
    async with async_session() as session:
        user = await UsersRepository(session).insert_data(user_data)
        await session.commit()
        return {"status": "OK", "new_data": user}


@router.delete("", description="удаление пользователя по ид")
async def delete_user(user_id: int):
    pass


@router.put("", description="полное обновление пользователя")
async def put_user(user_data: User):
    pass


@router.patch("", description="частичное обновление пользователя")
async def patch_user(user_data: User):
    pass
