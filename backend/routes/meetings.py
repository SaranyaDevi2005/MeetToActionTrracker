from fastapi import APIRouter, HTTPException

from models.schemas import TaskUpdateRequest
from database.mongo import meetings_collection
from services.chromadb_service import store_action_items

router = APIRouter()


def _serialize(meeting):
    return meeting


@router.get("/meeting/{meeting_id}")
async def get_meeting(meeting_id: str):
    meeting = meetings_collection.find_one({"meeting_id": meeting_id})
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return _serialize(meeting)


@router.get("/meetings")
async def list_meetings(search: str = ""):
    query = {}
    if search:
        query = {"title": {"$regex": search, "$options": "i"}}
    meetings = list(meetings_collection.find(query).sort("upload_date", -1))
    return [_serialize(m) for m in meetings]


@router.put("/task")
async def update_task(payload: TaskUpdateRequest):
    meeting = meetings_collection.find_one({"meeting_id": payload.meeting_id})
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    action_items = meeting.get("action_items", [])
    if payload.task_index < 0 or payload.task_index >= len(action_items):
        raise HTTPException(status_code=400, detail="Invalid task index")

    item = action_items[payload.task_index]
    if payload.owner is not None:
        item["owner"] = payload.owner
    if payload.task is not None:
        item["task"] = payload.task
    if payload.deadline is not None:
        item["deadline"] = payload.deadline
    if payload.approved is not None:
        item["approved"] = payload.approved

    meetings_collection.update_one(
        {"meeting_id": payload.meeting_id}, {"$set": {"action_items": action_items}}
    )

    try:
        store_action_items(
            meeting_id=payload.meeting_id,
            meeting_title=meeting.get("title", ""),
            action_items=action_items,
        )
    except RuntimeError:
        pass  # non-critical - chat search will just use slightly stale data

    return {"status": "updated", "task": item}


@router.delete("/task/{meeting_id}/{task_index}")
async def delete_task(meeting_id: str, task_index: int):
    meeting = meetings_collection.find_one({"meeting_id": meeting_id})
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    action_items = meeting.get("action_items", [])
    if task_index < 0 or task_index >= len(action_items):
        raise HTTPException(status_code=400, detail="Invalid task index")

    action_items.pop(task_index)
    meetings_collection.update_one(
        {"meeting_id": meeting_id}, {"$set": {"action_items": action_items}}
    )
    return {"status": "deleted"}