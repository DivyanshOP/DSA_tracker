from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal

router = APIRouter(prefix="/problems", tags=["Problems"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ProblemResponse)
def create_problem(problem: schemas.ProblemCreate, db: Session = Depends(get_db)):
    db_problem = models.Problem(**problem.model_dump())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@router.get("/", response_model=List[schemas.ProblemResponse])
def get_problems(db: Session = Depends(get_db)):
    return db.query(models.Problem).all()