from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Union
import requests
from config import BASE_URL

router = APIRouter(prefix="/contribution", tags=["Contribution Tracker"])


class ContributionRegistrationSchema(BaseModel):
    event_id: int
    amount: int
    name: Optional[str] = None
    address: Optional[str] = None
    mobile_number: Optional[str] = None


class ContributionUpdateSchema(BaseModel):
    event_id: int
    name: str
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