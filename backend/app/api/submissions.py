from datetime import datetime
import os
import uuid
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from app.auth.dependencies import get_current_user

from app.database.collections import submissions_collection
from app.services.moderation_service import analyze_image

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/")
def test_submission():
    return {
        "message": "Submission API Working"
    }


@router.get("/my")
def get_my_submissions(
    current_user=Depends(get_current_user)
):

    submissions = list(
        submissions_collection.find(
            {
                "user_id": current_user["user_id"]
            }
        )
    )

    for submission in submissions:
        submission["_id"] = str(
            submission["_id"]
        )

    return submissions


@router.get("/all")
def get_all_submissions():

    submissions = list(
        submissions_collection.find()
    )

    for submission in submissions:
        submission["_id"] = str(
            submission["_id"]
        )

    return submissions


@router.post("/upload")
async def upload_image(
    image: UploadFile = File(...),
    current_user=Depends(get_current_user)
):

    file_extension = image.filename.split(".")[-1]

    unique_filename = (
        f"{uuid.uuid4()}.{file_extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )

    verdict = analyze_image(file_path)

    submission = {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "images": [file_path],
        "outcome": verdict["overall_outcome"],
        "verdict": verdict,
        "created_at": datetime.utcnow()
    }

    result = submissions_collection.insert_one(
        submission
    )

    return {
        "message": "Image uploaded successfully",
        "submission_id": str(result.inserted_id),
        "image_path": file_path,
        "outcome": verdict["overall_outcome"],
        "user": current_user["email"]
    }