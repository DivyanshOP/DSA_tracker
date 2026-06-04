from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas,auth
from database import SessionLocal
from sqlalchemy.sql import func
import pandas as pd


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Notice we added the filter for current_user.id to every query!
    total_problems = db.query(models.Problem).filter(
        models.Problem.user_id == current_user.id
    ).count()
    
    total_solved = db.query(models.Problem).filter(
        models.Problem.user_id == current_user.id,
        models.Problem.is_solved == True
    ).count()
    
    total_minutes = db.query(func.sum(models.Session.duration_minutes)).filter(
        models.Session.user_id == current_user.id
    ).scalar() or 0

    return {
        "total_problems": total_problems,
        "total_solved": total_solved,
        "total_minutes": total_minutes
    }

@router.get('/coach')
def get_smart_coach(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    sessions = db.query(models.Session, models.Problem).join(models.Problem).all()
    
    if not sessions:
        return {"status": "insufficient_data", "message": "Log a few study sessions first so I can analyze your habits!"}
    
    data = []
    for sess, prob in sessions:
        primary_topic = prob.topic.split(",")[0].strip() if prob.topic else "Unknown"
        
        data.append({
            "topic": primary_topic,
            "duration": sess.duration_minutes,
            "status": sess.status
        })
        
    df = pd.DataFrame(data)
    
    topic_stats = df.groupby('topic').agg(
        avg_time=('duration', 'mean'),
        total_sessions=('duration', 'count'),
        struggle_count=('status', lambda x: (x != 'Solved smoothly').sum())
    ).reset_index()
    
    topic_stats['struggle_ratio'] = topic_stats['struggle_count'] / topic_stats['total_sessions']
    topic_stats['weakness_score'] = topic_stats['avg_time'] * topic_stats['struggle_ratio']
    
    valid_topics = topic_stats[topic_stats['total_sessions'] > 1]
    
    if valid_topics.empty:
         return {"status": "insufficient_data", "message": "Keep logging! I need at least 2 sessions on a topic to find patterns."}

    weakest_topic = valid_topics.sort_values(by='weakness_score', ascending=False).iloc[0]
    
    return {
        "status": "success",
        "weakest_topic": weakest_topic['topic'],
        "avg_time": round(weakest_topic['avg_time'], 1),
        "struggle_rate": round(weakest_topic['struggle_ratio'] * 100, 1),
    }