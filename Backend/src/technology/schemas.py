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
    about: Optional[str] = None

class TechnologyUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    about: Optional[str] = None

class TechnologyUpdateDescription(BaseModel):
    description: str

class TechnologyUpdateIcon(BaseModel):
    icon: str