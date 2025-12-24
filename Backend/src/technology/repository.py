from typing import Optional, Sequence
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.technology.model import TechnologyORM
from src.technology.schemas import TechnologyCreate, TechnologyUpdate, TechnologyUpdateDescription, TechnologyUpdateIcon


class TechnologyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[TechnologyORM]:
        stmt = select(TechnologyORM).order_by(TechnologyORM.name)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, tech_id: int) -> Optional[TechnologyORM]:
        stmt = select(TechnologyORM).where(TechnologyORM.id == tech_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, tech_data: TechnologyCreate) -> TechnologyORM:
        existing = await self.get_by_name(tech_data.name)
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Технология с таким названием уже существует"
            )
        
        new_tech = TechnologyORM(**tech_data.model_dump())
        self.session.add(new_tech)
        await self.session.commit()
        await self.session.refresh(new_tech)
        return new_tech

    async def update(self, tech_id: int, tech_data: TechnologyUpdate) -> TechnologyORM:
        technology = await self.get_by_id(tech_id)
        if not technology:
            raise HTTPException(status_code=404, detail="Технология не найдена")

        update_dict = tech_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(technology, key, value)

        await self.session.commit()
        await self.session.refresh(technology)
        return technology

    async def delete(self, tech_id: int) -> None:
        technology = await self.get_by_id(tech_id)
        if not technology:
            raise HTTPException(status_code=404, detail="Технология не найдена")
        await self.session.delete(technology)
        await self.session.commit()

    async def delete_all(self) -> None:
        try:
            stmt = delete(TechnologyORM)
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при удалении всех технологий: {str(e)}"
            )
    
    async def get_by_name(self, name: str) -> Optional[TechnologyORM]:
        stmt = select(TechnologyORM).where(TechnologyORM.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_icon(self, tech_id: int, tech_data: TechnologyUpdateIcon) -> TechnologyORM:
        technology = await self.get_by_id(tech_id)
        if not technology:
            raise HTTPException(status_code=404, detail="Технология не найдена")

        existing = await self.get_by_name(tech_data.icon)
        if existing and existing.id != tech_id:
            raise HTTPException(
                status_code=409,
                detail="Технология с таким названием уже существует"
            )

        technology.icon = tech_data.icon
        await self.session.commit()
        await self.session.refresh(technology)
        return technology
    
    async def update_description(self, tech_id: int, tech_data: TechnologyUpdateDescription) -> TechnologyORM:
        technology = await self.get_by_id(tech_id)
        if not technology:
            raise HTTPException(status_code=404, detail="Технология не найдена")

        existing = await self.get_by_name(tech_data.description)
        if existing and existing.id != tech_id:
            raise HTTPException(
                status_code=409,
                detail="Технология с таким названием уже существует"
            )

        technology.description = tech_data.description
        await self.session.commit()
        await self.session.refresh(technology)
        return technology