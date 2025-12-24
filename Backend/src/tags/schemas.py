from typing import Optional
from pydantic import BaseModel

class TagBase(BaseModel):
    name: str
    # color: Optional[str] = None

class TagResponse(TagBase):
    id: int
    
    class Config:
        from_attributes = True