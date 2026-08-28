from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
import requests
from config import BASE_URL

router = APIRouter(prefix="/analytics", tags=["Analytics"])


class TopContributor(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None


class EventSummarySchema(BaseModel):
    total_contributions_count: int
    total_amount_raised: float
    average_contribution: float
    top_contributor: Optional[TopContributor] = None


@router.get("/event/{event_id}/summary", response_model=EventSummarySchema)
def event_contribution_summary(event_id: int):
    url = f"{BASE_URL}/contribution/read_all/{event_id}"

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException:
        # Backend unreachable/timed out — degrade to an empty summary
        # rather than raising a 500.
        return EventSummarySchema(
            total_contributions_count=0,
            total_amount_raised=0,
            average_contribution=0,
            top_contributor=None
        )

    if response.status_code != 200:
        # No contributions found, or backend has nothing for this event —
        # treat as an empty result rather than an error.
        return EventSummarySchema(
            total_contributions_count=0,
            total_amount_raised=0,
            average_contribution=0,
            top_contributor=None
        )

    contributions = response.json()

    if not contributions:
        return EventSummarySchema(
            total_contributions_count=0,
            total_amount_raised=0,
            average_contribution=0,
            top_contributor=None
        )

    amounts = [contribution.get("amount", 0) or 0 for contribution in contributions]

    total_contributions_count = len(contributions)
    total_amount_raised = sum(amounts)
    average_contribution = total_amount_raised / total_contributions_count

    top_contribution = max(contributions, key=lambda contribution: contribution.get("amount", 0) or 0)

    return EventSummarySchema(
        total_contributions_count=total_contributions_count,
        total_amount_raised=total_amount_raised,
        average_contribution=round(average_contribution, 2),
        top_contributor=TopContributor(
            name=top_contribution.get("name"),
            amount=top_contribution.get("amount")
        )
    )