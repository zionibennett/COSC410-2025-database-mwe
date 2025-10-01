from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProfessorCreate(BaseModel):
    name: str

class ProfessorOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class CourseCreate(BaseModel):
    title: str
    professor_id: int

class CourseOut(BaseModel):
    id: int
    title: str
    professor_id: int
    professor_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
