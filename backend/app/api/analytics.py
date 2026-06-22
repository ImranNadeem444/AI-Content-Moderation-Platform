from fastapi import APIRouter

from app.database.collections import (
    users_collection,
    submissions_collection,
    appeals_collection
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/dashboard")
def get_dashboard_analytics():

    total_users = users_collection.count_documents({})

    total_submissions = (
        submissions_collection.count_documents({})
    )

    approved_submissions = (
        submissions_collection.count_documents(
            {"outcome": "Approved"}
        )
    )

    blocked_submissions = (
        submissions_collection.count_documents(
            {"outcome": "Blocked"}
        )
    )

    flagged_submissions = (
        submissions_collection.count_documents(
            {"outcome": "Flagged"}
        )
    )

    total_appeals = (
        appeals_collection.count_documents({})
    )

    approved_appeals = (
        appeals_collection.count_documents(
            {"status": "Approved"}
        )
    )

    rejected_appeals = (
        appeals_collection.count_documents(
            {"status": "Rejected"}
        )
    )

    pending_appeals = (
        appeals_collection.count_documents(
            {"status": "Pending"}
        )
    )

    top_submitters = list(
        submissions_collection.aggregate([
            {
                "$group": {
                    "_id": "$email",
                    "submission_count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "submission_count": -1
                }
            },
            {
                "$limit": 5
            }
        ])
    )

    top_violators = list(
        submissions_collection.aggregate([
            {
                "$match": {
                    "outcome": {
                        "$ne": "Approved"
                    }
                }
            },
            {
                "$group": {
                    "_id": "$email",
                    "violation_count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "violation_count": -1
                }
            },
            {
                "$limit": 5
            }
        ])
    )

    graphic_violence_detections = 0

    submissions = list(
        submissions_collection.find({})
    )

    for submission in submissions:

        verdicts = submission.get(
            "verdicts",
            []
        )

        for verdict in verdicts:

            categories = verdict.get(
                "categories",
                []
            )

            for category in categories:

                if (
                    category.get("category")
                    == "Graphic Violence"
                    and category.get("result")
                ):
                    graphic_violence_detections += 1

    return {
        "total_users": total_users,
        "total_submissions": total_submissions,
        "approved_submissions": approved_submissions,
        "blocked_submissions": blocked_submissions,
        "flagged_submissions": flagged_submissions,
        "total_appeals": total_appeals,
        "approved_appeals": approved_appeals,
        "rejected_appeals": rejected_appeals,
        "pending_appeals": pending_appeals,
        "graphic_violence_detections":
            graphic_violence_detections,
        "top_submitters": top_submitters,
        "top_violators": top_violators
    }