from models.users_model import UserOrm
from repos.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UserOrm
