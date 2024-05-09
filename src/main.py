from fastapi import FastAPI
from src.text.router import router as text_router
from src.pages.router import router as page_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/images'), name='static')
app.include_router(text_router)
app.include_router(page_router)
