from fastapi import APIRouter, HTTPException

from models.schemas import ChatRequest
from services.chromadb_service import search_chunks, search_tasks
from services.groq_service import answer_query

router = APIRouter()


@router.post("/chat")
async def chat(payload: ChatRequest):
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        transcript_chunks = search_chunks(payload.query)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        task_chunks = search_tasks(payload.query)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Combine both sources - task assignments first since they're usually more precise for "who/when" questions
    combined_chunks = task_chunks + transcript_chunks

    try:
        answer = answer_query(payload.query, combined_chunks)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"answer": answer, "sources_used": len(combined_chunks)}