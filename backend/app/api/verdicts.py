from bson import ObjectId

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.auth.dependencies import get_current_user

from app.database.collections import (
    submissions_collection
)

router = APIRouter(
    prefix="/verdicts",
    tags=["Verdicts"]
)


@router.get("/")
def test_verdicts():
    return {
        "message": "Verdicts API Working"
    }


@router.get("/all")
def get_all_verdicts():

    submissions = list(
        submissions_collection.find()
    )

    verdicts = []

    for submission in submissions:

        verdicts.append({
            "submission_id": str(submission["_id"]),
            "user_id": submission.get("user_id"),
            "outcome": submission.get("outcome"),
            "verdict": submission.get("verdict")
        })

    return verdicts


@router.put("/{submission_id}/override")
def override_verdict(
    submission_id: str,
    outcome: str,
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    result = submissions_collection.update_one(
        {
            "_id": ObjectId(submission_id)
        },
        {
            "$set": {
                "outcome": outcome
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Submission not found"
        )

    return {
        "message": "Verdict overridden successfully",
        "new_outcome": outcome
    }