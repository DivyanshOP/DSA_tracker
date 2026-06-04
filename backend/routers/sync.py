from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
import models, auth
from database import SessionLocal

router = APIRouter(prefix="/sync", tags=["Sync"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/leetcode/{username}")
def sync_leetcode(username: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    url = "https://leetcode.com/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }

    recent_query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        title
        titleSlug
      }
    }
    """
    
    try:
        response = requests.post(
            url, 
            json={"query": recent_query, "variables": {"username": username, "limit": 20}},
            headers=headers, 
            timeout=10
        )
        data = response.json()
        submissions = data.get("data", {}).get("recentAcSubmissionList", [])
    except Exception as e:
        return {"message": "Failed to connect to LeetCode", "error": str(e)}

    added = 0
    updated = 0

    for sub in submissions:
        title = sub["title"]
        slug = sub["titleSlug"]

        
        existing = db.query(models.Problem).filter(
            models.Problem.title == title,
            models.Problem.user_id == current_user.id 
        ).first()

        if existing:
            if not existing.is_solved:
                existing.is_solved = True
                updated += 1
            continue

        
        detail_query = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            difficulty
            topicTags { name }
          }
        }
        """
        try:
            detail_resp = requests.post(
                url, 
                json={"query": detail_query, "variables": {"titleSlug": slug}},
                headers=headers,
                timeout=5
            )
            detail_data = detail_resp.json().get("data", {}).get("question", {})
            
            difficulty = detail_data.get("difficulty", "Medium")
            tags = detail_data.get("topicTags", [])
            topic = tags[0]["name"] if tags else "General"
        except:
            difficulty = "Medium"
            topic = "General"

        
        new_problem = models.Problem(
            title=title,
            difficulty=difficulty,
            topic=topic,
            url=f"https://leetcode.com/problems/{slug}/",
            is_solved=True,
            user_id=current_user.id 
        )
        db.add(new_problem)
        added += 1

    db.commit()
    return {"message": "Sync complete!", "added": added, "updated": updated}