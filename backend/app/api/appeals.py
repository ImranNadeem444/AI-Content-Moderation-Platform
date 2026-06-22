from datetime import datetime

from bson import ObjectId

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.auth.dependencies import get_current_user

from app.schemas.appeal import AppealCreate

from app.database.collections import (
    appeals_collection,
    submissions_collection
)

router = APIRouter(
    prefix="/appeals",
    tags=["Appeals"]
)


@router.get("/")
def test_appeals():
    return {
        "message": "Appeals API Working"
    }


@router.post("/create")
def create_appeal(
    appeal: AppealCreate,
    current_user=Depends(get_current_user)
):

    appeal_data = {
        "submission_id": appeal.submission_id,
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "reason": appeal.reason,
        "status": "Pending",
        "admin_response": "",
        "created_at": datetime.utcnow()
    }

    result = appeals_collection.insert_one(
        appeal_data
    )

    return {
        "message": "Appeal submitted successfully",
        "appeal_id": str(result.inserted_id),
        "status": "Pending",
        "user": current_user["email"]
    }


@router.get("/my")
def get_my_appeals(
    current_user=Depends(get_current_user)
):

    appeals = list(
        appeals_collection.find(
            {
                "user_id": current_user["user_id"]
            }
        )
    )

    for appeal in appeals:
        appeal["_id"] = str(
            appeal["_id"]
        )

    return appeals


@router.get("/all")
def get_all_appeals(
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    appeals = list(
        appeals_collection.find()
    )

    for appeal in appeals:
        appeal["_id"] = str(
            appeal["_id"]
        )

    return appeals


@router.put("/{appeal_id}/approve")
def approve_appeal(
    appeal_id: str,
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    appeal = appeals_collection.find_one(
        {
            "_id": ObjectId(appeal_id)
        }
    )

    if not appeal:
        raise HTTPException(
            status_code=404,
            detail="Appeal not found"
        )

    appeals_collection.update_one(
        {
            "_id": ObjectId(appeal_id)
        },
        {
            "$set": {
                "status": "Approved",
                "admin_response": "Appeal accepted after review."
            }
        }
    )

    submissions_collection.update_one(
        {
            "_id": ObjectId(
                appeal["submission_id"]
            )
        },
        {
            "$set": {
                "outcome": "Approved"
            }
        }
    )

    return {
        "message": "Appeal approved"
    }


@router.put("/{appeal_id}/reject")
def reject_appeal(
    appeal_id: str,
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    result = appeals_collection.update_one(
        {
            "_id": ObjectId(appeal_id)
        },
        {
            "$set": {
                "status": "Rejected",
                "admin_response": "Appeal rejected after review."
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Appeal not found"
        )

    return {
        "message": "Appeal rejected"
    }