from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    difficulty = Column(String)  
    topic = Column(String)       
    is_solved = Column(Boolean, default=False)

    
    sessions = relationship("Session", back_populates="problem")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    
    problem_id = Column(Integer, ForeignKey("problems.id")) 
    duration_minutes = Column(Integer)
    status = Column(String) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
    problem = relationship("Problem", back_populates="sessions")