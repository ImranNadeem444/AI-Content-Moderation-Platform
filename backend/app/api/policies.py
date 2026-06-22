from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.auth.dependencies import get_current_user
from app.database.collections import policies_collection

router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)


@router.get("/")
def get_policies():

    policies = list(
        policies_collection.find()
    )

    for policy in policies:
        policy["_id"] = str(
            policy["_id"]
        )

    return policies


@router.put("/{category}")
def update_policy(
    category: str,
    enabled: bool,
    threshold: float,
    action: str,
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    policies_collection.update_one(
        {
            "category": category
        },
        {
            "$set": {
                "category": category,
                "enabled": enabled,
                "threshold": threshold,
                "action": action
            }
        },
        upsert=True
    )

    return {
        "message": "Policy updated successfully",
        "category": category
    }