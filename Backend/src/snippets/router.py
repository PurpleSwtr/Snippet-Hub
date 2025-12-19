from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from src.snippets.enums import CategoryType
from src.snippets.schemas import OptionCreate, OptionPrompt, OptionRead, OptionResponse
from src.core.dependencies import get_db
from src.snippets.model import OptionType, PromptOptionORM

from src.core.config import settings

router = APIRouter(prefix='/options', tags=['Options'])

@router.get(path="/options", response_model=list[OptionRead])
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.options_list) 
async def get_options(
    option_type: OptionType,
    category: CategoryType | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(PromptOptionORM).filter(PromptOptionORM.option_type == option_type)
    if category:
        query = query.filter(PromptOptionORM.category == category)
    return query.all()

@router.get(path="/option/{id}")
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.options_list) 
async def get_option(
    id: int,
    db: Session = Depends(get_db)
):
    query = db.query(PromptOptionORM).filter(PromptOptionORM.id == id)
    return query.scalar()

@router.post("/", response_model=OptionResponse, status_code=status.HTTP_201_CREATED)
def create_option(
    option_data: OptionCreate,
    db: Session = Depends(get_db)
):
    db_option = PromptOptionORM(**option_data.model_dump())
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option

@router.get("/prompt", response_model=list[OptionPrompt])
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.options_list) 
async def get_full_prompt(
    options: list[int] = Query(...),
    db: Session = Depends(get_db)
):
    query = db.query(PromptOptionORM).filter(PromptOptionORM.id.in_(options))
    return query.all()

@router.get("/option_types")
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.options_list)
async def get_option_types():
    """Список доступных типов опций"""
    return [option_type.value for option_type in OptionType]

@router.get("/category_types")
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.options_list)
async def get_category_types():
    """Список доступных категорий"""
    return [category.value for category in CategoryType]