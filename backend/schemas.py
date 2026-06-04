from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class ProblemBase(BaseModel):
    title: str
    difficulty: str
    topic: str
    is_solved: bool = False
    url: Optional[str] = None
    next_review_date: Optional[date] = None


class ProblemCreate(ProblemBase):
    pass

class ProblemResponse(ProblemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    difficulty: Optional[str] = None
    topic: Optional[str]= None
    url: Optional[str] = None
    is_solved: Optional[bool] = None
    next_review_date: Optional[date] = None




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
        
class AnalyticsSummary(BaseModel):
    total_problems: int
    total_solved: int
    total_minutes: int

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str