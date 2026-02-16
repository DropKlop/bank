from fastapi import APIRouter, Response

from schemas.users_schema import UserAdd, UserPatch, UserAuth
from api.depencies import DBDep, PaginationDep
from services.user_service import UserService

router = APIRouter(prefix="/user", tags=["Пользователь"])




@router.get("/me", description="получить информацию о себе")
async def get_about_user(db: DBDep):
    pass
    #try:
        #return await UserService(db).get_me()
    #except:
       # raise HTTPException(status_code=404, detail="user not found")


@router.post("/register", description="регистрация нового пользователя")
async def register_user(user_data: UserAdd, db: DBDep):
    data = await UserService(db).register_user(user_data)
    return {"status": "OK", "data": data}


@router.post("/auth", description="Аутентификация пользователя по почте и паролю")
async def auth_user(user_data: UserAuth, db: DBDep, response: Response):
    user = await UserService(db).auth_user(user_data, response)
    return {"status":"OK", "data": user}


@router.post("/logout", description="Выход из сессии")
async def logout(response: Response):
    await UserService().logout(response)
    return {"status":"OK"}


@router.get("", description="получить всех пользователей")
async def get_all_users(pagination: PaginationDep, db: DBDep):
    per_page = pagination.per_page
    page = per_page * (pagination.page - 1)
    data = await UserService(db).get_all(limit=per_page, offset=page)
    return {"status": "OK", "data": data}


@router.delete("", description="удаление пользователя по айди")
async def delete_user(user_id: int, db: DBDep):
    await UserService(db).delete_data(user_id)
    return {"status": "OK"}


@router.put("/{user_id}", description="полное обновление пользователя")
async def put_user(user_id: int, user_data: UserAdd , db: DBDep):
    await UserService(db).put_data(user_id, user_data)
    return {"status": "OK"}


@router.patch("/{user_id}", description="частичное обновление пользователя")
async def patch_user(user_id: int, user_data: UserPatch , db: DBDep):
    await UserService(db).patch_data(user_id, user_data)
    return {"status": "OK"}
