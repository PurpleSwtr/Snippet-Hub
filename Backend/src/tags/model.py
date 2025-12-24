# src/tags/model.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.core.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.snippets.model import SnippetORM

class TagORM(Base):
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    color: Mapped[str] = mapped_column(String, nullable=True)

    snippets: Mapped[list["SnippetORM"]] = relationship(
        "SnippetORM",
        secondary="snippet_tags",
        back_populates="tags",
        lazy="selectin"
    )