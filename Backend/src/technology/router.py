from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from src.core.dependencies import SessionDep
from src.core.config import settings
from src.technology.repository import TechnologyRepository
from src.technology.schemas import TechnologyCreate, TechnologyRead, TechnologyUpdate, TechnologyUpdateDescription, TechnologyUpdateIcon

router = APIRouter(prefix='/technology', tags=['Technology'])

@router.get("/", response_model=list[TechnologyRead])
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.technologies_list)
async def get_technologies(db: SessionDep):
    repo = TechnologyRepository(db)
    return await repo.get_all()

@router.get("/{tech_id}", response_model=TechnologyRead)
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.technologies_list)
async def get_technology(tech_id: int, db: SessionDep):
    repo = TechnologyRepository(db)
    tech = await repo.get_by_id(tech_id)
    if not tech:
        raise HTTPException(status_code=404, detail="Технология не найдена")
    return tech

@router.post("/", response_model=TechnologyRead, status_code=201)
async def create_technology(tech_data: TechnologyCreate, db: SessionDep):
    repo = TechnologyRepository(db)
    return await repo.create(tech_data)

@router.patch("/{tech_id}", response_model=TechnologyRead)
async def update_technology(tech_id: int, tech_data: TechnologyUpdate, db: SessionDep):
    repo = TechnologyRepository(db)
    return await repo.update(tech_id, tech_data)

@router.delete("/{tech_id}", status_code=204)
async def delete_technology(tech_id: int, db: SessionDep):
    repo = TechnologyRepository(db)
    await repo.delete(tech_id)

@router.delete("/", status_code=200)
async def delete_all_technologies(db: SessionDep):
    repo = TechnologyRepository(db)
    await repo.delete_all()
    return {"message": "Все технологии удалены"}

@router.put("/{tech_id}/update-icon", response_model=TechnologyRead)
async def update_technology_icon(
    tech_id: int,
    tech_data: TechnologyUpdateIcon,
    db: SessionDep
):
    repo = TechnologyRepository(db)
    updated_tech = await repo.update_icon(tech_id, tech_data)
    return updated_tech


@router.put("/{tech_id}/update-description", response_model=TechnologyRead)
async def update_technology_description(
    tech_id: int,
    tech_data: TechnologyUpdateDescription,
    db: SessionDep
):
    repo = TechnologyRepository(db)
    updated_tech = await repo.update_description(tech_id, tech_data)
    return updated_tech