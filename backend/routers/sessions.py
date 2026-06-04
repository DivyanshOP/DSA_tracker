from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, auth
from database import SessionLocal

router = APIRouter(prefix="/sessions", tags=["Sessions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    
    db_session = models.Session(**session.model_dump(), user_id=current_user.id)
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
    return db_session