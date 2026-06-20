from fastapi import APIRouter

from app.database.collections import submissions_collection

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