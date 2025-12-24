from typing import Optional
from pydantic import BaseModel, Field

from src.tags.schemas import TagBase, TagResponse
from src.tags.model import TagORM
from src.technology.model import TechnologyORM
from src.snippets.enums import SnippetType

class SnippetCreate(BaseModel):
    title: str
    snippet_type: SnippetType
    content: str
    technology_id: int
    tags: list[TagBase] = [] 

class SnippetUpdate(BaseModel):
    title: Optional[str] = None
    snippet_type: Optional[SnippetType] = None
    content: Optional[str] = None
    # technology_id: Optional[int] = None
    tags: Optional[list[TagBase]] = [] 

class SnippetResponse(BaseModel):
    id: int
    title: str
    content: str
    snippet_type: SnippetType
    tags: list[TagResponse] = [] 

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
