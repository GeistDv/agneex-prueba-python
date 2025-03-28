from fastapi import BackgroundTasks,HTTPException
import jwt
from datetime import datetime, timedelta
from typing import Optional

from src.config import settings

from src.app.base import schemas, service, models
from .models import Verification
from .schemas import VerificationOut

password_reset_jwt_subject = "preset"


async def registration_ms_user(new_ms_user: schemas.MsUserCreateInRegistration) -> bool:
    # if await models.MsUser.filter(username=new_ms_user.microservice).exists():
    if await models.MsUser.filter(microservice=new_ms_user.microservice).exists():


        return True
    else:
        user = await service.msuser_s.create_msuser(new_ms_user)
        return False


async def verify_registration_user(uuid: VerificationOut) -> bool:
    verify = await Verification.get(link=uuid.link).prefetch_related("user")
    if verify:
        await service.msuser_s.update(schema=schemas.MsUserBaseInDB(is_active=True), id=verify.user.id)
        await Verification.filter(link=uuid.link).delete()
        return True
    else:
        return False


def generate_password_reset_token(email: str):
    delta = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": password_reset_jwt_subject, "email": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
        return None

def validate_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token  
    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Token inválido")
