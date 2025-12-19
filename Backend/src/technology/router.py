from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from src.snippets.enums import CategoryType
from src.core.dependencies import get_db
from src.core.config import settings

from src.technology.model import TechnologyORM
from src.technology.schemas import TechnologyCreate


router = APIRouter(prefix='/technology', tags=['Technology'])

@router.post(path="/new_technology",)
async def create_technology(
    technology_data: TechnologyCreate,
    db: Session = Depends(get_db),
):
    db_technology = TechnologyORM(**technology_data.model_dump())
    db.add(db_technology)
    db.commit()
    db.refresh(db_technology)
    return db_technology
