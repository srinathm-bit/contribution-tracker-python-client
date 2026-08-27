from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import requests
import json
from config import BASE_URL

router = APIRouter(prefix="/user", tags=["User Tracker"])


class UserRegistrationSchema(BaseModel):
    name: str
    email: str
    dob: Optional[str] = None
    address: Optional[str] = None
    mobile_number: Optional[str] = None


@router.post("/user_registration")
def user_registration(user: UserRegistrationSchema):
    url = f"{BASE_URL}/user/user_registration"
    body_data = user.model_dump()
    response = requests.post(url, json=body_data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "registration failed"}


@router.get("/{user_id}")
def read_one_user(user_id: int):
    url = f"{BASE_URL}/user/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "user not found"}


@router.delete("/{user_id}")
def delete_user(user_id: int):
    url = f"{BASE_URL}/user/{user_id}"
    response = requests.delete(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "user not found"}


@router.get("/")
def read_all_users():
    url = f"{BASE_URL}/user/"
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        users_list = [["id", "name", "dob", "email", "address", "mobile_number"]]
        for user in json_response:
            users_list.append([
                str(user.get("id", "")),
                str(user.get("name", "")),
                str(user.get("dob", "")),
                str(user.get("email", "")),
                str(user.get("address", "")),
                str(user.get("mobile_number", ""))
            ])
        return users_list
    return {"status": False, "message": "failed to read users"}
