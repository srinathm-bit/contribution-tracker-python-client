from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import requests
from config import BASE_URL

router = APIRouter(prefix="/event", tags=["Event Tracker"])


class EventRegistrationSchema(BaseModel):
    name: str
    date: str
    location: str
    user_id: int


@router.post("/event_registration")
def event_registration(event: EventRegistrationSchema):
    url = f"{BASE_URL}/event/event_registration"
    body_data = event.model_dump()
    response = requests.post(url, json=body_data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "registration failed"}


@router.get("/{event_id}")
def read_one_event(event_id: int):
    url = f"{BASE_URL}/event/{event_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "failed to read event"}


@router.delete("/{event_id}")
def delete_event(event_id: int):
    url = f"{BASE_URL}/event/{event_id}"
    response = requests.delete(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "failed to delete event"}


@router.get("/")
def read_all_events():
    url = f"{BASE_URL}/event/"
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        event_list = [["id", "user_id", "name", "date", "location"]]
        for event in json_response:
            event_list.append([
                str(event.get("id", "")),
                str(event.get("user_id", "")),
                str(event.get("name", "")),
                str(event.get("date", "")),
                str(event.get("location", ""))
            ])
        return event_list
    else:
        return {"status": False, "message": "failed to read events"}
