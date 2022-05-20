#This file specifies the request/response schemas

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class CreateUser(BaseModel):
    """
    Inherits from BaseModel of Pydantic
    """
    email: EmailStr
    password: str

class UserResponse(BaseModel):

    """
    Using BaseModel as we don't need the password to be sent back
    """
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):

    email: EmailStr
    password: str

class PostBase(BaseModel):
    """
    Inherits from BaseModel of Pydantic
    """
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class PostResponse(PostBase):

    """
    When using with SQLAlchemy use the class Config with orm_mode set to True
    """
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostVotes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)