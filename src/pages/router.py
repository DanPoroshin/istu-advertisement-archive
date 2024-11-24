from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.text.models import Text
from src.db import get_async_session
from src.lingua.main import concordance
import asyncio

router = APIRouter(
    tags=['Pages'],
)

templates = Jinja2Templates(directory='src/templates')


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/text_details/{text_id}', response_class=HTMLResponse)
async def text_details(request: Request, text_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Text).where(Text.id == text_id)
    result = await session.execute(query)
    text = result.scalar()

    return templates.TemplateResponse('text_details.html', {'request': request, 'data': text})


@router.get('/all_texts', response_class=HTMLResponse)
async def all_texts(request: Request, session: AsyncSession = Depends(get_async_session)):
    query = select(Text)
    results = await session.execute(query)
    texts = results.scalars().unique().all()
    return templates.TemplateResponse("all_texts.html", {"request": request, "data": texts})


@router.get('/search_by_lemma', response_class=HTMLResponse)
async def search_by_lemmatized_text(request: Request, search_terms: str = Query(None, description="Comma-separated list of search terms"), session: AsyncSession = Depends(get_async_session)):
    texts = []
    if search_terms:
        terms = [term.strip() for term in search_terms.split(',')]
        query = select(Text).where(
            or_(*[Text.lemmatized_text.any(term) for term in terms])
        )
        results = await session.execute(query)
        texts = results.scalars().all()

    return templates.TemplateResponse("search_by_lemma.html", {"request": request, "texts": texts, "search_terms": search_terms})


@router.get('/add', response_class=HTMLResponse)
async def add(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


@router.get('/search_text', response_class=HTMLResponse)
async def search_in_text_field(request: Request, search_query: str = Query(None, description="Search query string"), session: AsyncSession = Depends(get_async_session)):
    texts = []
    concordances = []
    if search_query:
        search_pattern = f'%{search_query}%'
        target_word = search_query.split()[0]
        query = select(Text).where(Text.text.ilike(search_pattern))
        results = await session.execute(query)
        texts = results.scalars().all()

        # Create concordance coroutines for each text
        concordance_coroutines = [concordance(text.text, target_word) for text in texts]
        # Use asyncio.gather to run the coroutines concurrently
        concordances = await asyncio.gather(*concordance_coroutines)

        # Zip texts and concordances together before passing to the template
        text_concordance_pairs = list(zip(texts, concordances))
    else:
        text_concordance_pairs = []

    return templates.TemplateResponse("search_by_text.html", {
        "request": request,
        "text_concordance_pairs": text_concordance_pairs,
        "search_query": search_query
    })