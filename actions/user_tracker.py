from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/user", tags=["User Tracker"])


class UserRegistrationSchema(BaseModel):
    name: str
    email: str
    dob: Optional[str] = None
    address: Optional[str] = None
    mobile_number: Optional[str] = None


@router.post("/user_registration")
def user_registration(user: UserRegistrationSchema):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO users (name, email, dob, address, mobile_number)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                user.name,
                user.email,
                user.dob,
                user.address,
                user.mobile_number
            ))
            user_id = cursor.lastrowid
        conn.close()
        return {
            "status": True,
            "message": "User registered successfully",
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "dob": user.dob,
            "address": user.address,
            "mobile_number": user.mobile_number
        }
    except Exception as e:
        return {"status": False, "message": f"registration failed: {str(e)}"}


@router.get("/{user_id}")
def read_one_user(user_id: int):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
        conn.close()
        if user:
            return user
        else:
            return {"status": False, "message": "user not found"}
    except Exception as e:
        return {"status": False, "message": f"user not found: {str(e)}"}


@router.delete("/{user_id}")
def delete_user(user_id: int):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            affected = cursor.rowcount
        conn.close()
        if affected > 0:
            return {"status": True, "message": "User deleted successfully", "id": user_id}
        else:
            return {"status": False, "message": "user not found"}
    except Exception as e:
        return {"status": False, "message": f"user delete failed: {str(e)}"}


@router.get("/")
def read_all_users():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, dob, email, address, mobile_number FROM users ORDER BY id ASC")
            users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        return {"status": False, "message": f"failed to read users: {str(e)}"}

