import jwt
from datetime import datetime, timedelta, timezone

from src.config import settings

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_token(user_id: int):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload decodificado:", decoded_payload)  # 🔍 DEBUG
        user_id = decoded_payload.get("user_id")
        if user_id is None:
            raise Exception("El token no contiene user_id")
        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise Exception("Token ha expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")


