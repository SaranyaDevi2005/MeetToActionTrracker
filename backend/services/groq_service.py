import json
from groq import Groq
from config.settings import settings

client = Groq(api_key=settings.GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"

ANALYSIS_PROMPT = """You are a meeting analysis assistant. Read the meeting transcript below and
extract structured information. Respond with ONLY valid JSON, no markdown, no preamble.

Return JSON in exactly this format:
{{
  "summary": "short summary of the meeting",
  "participants": ["name1", "name2"],
  "action_items": [
    {{"owner": "name", "task": "task description", "deadline": "YYYY-MM-DDTHH:MM:SS or null"}}
  ],
  "decisions": ["decision 1", "decision 2"]
}}

Transcript:
{transcript}
"""


def analyze_transcript(transcript: str) -> dict:
    """Send transcript to Groq LLM and return structured meeting data."""
    if not transcript or not transcript.strip():
        raise ValueError("Empty transcript cannot be analyzed")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": ANALYSIS_PROMPT.format(transcript=transcript)}
            ],
            temperature=0.2,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
        return data
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Groq returned invalid JSON: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Groq API failed: {str(e)}")


def answer_query(query: str, context_chunks: list) -> str:
    """RAG: answer a user question using retrieved transcript chunks as context."""
    context_text = "\n\n".join(context_chunks) if context_chunks else "No relevant context found."

    prompt = f"""You are an assistant answering questions about past meetings.
Use ONLY the context below to answer. If the answer isn't in the context, say you don't have that information.

Context:
{context_text}

Question: {query}

Answer:"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq API failed: {str(e)}")