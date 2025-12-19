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
    
    snippets: Mapped[list["SnippetORM"]] = relationship(
        "SnippetORM",
        back_populates="technology",
        cascade="all, delete-orphan",
        lazy="selectin"
    )