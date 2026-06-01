from fastapi import FastAPI
import models
from database import engine
from routers import problems

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Study Tracker API")

# Include our routes
app.include_router(problems.router)

@app.get("/")
def root():
    return {"message": "Study Tracker API is running. Go to /docs to test."}