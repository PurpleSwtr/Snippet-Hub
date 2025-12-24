from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, Column, String, Enum as SQLEnum, Table, Text
from sqlalchemy import String, ForeignKey
from src.snippets.enums import SnippetType
from src.core.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.tags.model import TagORM
    from src.technology.model import TechnologyORM


snippet_tags = Table(
    "snippet_tags",
    Base.metadata,
    Column("snippet_id", ForeignKey("snippets.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

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
    tags: Mapped[list["TagORM"]] = relationship(
        "TagORM",
        secondary=snippet_tags,
        back_populates="snippets",
        lazy="selectin", 
    )