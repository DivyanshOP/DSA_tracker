from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import problems, sessions, analytics, sync,users
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DSA Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problems.router)
app.include_router(sessions.router)
app.include_router(analytics.router)
app.include_router(sync.router)
app.include_router(users.router)