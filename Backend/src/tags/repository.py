from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.tags.model import TagORM
from src.tags.schemas import TagCreate

class TagRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tag_data: TagCreate) -> TagORM:
        stmt = select(TagORM).where(TagORM.name == tag_data.name)
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400, 
                detail=f"Тег '{tag_data.name}' уже существует"
            )

        new_tag = TagORM(name=tag_data.name, color=tag_data.color)
        
        self.session.add(new_tag)
        await self.session.commit()
        await self.session.refresh(new_tag)
        
        return new_tag