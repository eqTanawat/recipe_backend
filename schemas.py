import datetime as _dt
from typing import Optional, List
import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    username: str
    email: str

class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        from_attributes=True

class User(_UserBase):
    id: int

    class Config:
        from_attributes=True



class _UserProfile(_pydantic.BaseModel):
    location: str
    status1: str
    status2: str
    name: str
    surname: str
    nickname: str
    phone: str
    gender: str
    birth: str

class UserProfileCreate(_UserProfile):
    pass

class UserProfile(_UserProfile):
    owner_username: str
    owner_email: str
    date_last_updated: _dt.datetime

    class Config:
        from_attributes = True
    


class _RecipeBase(_pydantic.BaseModel):
    recipe_name: str
    ingredients: str
    steps: str

class RecipeCreate(_RecipeBase):
    pass

class Recipe(_RecipeBase):
    recipe_id: int
    owner_username: str
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        from_attributes=True


# class UserProfile(_pydantic.BaseModel):
#     owner_username: str
#     owner_email: str
#     location: str
#     status1: str
#     status2: str
#     name: str
#     surname: str
#     nickname: str
#     phone: str
#     gender: str
#     birth: str
#     date_last_updated: _dt.datetime

#     class Config:
#         from_attributes=True