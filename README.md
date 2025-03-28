# 🚀 Proyecto Agneex - Configuración y Ejecución

## 📌 Requisitos previos
Antes de iniciar, asegúrate de tener instalado **uv** para la gestión del entorno virtual.

### 🔹 Instalación de `uv`
Ejecuta el siguiente comando en PowerShell:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Se recomienda usar la versión **0.6.10**.

### 🔹 Creación y activación del entorno virtual
```powershell
uv venv nombre_de_tu_entorno
nombre_de_tu_entorno\Scripts\activate
```

## 📦 Instalación de dependencias
Antes de instalar los requerimientos, **elimina `uvloop` del archivo `requirements.txt`** para evitar problemas.

```powershell
uv pip install -r requirements.txt
```
Si encuentras errores, instala las siguientes librerías de manera manual:
```powershell
uv pip install passlib
uv pip install tortoise-orm
uv pip install itsdangerous
uv pip install bcrypt
uv pip install pyjwt
uv pip install tomlkit
```

## 🔧 Modificaciones necesarias

### 🔹 Modificación en `main.py`
Para asegurar el correcto funcionamiento, se agregó la siguiente línea:
```python
if __name__ == "__main__":
    print("🔥 Servidor corriendo en http://127.0.0.1:8000")  
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

Además, se actualizaron las importaciones:
**Antes:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import RegisterTortoise, tortoise_exception_handlers
from dotenv import load_dotenv
from src.config import settings
from src.app import routers
import logging.config
```

**Después:**
```python
import logging.config
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
from src.config import settings
from src.app import routers
```

### 🔹 Modificación en `schemas.py` (dentro de `base`)
Cambia la siguiente línea:
```python
orm_mode = True
```
por esta:
```python
from_attributes = True
```
Esto se debe a la compatibilidad con **Pydantic v2**.

### 🔹 Modificación en `service.py` (dentro de `auth`)
Reemplaza:
```python
if await models.MsUser.filter(username=new_ms_user.microservice).exists():
```
por esta línea:
```python
if await models.MsUser.filter(microservice=new_ms_user.microservice).exists():
```
`username` no existe en `MsUser`, pero `microservice` sí es un campo válido.

### 🔹 Modificación en la tabla `msuser`
Si el estado de tu microservicio está inactivo (`is_active = FALSE`), usa esta consulta para activarlo:
```sql
UPDATE msuser SET is_active = TRUE WHERE microservice = 'nombre_del_microservicio';
```
Si `is_active` está en `FALSE`, **no se podrá generar el `access_token` correctamente**.

🔹 Modificación del modelo MsUser
El modelo MsUser fue modificado para que el campo is_active siempre sea True por defecto, asegurando que los otros endpoints funcionen correctamente.

class MsUser(models.Model):
    microservice = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100)
    date_join = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)  # Modificado
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)


🔧 Comandos para migraciones
Para correr las migraciones, usa los siguientes comandos:

aerich init -t src.config.tortoise_conf.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade

📂 Archivos adicionados en la rama develop
En la rama develop, se adicionaron los siguientes archivos:

Un test

Un archivo pyproject.toml

Un archivo uv.lock

La carpeta migrations

Esto se realizó debido a problemas con el entorno virtual para correr las migraciones y ejecutar el proyecto. Por lo tanto, se separaron los proyectos para mostrar de manera funcional la prueba.
---

✅ **Con estos pasos, tu aplicación estará lista para ejecutarse correctamente.** 🚀

