from fastapi import APIRouter, HTTPException

from models.schemas import CalendarCreateRequest
from services.scheduler_service import schedule_task_reminders
from config.employees import get_employee_email
from database.mongo import meetings_collection, calendar_events_collection

router = APIRouter()


@router.post("/calendar/create")
async def create_event(payload: CalendarCreateRequest):
    meeting = meetings_collection.find_one({"meeting_id": payload.meeting_id})
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    action_items = meeting.get("action_items", [])
    if payload.task_index < 0 or payload.task_index >= len(action_items):
        raise HTTPException(status_code=400, detail="Invalid task index")

    item = action_items[payload.task_index]
    if not item.get("approved"):
        raise HTTPException(status_code=400, detail="Task must be approved before scheduling reminders")
    if not item.get("deadline"):
        raise HTTPException(status_code=400, detail="Task has no deadline set")

    owner_email = item.get("owner_email") or get_employee_email(item.get("owner"))
    if not owner_email:
        raise HTTPException(status_code=400, detail=f"No email found for owner '{item.get('owner')}'. Add it in employees.py or the Owner Email field.")

    try:
        jobs = schedule_task_reminders(
            owner_email=owner_email,
            task_title=item["task"],
            deadline=item["deadline"],
            meeting_name=meeting.get("title", ""),
            owner_name=item["owner"],
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    item["calendar_event_id"] = "scheduled"
    item["owner_email"] = owner_email
    meetings_collection.update_one(
        {"meeting_id": payload.meeting_id}, {"$set": {"action_items": action_items}}
    )

    calendar_events_collection.insert_one(
        {
            "meeting_id": payload.meeting_id,
            "task_index": payload.task_index,
            "task": item["task"],
            "reminders_scheduled": jobs,
        }
    )

    return {"status": "scheduled", "reminders": jobs}