from typing import Optional, Sequence
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

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