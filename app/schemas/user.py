from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    last_name: str
    phone_number: str
    ruc: str
    icargo_user: bool = False
    google_user: bool = False
    fb_user: bool = False
    apple_user: bool = False


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
