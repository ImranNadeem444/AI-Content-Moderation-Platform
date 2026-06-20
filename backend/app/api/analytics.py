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

    rejected_submissions = (
        submissions_collection.count_documents(
            {"outcome": "Rejected"}
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

    return {
        "total_users": total_users,
        "total_submissions": total_submissions,
        "approved_submissions": approved_submissions,
        "rejected_submissions": rejected_submissions,
        "total_appeals": total_appeals,
        "approved_appeals": approved_appeals,
        "rejected_appeals": rejected_appeals,
        "pending_appeals": pending_appeals
    }