from fastapi import FastAPI
from src.text.router import router as text_router
from src.pages.router import router as page_router
from src.auth.base_config import fastapi_users, auth_backend
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/images'), name='static')
app.include_router(text_router)
app.include_router(page_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
