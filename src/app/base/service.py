from typing import Optional

from src.app.auth.security import verify_password, get_password_hash

from . import schemas, models
from ..base.service_base import BaseService


class MsUserService(BaseService):
    model = models.MsUser
    create_schema = schemas.MsUserCreateInRegistration
    update_schema = schemas.MsUserUpdate
    get_schema = schemas.MsUser_G_Pydantic

    async def create_msuser(self, schema: schemas.MsUserCreateInRegistration, **kwargs):
        hash_password = get_password_hash(schema.model_dump().pop("password"))
        return await self.create(
            schemas.MsUserCreateInRegistration(
                **schema.model_dump(exclude={"password"}), password=hash_password, **kwargs
            )
        )

    async def authenticate(self, microservice: str, password: str) -> Optional[models.MsUser]:
        msuser = await self.model.get(microservice=microservice)
        if not msuser:
            return None
        if not verify_password(password, msuser.password):
            return None
        return msuser

    async def change_password(self, obj: models.MsUser, new_password: str):
        hashed_password = get_password_hash(new_password)
        obj.password = hashed_password
        await obj.save()

    async def create_supermsuser(self, schema: schemas.MsUserCreateInRegistration):
        hash_password = get_password_hash(schema.model_dump().pop("password"))
        return await self.create(
            schemas.MsUserCreate(
                **schema.model_dump(exclude={"password"}),
                password=hash_password,
                is_active=True,
                is_superMsUser=True,
            )
        )


msuser_s = MsUserService()