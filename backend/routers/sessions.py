from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models,schemas
from database import SessionLocal
from datetime import date, timedelta
router = APIRouter(prefix='/sessions', tags=["Sessions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/",response_model = List[schemas.SessionResponse])
def get_sessions(db:Session=Depends(get_db)):
    return db.query(models.Session).all()

@router.post("/", response_model=schemas.SessionResponse)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    db_session = models.Session(**session.model_dump())
    db.add(db_session)
    
    
    problem = db.query(models.Problem).filter(models.Problem.id == session.problem_id).first()
    
    if problem:
        
        problem.is_solved = True 
        
        
        today = date.today()
        if session.status == "Confused":
            problem.next_review_date = today + timedelta(days=1)  
        elif session.status == "Needed Hints":
            problem.next_review_date = today + timedelta(days=3) 
        elif session.status == "Solved smoothly":
            problem.next_review_date = today + timedelta(days=7)  
            
    db.commit()
    db.refresh(db_session)
    return db_session


