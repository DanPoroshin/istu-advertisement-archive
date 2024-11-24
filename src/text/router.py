import os
from pathlib import Path
import shutil
import uuid
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form, Query

from src.text.schemas import BaseTextDTO, TextDTO, TextUpdateDTO
from src.text.models import Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, func, or_
from typing import List
from src.db import get_async_session
from src.lingua.main import lemmatize

router = APIRouter(
    prefix='/text',
    tags=['Text'],
)


@router.post('/add', status_code=201)
async def add_text(title_: str = Form(...),
                   text_: str = Form(...),
                   kirillic_text_: str = Form(None),
                   comment_: str = Form(...),
                   image_: UploadFile = File(),
                   session: AsyncSession = Depends(get_async_session)):

    # Create the directory if it doesn't exist
    images_dir = Path('src/images')
    images_dir.mkdir(parents=True, exist_ok=True)

    try:
        filename = f"{uuid.uuid4()}.{image_.filename.split('.')[-1]}"

        with (images_dir / filename).open('wb') as buffer:
            shutil.copyfileobj(image_.file, buffer)

        lemmatized_text = await lemmatize(kirillic_text_)
        text_model = Text(
            title=title_,
            text=text_.lower(),
            kirillic_text=kirillic_text_.lower(),
            lemmatized_text=lemmatized_text,
            image=filename,
            comment=comment_,
        )
        session.add(text_model)

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='There was an error uploading your image.')

    finally:
        await session.commit()

        return {'response': HTTPException(status_code=status.HTTP_200_OK)}


@router.get('/all', response_model=List[BaseTextDTO])
async def all(session: AsyncSession = Depends(get_async_session)):
    query = select(Text)
    results = await session.execute(query)

    texts = results.scalars().unique().all()
    return texts


@router.get('/{text_id}', response_model=TextDTO)
async def get_text(text_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Text).where(Text.id == text_id)
    result = await session.execute(query)
    text = result.scalar()
    return text


@router.get('/search_by_lemma/', response_model=List[BaseTextDTO])
async def search_by_lemmatized_text(
    search_terms: str = Query(...,
                              description="Comma-separated list of search terms"),
    session: AsyncSession = Depends(get_async_session)
):
    # Split the search_terms into a list of words
    terms = [term.strip() for term in search_terms.split(',')]

    # Build a query that uses an OR condition to check each term against the lemmatized_text array
    query = select(Text).where(
        or_(*[Text.lemmatized_text.any(term) for term in terms])
    )
    results = await session.execute(query)

    return results.scalars().all()


@router.get('/search_text/', response_model=List[BaseTextDTO])
async def search_in_text_field(
    search_query: str = Query(..., description="Search query string"),
    session: AsyncSession = Depends(get_async_session)
):
    # Construct the search pattern
    search_pattern = f'%{search_query}%'

    # Build a query that uses the ilike operator for case-insensitive pattern matching
    query = select(Text).where(Text.text.ilike(search_pattern))
    results = await session.execute(query)

    return results.scalars().all()
