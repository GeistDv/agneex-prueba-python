import os

PROJECT_NAME = ""
SERVER_HOST = os.environ.get("")

SECRET_KEY = "a9f3d6e2b7c8d1f4e5a6b9c3d7f2e0a4b1f3e7c8a2d4e5b9c3d7f2b6a8e9d1"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_V1_STR = "/api/v1"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
]

DATABASE_URI = f'postgres://{os.environ.get("DB_USER","postgres")}:' \
               f'{os.environ.get("DB_PASSWORD","admin")}@' \
               f'{os.environ.get("DB_HOST","localhost")}:' \
               f'{os.environ.get("DB_PORT","5433")}/' \
               f'{os.environ.get("DB_NAME","agneex")}'


APPS_MODELS = [
    "src.app.auth.models",
    "src.app.base.models",
    "aerich.models",
]
