from pydantic import BaseModel, Field

from src.snippets.enums import CategoryType

class TechnologyResponse(BaseModel):
    content: str

class TechnologyCreate(BaseModel):
    name: str
    icon: str
    description: str

class TechnologyRead(BaseModel):
    id: int
    name: str
    description: str
    icon: str

class TechnologyUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    description: str | None = None