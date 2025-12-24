from typing import Optional, Sequence
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.snippets.schemas import SnippetCreate, SnippetUpdate
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
                    new_tag = TagORM(name=tag_in.name)
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
    
    async def update(self, snippet_id: int, snippet_data: SnippetUpdate) -> Optional[SnippetORM]:
        snippet = await self.get_by_id(snippet_id)
        if not snippet:
            raise HTTPException(status_code=404, detail="Сниппет не найден")

        update_dict = snippet_data.model_dump(exclude_unset=True)

        if 'tags' in update_dict:
            tags_data = update_dict.pop('tags')
            
            if tags_data is not None:
                tag_names = [t['name'] for t in tags_data]
                
                stmt = select(TagORM).where(TagORM.name.in_(tag_names))
                result = await self.session.execute(stmt)
                existing_tags = result.scalars().all()
                existing_tag_names = {tag.name for tag in existing_tags}
                
                new_tags_orm_list = list(existing_tags)
                
                for tag_dict in tags_data:
                    if tag_dict['name'] not in existing_tag_names:
                        new_tag = TagORM(name=tag_dict['name'])
                        new_tags_orm_list.append(new_tag)
                
                snippet.tags = new_tags_orm_list

        for key, value in update_dict.items():
            setattr(snippet, key, value)

        await self.session.commit()

        return await self.get_by_id(snippet_id)