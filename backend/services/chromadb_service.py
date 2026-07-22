import chromadb
from config.settings import settings

chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
collection = chroma_client.get_or_create_collection(name="meeting_chunks")


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list:
    """Simple sliding-window chunker."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c for c in chunks if c.strip()]


def store_transcript(meeting_id: str, meeting_title: str, transcript: str,
                      participants: list, upload_date: str):
    """Chunk transcript, embed (Chroma default embedding fn) and store with metadata."""
    try:
        chunks = chunk_text(transcript)
        ids = [f"{meeting_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "meeting_id": meeting_id,
                "meeting_title": meeting_title,
                "upload_date": upload_date,
                "participants": ", ".join(participants),
            }
            for _ in chunks
        ]
        collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    except Exception as e:
        raise RuntimeError(f"ChromaDB storage failed: {str(e)}")


def search_chunks(query: str, top_k: int = 5) -> list:
    """Search for the most relevant transcript chunks for a query."""
    try:
        results = collection.query(query_texts=[query], n_results=top_k)
        docs = results.get("documents", [[]])[0]
        return docs
    except Exception as e:
        raise RuntimeError(f"ChromaDB retrieval failed: {str(e)}")
task_collection = chroma_client.get_or_create_collection(name="task_assignments")


def store_action_items(meeting_id: str, meeting_title: str, action_items: list):
    """Store each action item as its own searchable document, so chat can
    answer questions like 'who is doing X' or 'what's due this week'."""
    if not action_items:
        return

    try:
        documents = []
        ids = []
        metadatas = []

        for i, item in enumerate(action_items):
            owner = item.get("owner", "Unassigned")
            task = item.get("task", "")
            deadline = item.get("deadline", "No deadline set")

            # Plain-English sentence so the embedding captures the full meaning
            doc_text = (
                f"{owner} is responsible for: {task}. "
                f"Deadline: {deadline}. From meeting: {meeting_title}."
            )

            documents.append(doc_text)
            ids.append(f"{meeting_id}_task_{i}")
            metadatas.append(
                {
                    "meeting_id": meeting_id,
                    "meeting_title": meeting_title,
                    "owner": owner,
                    "deadline": deadline or "",
                }
            )

        task_collection.upsert(documents=documents, ids=ids, metadatas=metadatas)
    except Exception as e:
        raise RuntimeError(f"ChromaDB task storage failed: {str(e)}")


def search_tasks(query: str, top_k: int = 5) -> list:
    """Search stored task assignments for relevant matches."""
    try:
        results = task_collection.query(query_texts=[query], n_results=top_k)
        docs = results.get("documents", [[]])[0]
        return docs
    except Exception as e:
        raise RuntimeError(f"ChromaDB task retrieval failed: {str(e)}")