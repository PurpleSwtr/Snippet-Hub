from typing import Optional, Sequence
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.snippets.schemas import SnippetCreate
from src.tags.model import TagORM
from src.snippets.model import SnippetORM

class SnippetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete_all(self) -> None:
        try:
            stmt = delete(SnippetORM)
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при удалении всех технологий: {str(e)}"
            )
    
    async def create(self, snippet_data: SnippetCreate) -> SnippetORM:
      
        snippet_dict = snippet_data.model_dump(exclude={'tags'})
        new_snippet = SnippetORM(**snippet_dict)

        if snippet_data.tags:
            tag_names = [tag.name for tag in snippet_data.tags]

            stmt = select(TagORM).where(TagORM.name.in_(tag_names))
            result = await self.session.execute(stmt)
            existing_tags = result.scalars().all()
            
            existing_tag_names = {tag.name for tag in existing_tags}

            tags_to_attach = list(existing_tags)

            for tag_in in snippet_data.tags:
                if tag_in.name not in existing_tag_names:
                    new_tag = TagORM(name=tag_in.name, color=tag_in.color)
                    tags_to_attach.append(new_tag)
            
            new_snippet.tags = tags_to_attach

        self.session.add(new_snippet)
        await self.session.commit()
        await self.session.refresh(new_snippet)
        return new_snippet

    async def delete(self, snippet_id: int) -> None:
        snippet = await self.get_by_id(snippet_id)
        if not snippet:
            raise HTTPException(status_code=404, detail="Технология не найдена")
        await self.session.delete(snippet)
        await self.session.commit()

    async def get_by_id(self, snippet_id: int) -> Optional[SnippetORM]:
        stmt = select(SnippetORM).where(SnippetORM.id == snippet_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()