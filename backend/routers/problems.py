from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, auth
from database import SessionLocal

router = APIRouter(prefix="/problems", tags=["Problems"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_problems(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Problem).filter(models.Problem.user_id == current_user.id).all()

@router.post("/")
def create_problem(problem: schemas.ProblemBase, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    
    db_problem = models.Problem(**problem.model_dump(), user_id=current_user.id)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@router.get("/triage")
def get_triage_queue(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Problem).filter(
        models.Problem.user_id == current_user.id,
        models.Problem.is_solved == True,
        ~models.Problem.sessions.any()
    ).all()

@router.get("/due")
def get_due_problems(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Problem).filter(
        models.Problem.user_id == current_user.id,
        models.Problem.is_solved == True,
        models.Problem.next_review_date <= date.today()
    ).all()