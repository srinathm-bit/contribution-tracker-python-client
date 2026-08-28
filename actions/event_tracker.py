from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

router = APIRouter(prefix="/event", tags=["Event Tracker"])


class EventRegistrationSchema(BaseModel):
    name: str
    date: str
    location: str
    user_id: int


@router.post("/event_registration")
def event_registration(event: EventRegistrationSchema):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO events (user_id, name, date, location)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                event.user_id,
                event.name,
                event.date,
                event.location
            ))
            event_id = cursor.lastrowid
        conn.close()
        return {
            "status": True,
            "message": "Event registered successfully",
            "id": event_id,
            "user_id": event.user_id,
            "name": event.name,
            "date": event.date,
            "location": event.location
        }
    except Exception as e:
        return {"status": False, "message": f"registration failed: {str(e)}"}


@router.get("/{event_id}")
def read_one_event(event_id: int):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            event = cursor.fetchone()
        conn.close()
        if event:
            return event
        else:
            return {"status": False, "message": "failed to read event"}
    except Exception as e:
        return {"status": False, "message": f"failed to read event: {str(e)}"}


@router.delete("/{event_id}")
def delete_event(event_id: int):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
            affected = cursor.rowcount
        conn.close()
        if affected > 0:
            return {"status": True, "message": "Event deleted successfully", "id": event_id}
        else:
            return {"status": False, "message": "failed to delete event"}
    except Exception as e:
        return {"status": False, "message": f"failed to delete event: {str(e)}"}


@router.get("/")
def read_all_events():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, user_id, name, date, location FROM events ORDER BY id ASC")
            events = cursor.fetchall()
        conn.close()
        return events
    except Exception as e:
        return {"status": False, "message": f"failed to read events: {str(e)}"}

