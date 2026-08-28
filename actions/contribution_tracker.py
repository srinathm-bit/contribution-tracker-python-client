from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Union
from database import get_db_connection

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
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO contributions (event_id, amount, name, address, mobile_number)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                contribution.event_id,
                contribution.amount,
                contribution.name,
                contribution.address,
                str(contribution.mobile_number) if contribution.mobile_number is not None else None
            ))
            contrib_id = cursor.lastrowid
        conn.close()
        return {
            "status": True,
            "message": "Contribution registered successfully",
            "id": contrib_id,
            "event_id": contribution.event_id,
            "amount": contribution.amount,
            "name": contribution.name,
            "address": contribution.address,
            "mobile_number": contribution.mobile_number
        }
    except Exception as e:
        return {"status": False, "message": f"registration failed: {str(e)}"}


@router.delete("/{contribution_id}")
def delete_contribution(contribution_id: int):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM contributions WHERE id = %s", (contribution_id,))
            affected = cursor.rowcount
        conn.close()
        if affected > 0:
            return {"status": True, "message": "Contribution deleted successfully", "id": contribution_id}
        else:
            return {"status": False, "status_code": 404, "message": "failed to delete contribution"}
    except Exception as e:
        return {"status": False, "status_code": 500, "message": f"failed to delete contribution: {str(e)}"}


@router.get("/{contribution_id}")
def read_one_contribution(contribution_id: int):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM contributions WHERE id = %s", (contribution_id,))
            contrib = cursor.fetchone()
        conn.close()
        if contrib:
            return contrib
        else:
            return {"status": False, "message": "failed to read contribution"}
    except Exception as e:
        return {"status": False, "message": f"failed to read contribution: {str(e)}"}


@router.get("/read_all/{event_id}")
def read_all_contributions(event_id: str):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, event_id, name, address, amount, mobile_number FROM contributions WHERE event_id = %s ORDER BY id ASC", (event_id,))
            contributions = cursor.fetchall()
        conn.close()
        return contributions
    except Exception as e:
        return {"status": False, "message": f"failed to read contributions: {str(e)}"}



@router.put("/{contribution_id}")
def update_contributions_report(contribution_id: int, contribution: ContributionUpdateSchema):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                UPDATE contributions
                SET event_id = %s, name = %s, address = %s, amount = %s, mobile_number = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                contribution.event_id,
                contribution.name,
                contribution.address,
                contribution.amount,
                str(contribution.mobile_number),
                contribution_id
            ))
            affected = cursor.rowcount
        conn.close()
        if affected > 0:
            return {
                "status": True,
                "message": "Contribution updated successfully",
                "id": contribution_id,
                "event_id": contribution.event_id,
                "name": contribution.name,
                "address": contribution.address,
                "amount": contribution.amount,
                "mobile_number": str(contribution.mobile_number)
            }
        else:
            return {"status": False, "message": "Failed to update contribution"}
    except Exception as e:
        return {"status": False, "message": f"Failed to update contribution: {str(e)}"}