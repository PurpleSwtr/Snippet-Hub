from pydantic import BaseModel, Field

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
