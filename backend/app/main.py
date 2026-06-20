from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.submissions import router as submission_router
from app.api.appeals import router as appeals_router
from app.api.verdicts import router as verdicts_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title="AI Content Moderation Platform",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(submission_router)
app.include_router(appeals_router)
app.include_router(verdicts_router)
app.include_router(analytics_router)


@app.get("/")
async def root():
    return {
        "message": "AI Content Moderation Platform API"
    }