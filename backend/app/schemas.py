from pydantic import BaseModel, ConfigDict
from typing import Optional

class AuthorCreate(BaseModel):
    name: str

class AuthorOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
    title: str
    author_id: int

class BookOut(BaseModel):
    id: int
    title: str
    author_id: int
    author_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
