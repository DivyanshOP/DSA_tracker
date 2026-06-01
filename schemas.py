from pydantic import BaseModel
from typing import Optional


class ProblemBase(BaseModel):
    title: str
    difficulty: str
    topic: str
    is_solved: bool = False


class ProblemCreate(ProblemBase):
    pass

class ProblemResponse(ProblemBase):
    id: int

    class Config:
        from_attributes = True