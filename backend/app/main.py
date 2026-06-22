from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.submissions import router as submission_router
from app.api.appeals import router as appeals_router
from app.api.verdicts import router as verdicts_router
from app.api.analytics import router as analytics_router
from app.api.policies import router as policies_router

app = FastAPI(
    title="AI Content Moderation Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(submission_router)
app.include_router(appeals_router)
app.include_router(verdicts_router)
app.include_router(analytics_router)
app.include_router(policies_router)


@app.get("/")
async def root():
    return {
        "message": "AI Content Moderation Platform API",
        "version": "1.0.0",
        "status": "running"
    }