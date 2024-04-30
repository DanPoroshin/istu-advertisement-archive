from fastapi import APIRouter, Depends, status, HTTPException
from src.text.schemas import BaseTextDTO, TextDTO, TextUpdateDTO
from src.text.models import Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from src.security.main import verification

from src.db import get_async_session

router = APIRouter(
    prefix='/text',
    tags=['Text'],
)

@router.post('/add', status_code=200)
async def add_text(text_dto: BaseTextDTO, auth: bool = Depends(verification), session: AsyncSession = Depends(get_async_session)):
    if auth:
        text_model = Text(
            title=text_dto.title,
            text=text_dto.text,
            kirillic_text=text_dto.kirillic_text,
            image=text_dto.image,
            comment=text_dto.comment,
        )
        session.add(text_model)
        await session.commit()

        return {"status": "200"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)