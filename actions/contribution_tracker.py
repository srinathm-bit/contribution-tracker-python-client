from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Union
import requests
import csv
import io
import re
from config import BASE_URL
from actions.email_service import send_confirmation_email

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

router = APIRouter(prefix="/contribution", tags=["Contribution Tracker"])


class ContributionRegistrationSchema(BaseModel):
    event_id: int
    amount: int
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    mobile_number: Optional[str] = None


class ContributionUpdateSchema(BaseModel):
    event_id: int
    name: str
    email: Optional[str] = None
    address: str
    amount: int
    mobile_number: Union[str, int]


@router.post("/contributions_registration")
def contribution_registration(contribution: ContributionRegistrationSchema):
    url = f"{BASE_URL}/contribution/contributions_registration"
    body_data = contribution.model_dump()
    response = requests.post(url, json=body_data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "registration failed"}


@router.delete("/{contribution_id}")
def delete_contribution(contribution_id: int):
    url = f"{BASE_URL}/contribution/{contribution_id}"
    response = requests.delete(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "status_code": response.status_code, "message": "failed to delete contribution"}


@router.get("/{contribution_id}")
def read_one_contribution(contribution_id: int):
    url = f"{BASE_URL}/contribution/{contribution_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "failed to read contribution"}


@router.get("/read_all/{event_id}")
def read_all_contributions(event_id: str):
    url = f"{BASE_URL}/contribution/read_all/{event_id}"
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        contribution_list = [["id", "event_id", "name", "address", "amount", "mobile_number"]]

        for contribution in json_response:
            contribution_list.append([
                str(contribution.get("id", "")),
                str(contribution.get("event_id", "")),
                str(contribution.get("name", "")),
                str(contribution.get("address", "")),
                str(contribution.get("amount", "")),
                str(contribution.get("mobile_number", ""))
            ])
        return contribution_list

    return {"status": False, "message": "failed to read contributions"}


@router.get("/report/{event_id}")
def contributions_report(event_id: int):
    url = f"{BASE_URL}/contribution/report/{event_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "failed to read contribution report"}


@router.put("/{contribution_id}")
def update_contributions_report(contribution_id: int, contribution: ContributionUpdateSchema):
    url = f"{BASE_URL}/contribution/{contribution_id}"
    body_data = contribution.model_dump()
    body_data["mobile_number"] = str(body_data["mobile_number"])
    response = requests.put(url, json=body_data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "Failed to update contribution"}


@router.get("/export/{event_id}")
def export_contributions_csv(event_id: int, format: str = "csv"):
    url = f"{BASE_URL}/contribution/read_all/{event_id}"

    try:
        response = requests.get(url, timeout=5)
        contributions = response.json() if response.status_code == 200 else []
    except requests.RequestException:
        contributions = []

    if not isinstance(contributions, list):
        contributions = []

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Contribution ID", "Contributor Name", "Amount", "Mobile Number", "Address"])
    for contribution in contributions:
        writer.writerow([
            contribution.get("id", ""),
            contribution.get("name", ""),
            contribution.get("amount", ""),
            contribution.get("mobile_number", ""),
            contribution.get("address", "")
        ])

    output.seek(0)

    headers = {
        "Content-Disposition": f'attachment; filename="event_{event_id}_report.csv"'
    }
    return StreamingResponse(output, media_type="text/csv", headers=headers)


@router.post("/{contribution_id}/send-email")
def send_contribution_email(contribution_id: int, background_tasks: BackgroundTasks):
    # 1. Fetch the contribution
    contribution_resp = requests.get(f"{BASE_URL}/contribution/{contribution_id}", timeout=5)
    if contribution_resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Contribution not found")
    contribution = contribution_resp.json()

    # 2. Fetch the event it belongs to (for the event name)
    event_id = contribution.get("event_id")
    event = {}
    if event_id is not None:
        event_resp = requests.get(f"{BASE_URL}/event/{event_id}", timeout=5)
        if event_resp.status_code == 200:
            event = event_resp.json()
    event_name = event.get("name", "the event")

    # 3. Work out the contributor's email.
    # ASSUMPTION: the contribution record itself may already carry an "email"
    # field on the real backend even though our ContributionRegistrationSchema
    # doesn't declare one. If it's missing, fall back to the event owner's
    # registered email as a best-effort. Confirm against your real backend
    # response and adjust if this fallback isn't correct for your data model.
    contributor_email = contribution.get("email")
    if not contributor_email:
        user_id = event.get("user_id")
        if user_id is not None:
            user_resp = requests.get(f"{BASE_URL}/user/{user_id}", timeout=5)
            if user_resp.status_code == 200:
                contributor_email = user_resp.json().get("email")

    if not contributor_email or not EMAIL_REGEX.match(contributor_email):
        raise HTTPException(
            status_code=400,
            detail="Contributor does not have a valid email address on file"
        )

    contributor_name = contribution.get("name", "Contributor")
    amount = contribution.get("amount", "")
    contribution_date = (
        contribution.get("date")
        or contribution.get("created_at")
        or contribution.get("registered_at")
        or "N/A"
    )

    # 4. Queue the email as a background task so this response returns immediately
    background_tasks.add_task(
        send_confirmation_email,
        contributor_email,
        contributor_name,
        event_name,
        amount,
        contribution_date
    )

    return {
        "status": True,
        "message": f"Confirmation email queued for {contributor_email}"
    }