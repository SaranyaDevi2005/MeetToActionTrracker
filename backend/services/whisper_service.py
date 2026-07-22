import whisper
from config.settings import settings

_model = None


def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model(settings.WHISPER_MODEL)
    return _model


def transcribe_audio(file_path: str) -> str:
    """Transcribe an audio file and return the full text transcript."""
    try:
        model = get_model()
        result = model.transcribe(file_path)
        transcript = result.get("text", "").strip()
        if not transcript:
            raise ValueError("Transcription returned empty text")
        return transcript
    except Exception as e:
        raise RuntimeError(f"Whisper transcription failed: {str(e)}")