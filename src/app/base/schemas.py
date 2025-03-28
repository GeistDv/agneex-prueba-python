from typing import Optional

from fastapi import Body, Form
from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator
from .models import MsUser


class MsUserBase(BaseModel):
    microservice: Optional[str] = None


class MsUserBaseInDB(MsUserBase):
    id: int = None
    microservice: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

    class Config:
        from_attributes=True


class MsUserCreate(MsUserBaseInDB):
    microservice: str
    password: str


class MsUserCreateInRegistration(BaseModel):
    microservice: str
    password: str

    class Config:
        from_attributes=True


class MsUserUpdate(MsUserBaseInDB):
    password: Optional[str] = Form(...)


class MsUserInDB(MsUserBaseInDB):
    password: str


class MsUserPublic(MsUserBase):
    id: int

    class Config:
        from_attributes=True


MsUser_C_Pydantic = pydantic_model_creator(
    MsUser, name='create_MsUser', exclude_readonly=True, exclude=('is_active', 'is_staff', 'is_superuser'))
MsUser_G_Pydantic = pydantic_model_creator(MsUser, name='MsUser')