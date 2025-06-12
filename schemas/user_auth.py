from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import constr


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6)

    first_name: constr(min_length=1, max_length=50)
    middle_name: Optional[str] = None
    last_name: Optional[str] = None

    mobile_number: Optional[constr(min_length=10, max_length=13)] = None

    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLogout(BaseModel):
    session_id: str