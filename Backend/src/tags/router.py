from fastapi import APIRouter
from sqlalchemy import select

from src.tags.schemas import TagBase, TagResponse, TagCreate
from src.tags.model import TagORM
from src.tags.repository import TagRepository
from src.core.dependencies import SessionDep

router = APIRouter(prefix='/tags', tags=['Tags'])

@router.get(path="/", response_model=list[TagResponse])
async def get_tags(
    db: SessionDep
):
    stmt = select(TagORM)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post(path="/", response_model=TagResponse, status_code=201)
async def create_tag(
    tag_data: TagCreate,
    db: SessionDep
):
    repo = TagRepository(db)
    return await repo.create(tag_data)