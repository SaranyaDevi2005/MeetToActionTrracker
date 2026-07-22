from pydantic import BaseModel
from typing import List, Optional


class ActionItem(BaseModel):
    owner: str
    owner_email: Optional[str] = None
    task: str
    deadline: Optional[str] = None
    approved: bool = False
    calendar_event_id: Optional[str] = None

class MeetingAnalysis(BaseModel):
    summary: str
    participants: List[str] = []
    action_items: List[ActionItem] = []
    decisions: List[str] = []


class AnalyzeRequest(BaseModel):
    meeting_id: str
    transcript: str


class CalendarCreateRequest(BaseModel):
    meeting_id: str
    task_index: int


class ChatRequest(BaseModel):
    query: str


class TaskUpdateRequest(BaseModel):
    meeting_id: str
    task_index: int
    owner: Optional[str] = None
    task: Optional[str] = None
    deadline: Optional[str] = None
    approved: Optional[bool] = None