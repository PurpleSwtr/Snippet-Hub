from pydantic import BaseModel, Field

from src.snippets.enums import CategoryType, OptionType

class OptionResponse(BaseModel):
    content: str

class OptionCreate(BaseModel):
    name: str
    icon: str
    description: str
    content: str
    option_type: OptionType
    public: bool = True
    category: CategoryType | None = None

class OptionRead(BaseModel):
    id: int
    name: str
    description: str
    content: str
    option_type: OptionType
    category: CategoryType | None

class OptionPrompt(BaseModel):
    content: str