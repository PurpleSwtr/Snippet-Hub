from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, String, Enum as SQLEnum, Text
from sqlalchemy import String, ForeignKey
from src.technology.model import TechnologyORM
from src.snippets.enums import SnippetType
from src.core.db import Base

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
    # - Для CODE: {"language": "python", "framework": "fastapi"}
    # - Для LINK: {"url": "https://...", "preview": "..."}
    # - Для ARCHIVE: {"filename": "project.zip", "size": 1024}
    meta_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        default=dict
    )

    technology: Mapped["TechnologyORM"] = relationship(
        back_populates="snippets"
    )