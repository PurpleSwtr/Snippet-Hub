from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from src.snippets.enums import CategoryType
from src.core.dependencies import SessionDep, get_db
from src.core.config import settings
from src.technology.model import TechnologyORM
from src.technology.schemas import TechnologyCreate, TechnologyRead, TechnologyUpdate

router = APIRouter(prefix='/technology', tags=['Technology'])

@router.get("/", response_model=list[TechnologyRead])
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.technologies_list) 
async def get_technologies(db: SessionDep):
    stmt = select(TechnologyORM).order_by(TechnologyORM.name)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get(path="/techology/{id}")
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.technologies_list) 
async def get_technology(id: int, db: SessionDep):
    stmt = select(TechnologyORM).where(TechnologyORM.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

@router.post(path="/new_technology",)
async def create_technology(
    technology_data: TechnologyCreate,
    db: SessionDep,
):
    stmt = select(TechnologyORM).where(TechnologyORM.name == technology_data.name)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
         raise HTTPException(status_code=409, detail="Запись уже существует")

    new_tech = TechnologyORM(**technology_data.model_dump())
    db.add(new_tech)
    await db.commit()
    await db.refresh(new_tech)
    return new_tech
    

@router.patch("/{technology_id}", response_model=TechnologyRead)
async def update_technology(
    technology_id: int,
    technology_data: TechnologyUpdate,
    db: SessionDep,
):
    stmt = select(TechnologyORM).where(TechnologyORM.id == technology_id)
    result = await db.execute(stmt)
    technology = result.scalar_one_or_none()
    
    if not technology:
        raise HTTPException(status_code=404, detail="Технология не найдена")

    update_dict = technology_data.model_dump()
    for key, value in update_dict.items():
        setattr(technology, key, value)
    
    await db.commit()
    await db.refresh(technology)
    return technology

@router.delete("/delete/all")
async def delete_all_technologies(db: SessionDep):
    try:
        stmt = delete(TechnologyORM)
        result = db.execute(stmt)
        await db.commit()
        return {"message": "Все технологии удалены"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении всех технологий: {str(e)}"
        )
    
@router.delete("/{technology_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_technology(technology_id: int, db: SessionDep):
    stmt = select(TechnologyORM).where(TechnologyORM.id == technology_id)
    result = await db.execute(stmt)
    technology = result.scalar_one_or_none()
    
    if technology is None:
        raise HTTPException(status_code=404, detail="Технология не найдена")
    
    await db.delete(technology)
    await db.commit()
