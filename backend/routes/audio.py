import os
import uuid
import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException

from config.settings import settings
from services.whisper_service import transcribe_audio
from database.mongo import meetings_collection

router = APIRouter()

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4"}


@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid audio format: {ext}. Allowed: mp3, wav, m4a")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    meeting_id = str(uuid.uuid4())
    saved_path = os.path.join(settings.UPLOAD_DIR, f"{meeting_id}{ext}")

    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        with open(saved_path, "wb") as f:
            f.write(contents)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")

    meeting_doc = {
        "meeting_id": meeting_id,
        "title": file.filename,
        "audio_path": saved_path,
        "transcript": None,
        "summary": None,
        "participants": [],
        "decisions": [],
        "action_items": [],
        "upload_date": datetime.datetime.utcnow().isoformat(),
    }
    meetings_collection.insert_one(meeting_doc)

    return {"meeting_id": meeting_id, "file_path": saved_path}


@router.post("/transcribe")
async def transcribe(meeting_id: str):
    meeting = meetings_collection.find_one({"meeting_id": meeting_id})
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    try:
        transcript = transcribe_audio(meeting["audio_path"])
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    meetings_collection.update_one(
        {"meeting_id": meeting_id}, {"$set": {"transcript": transcript}}
    )

    return {"meeting_id": meeting_id, "transcript": transcript}