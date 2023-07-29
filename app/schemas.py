# schema modal
from datetime import datetime
from pydantic import BaseModel, EmailStr


# request
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# response
class Post(PostBase):
    id: int
    created_at: datetime

    # to tell it can be non dict data type response
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True