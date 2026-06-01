from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models,schemas
from database import SessionLocal

router = APIRouter(prefix='/sessions', tags=["Sessions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/",response_model = schemas.SessionResponse)
def create_session(session: schemas.SessionCreate,db: Session=Depends(get_db)):
    problem = db.query(models.Problem).filter(models.Problem.id==session.problem_id).first()
    if not problem:
        raise HTTPException(status_code = 404, detail="Problem not found")
    db_session= models.Session(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/",response_model = List[schemas.SessionResponse])
def get_sessions(db:Session=Depends(get_db)):
    return db.query(models.Session).all()




