from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from sqlalchemy.sql import func

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get(path='/summary',response_model=schemas.AnalyticsSummary)
def get_summary(db:Session=Depends(get_db)):
    total_problems = db.query(models.Problem).count()
    total_solved = db.query(models.Problem).filter(models.Problem.is_solved == True).count()
    total_time = db.query(func.sum(models.Session.duration_minutes)).scalar() or 0

    return {'total_problems': total_problems,'total_solved':total_solved,'total_minutes':total_time}
