from pydantic import BaseModel


class User(BaseModel):
    email: str | None
    full_name: str | None
