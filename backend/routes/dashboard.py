import datetime
from fastapi import APIRouter

from database.mongo import meetings_collection

router = APIRouter()


@router.get("/dashboard")
async def dashboard():
    meetings = list(meetings_collection.find({}))

    total_meetings = len(meetings)
    pending_tasks = 0
    completed_tasks = 0
    upcoming_deadlines = []

    now = datetime.datetime.utcnow()

    for m in meetings:
        for item in m.get("action_items", []):
            if item.get("calendar_event_id"):
                completed_tasks += 1
            else:
                pending_tasks += 1

            deadline = item.get("deadline")
            if deadline:
                try:
                    dt = datetime.datetime.fromisoformat(deadline)
                    if dt > now:
                        upcoming_deadlines.append(
                            {"task": item.get("task"), "owner": item.get("owner"), "deadline": deadline}
                        )
                except ValueError:
                    continue

    upcoming_deadlines.sort(key=lambda x: x["deadline"])

    return {
        "total_meetings": total_meetings,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "upcoming_deadlines": upcoming_deadlines[:10],
    }