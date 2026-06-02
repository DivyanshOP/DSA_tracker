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

class ProblemUpdate(BaseModel):
    title: Optional[str]
    difficulty: Optional[str]
    topic: Optional[str]
    is_solved: Optional[bool] = None




from datetime import datetime
class SessionBase(BaseModel):
    problem_id:int
    duration_minutes:int
    status:str


class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id:int
    created_at :datetime
    
    class Config:
        from_attributes = True
        
