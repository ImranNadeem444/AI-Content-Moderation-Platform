import random

from app.database.collections import policies_collection


def analyze_image(image_path: str):

    categories = []

    overall_outcome = "Approved"

    policies = list(
        policies_collection.find()
    )

    if not policies:

        return {
            "overall_outcome": "Approved",
            "categories": [
                {
                    "category": "Graphic Violence",
                    "result": False,
                    "confidence": 0.05,
                    "reason": "No policies configured"
                }
            ]
        }

    for policy in policies:

        if not policy.get("enabled", True):
            continue

        confidence = round(
            random.uniform(0.0, 1.0),
            2
        )

        detected = (
            confidence >= policy["threshold"]
        )

        reason = (
            f"Confidence score: {confidence}"
        )

        categories.append(
            {
                "category": policy["category"],
                "result": detected,
                "confidence": confidence,
                "reason": reason
            }
        )

        if detected:

            if policy["action"] == "Auto-Block":
                overall_outcome = "Blocked"

            elif (
                policy["action"] == "Flag for Review"
                and overall_outcome != "Blocked"
            ):
                overall_outcome = "Flagged"

    return {
        "overall_outcome": overall_outcome,
        "categories": categories
    }