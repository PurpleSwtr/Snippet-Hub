
---

### 📄 `package.json`

```json
{
  "devDependencies": {
    "@iconify-json/heroicons": "^1.2.3",
    "@iconify-json/simple-icons": "^1.2.63"
  }
}
```

---

### 📄 `pyproject.toml`

```toml
[project]
name = "backend"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "alembic>=1.17.2",
    "asyncpg>=0.31.0",
    "fastapi>=0.124.2",
    "fastapi-cache2>=0.2.2",
    "ollama>=0.6.1",
    "pydantic>=2.12.5",
    "pydantic-settings>=2.12.0",
    "redis>=7.1.0",
    "requests>=2.32.5",
    "sqlalchemy>=2.0.45",
    "uvicorn>=0.38.0",
]
```

---

### 📄 `src/__init__.py`

```python

```

---

### 📄 `src/main.py`

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache

from src.core.db import Base, engine

from redis.asyncio import Redis
from fastapi_cache.backends.redis import RedisBackend

from src.snippets.router import router as snippets_router
from src.icons.router import router as icons_router
from src.technology.router import router as techonologies_router

from src.core.config import settings

from src.technology.model import TechnologyORM
from src.snippets.model import SnippetORM

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix
    )
    # FIXME: Заглушка
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Таблицы созданы")
    yield

app = FastAPI(
    title="Technology-Snippets",
    root_path="/api/v1",
    lifespan=lifespan 
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(snippets_router)
app.include_router(icons_router)
app.include_router(techonologies_router)

# app.mount("/static/icons", StaticFiles(directory=settings.FRONT_STATIC_DIR), name="icons")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         app, 
#         host="0.0.0.0", 
#         port=8000,
#         log_level="info"
#     )
```

---

### 📄 `src/core/__init__.py`

```python

```

---

### 📄 `src/core/config.py`

```python
from pathlib import Path
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class RedisDB(BaseModel):
    cache: int = 0

class RedisConfig(BaseModel):
    host: str = Field(default="localhost", validation_alias="REDIS_HOST")
    port: int = Field(default=6379, validation_alias="REDIS_PORT")
    TTL: int = Field(default=15, validation_alias="CACHE_TTL")
    db: RedisDB = RedisDB()

class CacheNamespace(BaseModel):
    icons_list: str = "icons-list"
    # options_list: str = "options-list"
    snippets_list: str = "snippets-list"
    technologies_list: str = "technologies-list"

class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()

class Settings(BaseSettings):
    app_name: str = "LLM Manager"
    
    BASE_DIR: Path = Path(__file__).resolve().parents[2]

    FRONT_STATIC_DIR: Path = Path(__file__).resolve().parents[3] / "Frontend" / "public" / "icons"


    redis: RedisConfig = Field(default_factory=RedisConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

settings = Settings()
```

---

### 📄 `src/core/db.py`

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://app_user:example@localhost:5432/app_db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
```

---

### 📄 `src/core/dependencies.py`

```python
from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import async_session_maker

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
```

---

### 📄 `src/icons/__init__.py`

```python

```

---

### 📄 `src/icons/router.py`

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi_cache.decorator import cache

from src.core.config import settings 
from src.icons.service import get_icons_names, get_icon
router = APIRouter(prefix='/icons', tags=['Icons'])

@router.get("/namelist/{pack}")
@cache(expire=settings.redis.TTL, namespace=settings.cache.namespace.icons_list) 
async def list_icons(pack: str):
    print("Данные с диска")
    try:
        data = get_icons_names(pack=pack)
        if not data:
            raise NotADirectoryError
        return data
    except NotADirectoryError:
        raise HTTPException(status_code=404, detail="Pack not found")

# @router.get("/static/{pack}/{filename}")
# async def get_icon_file(pack: str, filename: str):
#     try:
#         icon_path = get_icon(pack=pack, filename=filename)
#         return FileResponse(icon_path, media_type="image/svg+xml")
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="Icon not found")
```

---

### 📄 `src/icons/service.py`

```python
import os
from pathlib import Path
from src.core.config import settings

def get_directory(floader: str):
    icons_path = os.path.join(settings.FRONT_STATIC_DIR, floader)
    if not os.path.isdir(icons_path):
        raise NotADirectoryError(f"Pack not found")
    return icons_path

def get_icons_names(pack: str):
    icons_path = get_directory(floader=pack)
    all_items = os.listdir(icons_path)
    files_only = [item for item in all_items if os.path.isfile(os.path.join(icons_path, item))]
    return files_only

def get_icon(pack: str ,filename: str):
    icon_path = get_directory(floader=pack)
    return os.path.join(icon_path, filename)
```

---

### 📄 `src/snippets/__init__.py`

```python

```

---

### 📄 `src/snippets/enums.py`

```python
from enum import Enum

class SnippetType(str, Enum):
    CODE = "code"
    MARKDOWN = "markdown"
    # IMAGE = "image"
    ARCHIVE = "archive"
    LINK = "link"
    PROMPT = "prompt"

class OptionType(str, Enum):
    FORMAT = "format"
    MODIFIER = "modifier" 
    ROLE = "role"
    TEMPLATE = "template"

class CategoryType(str, Enum):
    GENERAL = "general"
    PROGRAMMING = "programming"
    DESIGN = "design"
    DOCUMENTATION = "documentation"
    SECURITY = "security"
    DATA_SCIENCE = "data_science"
    DEVOPS = "devops"
    BUSINESS = "business"
```

---

### 📄 `src/snippets/model.py`

```python
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, String, Enum as SQLEnum, Text
from sqlalchemy import String, ForeignKey
from src.snippets.enums import SnippetType
from src.core.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.technology.model import TechnologyORM


class SnippetORM(Base):
    __tablename__ = "snippets"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    technology_id: Mapped[int] = mapped_column(
        ForeignKey("technologies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    snippet_type: Mapped[SnippetType] = mapped_column(
        SQLEnum(SnippetType),
        nullable=False,
        index=True
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    #   В теории:    
    # - CODE: {"language": "python", "framework": "fastapi"}
    # - LINK: {"url": "https://...", "preview": "..."}
    # - ARCHIVE: {"filename": "project.zip", "size": 1024}
    meta_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        default=dict
    )

    technology: Mapped["TechnologyORM"] = relationship(
        back_populates="snippets",
        foreign_keys=[technology_id],
        lazy="selectin"
    )
```

---

### 📄 `src/snippets/repository.py`

```python
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
```

---

### 📄 `src/snippets/router.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from src.technology.model import TechnologyORM
from src.snippets.model import SnippetORM
from src.snippets.schemas import SnippetCreate, SnippetResponse
from src.snippets.enums import CategoryType
from src.core.dependencies import SessionDep
from src.snippets.repository import SnippetRepository
from src.core.config import settings

router = APIRouter(prefix='/snippets', tags=['Snippets'])

@router.post(path="/new_snippet", response_model=SnippetResponse, status_code=201)
async def create_snippet(
    snippet_data: SnippetCreate,
    db: SessionDep,
):
    stmt = select(SnippetORM).where(SnippetORM.title == snippet_data.title)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Запись уже существует")

    new_tech = SnippetORM(**snippet_data.model_dump())
    db.add(new_tech)
    await db.commit()
    await db.refresh(new_tech)
    return new_tech
    
@router.get(path="/", response_model=list[SnippetResponse])
async def get_snippets(
    db: SessionDep
):
    stmt = select(SnippetORM)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get(path="/{tech_id}", response_model=list[SnippetResponse])
async def get_snippets_by_technology(
    tech_id: int,
    db: SessionDep
):
    tech_exists_stmt = select(TechnologyORM.id).where(TechnologyORM.id == tech_id)
    tech_exists = await db.execute(tech_exists_stmt)
    
    if not tech_exists.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Технология не найдена")

    stmt = select(SnippetORM).where(SnippetORM.technology_id == tech_id)
    result = await db.execute(stmt)
    snippets = result.scalars().all()
    return snippets


@router.delete("/", status_code=200)
async def delete_all_technologies(db: SessionDep):
    repo = SnippetRepository(db)
    await repo.delete_all()
    return {"message": "Все технологии удалены"}

@router.delete("/{id}", status_code=204)
async def delete(tech_id: int, db: SessionDep):
    repo = SnippetRepository(db)
    await repo.delete(tech_id)
```

---

### 📄 `src/snippets/schemas.py`

```python
from pydantic import BaseModel, Field

from src.technology.model import TechnologyORM
from src.snippets.enums import SnippetType

class SnippetCreate(BaseModel):
    title: str
    snippet_type: SnippetType
    content: str
    technology_id: int

class SnippetResponse(BaseModel):
    id: int
    title: str
    content: str
    snippet_type: SnippetType
    
    class Config:
        from_attributes = True
# class SnippetORM(Base):
#     __tablename__ = "snippets"
    
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

#     technology_id: Mapped[int] = mapped_column(
#         ForeignKey("technologies.id", ondelete="CASCADE"),
#         nullable=False,
#         index=True
#     )
    
#     snippet_type: Mapped[SnippetType] = mapped_column(
#         SQLEnum(SnippetType),
#         nullable=False,
#         index=True
#     )

#     content: Mapped[str] = mapped_column(Text, nullable=False)

#     meta_data: Mapped[Optional[dict]] = mapped_column(
#         JSON,
#         nullable=True,
#         default=dict
#     )

#     technology: Mapped["TechnologyORM"] = relationship(
#         back_populates="snippets",
#         foreign_keys=[technology_id],
#         lazy="selectin"
#     )
```

---

### 📄 `src/technology/__init__.py`

```python

```

---

### 📄 `src/technology/model.py`

```python
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from src.core.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.snippets.model import SnippetORM

class TechnologyORM(Base):
    __tablename__ = "technologies"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    icon: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    about: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    snippets: Mapped[list["SnippetORM"]] = relationship(
        "SnippetORM",
        back_populates="technology",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
```

---

### 📄 `src/technology/repository.py`

```python
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
```

---

### 📄 `src/technology/router.py`

```python
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
```

---

### 📄 `src/technology/schemas.py`

```python
from typing import Optional
from pydantic import BaseModel, Field

from src.snippets.enums import CategoryType

class TechnologyCreate(BaseModel):
    name: str
    icon: str
    description: str
    about: str

class TechnologyRead(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    about: str

class TechnologyUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    about: Optional[str] = None

class TechnologyUpdateDescription(BaseModel):
    description: str

class TechnologyUpdateIcon(BaseModel):
    icon: str
```
