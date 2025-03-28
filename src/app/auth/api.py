from fastapi import BackgroundTasks

from fastapi import APIRouter,  Depends, HTTPException,  status, Header,Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from src.app.base import service, schemas

from .schemas import Token, Msg, TokenPayload
from .jwt import create_token
from .service import registration_ms_user,validate_token

from src.app.auth.jwt import decode_token


auth_router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login/access-token")


@auth_router.post("/registration", response_model=Msg)
async def ms_user_registration(new_microservice: schemas.MsUserCreateInRegistration):
    microservice = await registration_ms_user(new_microservice)
    if microservice:
        raise HTTPException(status_code=400, detail="Microservice already exists")
    else:
        return {"msg": "Microservice Created"}


@auth_router.post("/login/access-token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    microservice = await service.msuser_s.authenticate(microservice=form_data.username, password=form_data.password)
    if not microservice:
        raise HTTPException(status_code=400, detail="Incorrect microservice or password")
    elif not microservice.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return create_token(microservice.id)


@auth_router.get("/validate-token", response_model=TokenPayload)
async def validate_token(token: str = Depends(oauth2_scheme)):
    print(f"Token recibido: {token}")
    try:
        payload = decode_token(token)
        print(payload)
        return TokenPayload(**payload)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    
