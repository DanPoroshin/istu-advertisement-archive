from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List
from src.db import get_async_session, Base
from src.text.router import router as text_router

app = FastAPI()

app.include_router(text_router)


