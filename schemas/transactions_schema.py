from pydantic import BaseModel, EmailStr, Field



class UserAdd(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class User(UserAdd):
    id: int

class UserPatch(BaseModel):
    email: EmailStr | None = Field(None)
    full_name: str | None = Field(None)
    password: str | None = Field(None)

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserWithRoleAdd(BaseModel):
    user_id: int
    role: str

class UserWithRole(UserWithRoleAdd):
    id: int
