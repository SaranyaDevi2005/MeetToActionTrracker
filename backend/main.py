from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import audio, analyze, meetings, calendar, chat, dashboard

app = FastAPI(title="MeetingMind AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio.router, tags=["Audio"])
app.include_router(analyze.router, tags=["Analyze"])
app.include_router(meetings.router, tags=["Meetings"])
app.include_router(calendar.router, tags=["Calendar"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(dashboard.router, tags=["Dashboard"])


@app.get("/")
async def root():
    return {"status": "MeetingMind AI backend is running"}