from fastapi import APIRouter, HTTPException

from models.schemas import AnalyzeRequest
from services.groq_service import analyze_transcript

from database.mongo import meetings_collection
from services.chromadb_service import store_transcript, store_action_items

router = APIRouter()


@router.post("/analyze")
async def analyze(payload: AnalyzeRequest):
    meeting = meetings_collection.find_one({"meeting_id": payload.meeting_id})
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if not payload.transcript or not payload.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript is empty")

    try:
        analysis = analyze_transcript(payload.transcript)
    except (RuntimeError, ValueError) as e:
        raise HTTPException(status_code=500, detail=str(e))

    for item in analysis.get("action_items", []):
        item["approved"] = False
        item["calendar_event_id"] = None

    meetings_collection.update_one(
        {"meeting_id": payload.meeting_id},
        {
            "$set": {
                "summary": analysis.get("summary", ""),
                "participants": analysis.get("participants", []),
                "decisions": analysis.get("decisions", []),
                "action_items": analysis.get("action_items", []),
            }
        },
    )

    try:
        store_transcript(
            meeting_id=payload.meeting_id,
            meeting_title=meeting.get("title", ""),
            transcript=payload.transcript,
            participants=analysis.get("participants", []),
            upload_date=meeting.get("upload_date", ""),
        )
        store_action_items(
            meeting_id=payload.meeting_id,
            meeting_title=meeting.get("title", ""),
            action_items=analysis.get("action_items", []),
        )
    except RuntimeError as e:
        return {"meeting_id": payload.meeting_id, "analysis": analysis, "warning": str(e)}
    return {"meeting_id": payload.meeting_id, "analysis": analysis}
