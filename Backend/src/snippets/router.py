from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from src.technology.model import TechnologyORM
from src.snippets.model import SnippetORM
from src.snippets.schemas import SnippetCreate, SnippetResponse
from src.snippets.enums import CategoryType
from src.core.dependencies import SessionDep
from src.snippets.repository import SnippetRepository
from src.core.config import settings

router = APIRouter(prefix='/snippets', tags=['Snippets'])

@router.post(path="/new_snippet", response_model=SnippetResponse, status_code=201)
async def create_snippet(
    snippet_data: SnippetCreate,
    db: SessionDep,
):
    stmt = select(SnippetORM).where(SnippetORM.title == snippet_data.title)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Запись уже существует")

    new_tech = SnippetORM(**snippet_data.model_dump())
    db.add(new_tech)
    await db.commit()
    await db.refresh(new_tech)
    return new_tech
    
@router.get(path="/", response_model=list[SnippetResponse])
async def get_snippets(
    db: SessionDep
):
    stmt = select(SnippetORM)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get(path="/{tech_id}", response_model=list[SnippetResponse])
async def get_snippets_by_technology(
    tech_id: int,
    db: SessionDep
):
    tech_exists_stmt = select(TechnologyORM.id).where(TechnologyORM.id == tech_id)
    tech_exists = await db.execute(tech_exists_stmt)
    
    if not tech_exists.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Технология не найдена")

    stmt = select(SnippetORM).where(SnippetORM.technology_id == tech_id)
    result = await db.execute(stmt)
    snippets = result.scalars().all()
    return snippets


@router.delete("/", status_code=200)
async def delete_all_technologies(db: SessionDep):
    repo = SnippetRepository(db)
    await repo.delete_all()
    return {"message": "Все технологии удалены"}

@router.delete("/{id}", status_code=204)
async def delete(tech_id: int, db: SessionDep):
    repo = SnippetRepository(db)
    await repo.delete(tech_id)