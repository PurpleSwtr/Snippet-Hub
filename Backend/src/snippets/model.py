from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy import String
from src.snippets.enums import OptionType, CategoryType
from src.core.db import Base

class PromptOptionORM(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    option_type: Mapped[OptionType] = mapped_column(SQLEnum(OptionType), nullable=False)
    icon: Mapped[str] = mapped_column(String, nullable=False)

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)


    # FIXME сделать связь с пользователями
    author: Mapped[int] = mapped_column(nullable=True) 

    public: Mapped[bool] = mapped_column(nullable=False)
    category: Mapped[CategoryType] = mapped_column(SQLEnum(CategoryType), nullable=True)
    priority: Mapped[int] = mapped_column(default=0)
