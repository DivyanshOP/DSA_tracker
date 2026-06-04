from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    problems = relationship("Problem", back_populates="owner")
    sessions = relationship("Session", back_populates="owner")

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    difficulty = Column(String)  
    topic = Column(String)       
    url = Column(String, nullable=True)
    is_solved = Column(Boolean, default=False)
    next_review_date = Column(Date, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id")) # <-- NEW
    
    owner = relationship("User", back_populates="problems")
    sessions = relationship("Session", back_populates="problem")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    duration_minutes = Column(Integer)
    status = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id")) # <-- NEW

    owner = relationship("User", back_populates="sessions")
    problem = relationship("Problem", back_populates="sessions")