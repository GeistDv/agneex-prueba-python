import logging.config
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
from src.config import settings
from src.app import routers

load_dotenv()

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

print("🚀 Iniciando aplicación FastAPI...")  
app = FastAPI(
    title="Agneex",
    description="Author - Jaime Alberto Martínez",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


app.include_router(routers.api_router, prefix=settings.API_V1_STR)


register_tortoise(
    app,
    db_url=settings.DATABASE_URI,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    print("🔥 Servidor corriendo en http://127.0.0.1:8000")  
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
