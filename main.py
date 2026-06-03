from fastapi import FastAPI
import models
from database import engine
from routers import problems,sessions,analytics

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DSA Tracker API")

# Include our routes
app.include_router(problems.router)
app.include_router(sessions.router)
app.include_router(analytics.router)
@app.get("/")
def root():
    return {"message": "DSA Tracker API is running. Go to /docs to test."}