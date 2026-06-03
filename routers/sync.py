from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import models
from database import SessionLocal

router = APIRouter(prefix="/sync", tags=["Integrations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/leetcode/{username}")
def sync_leetcode(username: str, db: Session = Depends(get_db)):
    url = "https://leetcode.com/graphql"
    
    # QUERY 1: Get the list of recent problems
    recent_query = """
    query getRecentSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            title
            titleSlug
        }
    }
    """
    try:
        response = requests.post(url, json={"query": recent_query, "variables": {"username": username, "limit": 20}})
        response.raise_for_status()
        submissions = response.json().get("data", {}).get("recentAcSubmissionList", [])
        
        if not submissions:
            return {"message": "No recent accepted submissions found.", "added": 0, "updated": 0}
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch from LeetCode: {str(e)}")

    added_count = 0
    updated_count = 0

   
    detail_query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            difficulty
            topicTags {
                name
            }
        }
    }
    """

    for sub in submissions:
        title = sub["title"]
        slug = sub["titleSlug"]
        problem_url = f"https://leetcode.com/problems/{slug}/"
        
        
        detail_resp = requests.post(url, json={"query": detail_query, "variables": {"titleSlug": slug}})
        question_data = detail_resp.json().get("data", {}).get("question", {})
        
        
        difficulty = question_data.get("difficulty", "Unknown") if question_data else "Unknown"
        
        tags_list = question_data.get("topicTags", []) if question_data else []
        topic_string = ", ".join([tag["name"] for tag in tags_list]) if tags_list else "Unknown"

        
        existing_problem = db.query(models.Problem).filter(models.Problem.title == title).first()
        
        if existing_problem:
            if not existing_problem.is_solved:
                existing_problem.is_solved = True
                updated_count += 1
            
            existing_problem.topic = topic_string
            existing_problem.difficulty = difficulty
            existing_problem.url = problem_url
        else:
            new_problem = models.Problem(
                title=title,
                difficulty=difficulty, 
                topic=topic_string,
                url=problem_url,
                is_solved=True
            )
            db.add(new_problem)
            added_count += 1

    db.commit()
    
    return {
        "message": "Deep Sync complete!", 
        "added": added_count, 
        "updated": updated_count
    }