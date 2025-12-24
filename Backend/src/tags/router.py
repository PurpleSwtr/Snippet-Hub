from fastapi import APIRouter
from sqlalchemy import select

from src.tags.schemas import TagBase, TagResponse
from src.tags.model import TagORM
from src.core.dependencies import SessionDep

router = APIRouter(prefix='/tags', tags=['Tags'])

@router.get(path="/", response_model=list[TagBase])
async def get_tags(
    db: SessionDep
):
    stmt = select(TagORM)
    result = await db.execute(stmt)
    return result.scalars().all()

