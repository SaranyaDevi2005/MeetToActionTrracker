# NoteToAction — Agentic Meeting Assistant

An **agentic AI meeting assistant** that converts meeting conversations into structured, actionable tasks and helps automate follow-ups using **LLMs, RAG, tool calling, and human-in-the-loop approval**.

## 🚀 Overview

NoteToAction transforms unstructured meeting audio into actionable information.

**Meeting Audio → Speech-to-Text → Task Extraction → RAG → Validation → Human Approval → Tool Execution**

The system identifies:

* Tasks and action items
* Task owners
* Deadlines
* Relevant meeting context
* Follow-up requirements

Approved tasks can trigger automated actions such as **email notifications and task scheduling**.

## 🏗️ Architecture

```text
                Meeting Audio
                      │
                      ▼
             ┌─────────────────┐
             │ Whisper / STT    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ LLM Extraction  │
             │ Llama 3.3/Groq  │
             └────────┬────────┘
                      │
             Structured Tasks
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   ┌─────────────┐        ┌──────────────┐
   │ ChromaDB    │        │ Validation   │
   │ RAG         │        │ Pydantic     │
   └──────┬──────┘        └──────┬───────┘
          │                       │
          └───────────┬───────────┘
                      ▼
              Human Approval
                      │
                      ▼
             ┌─────────────────┐
             │ Tool Execution  │
             │ Email / Tasks   │
             └─────────────────┘
```

## ✨ Key Features

* 🎙️ **Audio transcription** using Whisper
* 🤖 **LLM-powered task extraction** using Llama 3.3 via Groq
* 🔎 **RAG with ChromaDB** for retrieving relevant meeting context
* 🧠 **Agentic workflow** for deciding when retrieval and actions are required
* ✅ **Structured output validation** using Pydantic
* 👤 **Human-in-the-loop approval** before executing important actions
* 📧 **Automated email notifications** for approved tasks
* 🗂️ **State management** for tracking tasks and workflow progress
* 📊 **RAG evaluation using RAGAS**

## 🛠️ Tech Stack

### AI / ML

* Python
* Llama 3.3
* Groq API
* Whisper
* RAG
* ChromaDB
* RAGAS

### Backend

* FastAPI
* Pydantic
* Python

### Frontend

* React
* Vite
* Tailwind CSS

### Database / Storage

* ChromaDB
* MongoDB

## 🔄 Agentic Workflow

The system follows an agent-style workflow:

1. **Ingest** meeting audio.
2. **Transcribe** audio using Whisper.
3. **Analyze** the transcript using an LLM.
4. **Extract** structured tasks, owners and deadlines.
5. **Retrieve** relevant context from previous meeting information using ChromaDB.
6. **Validate** the generated structured output using Pydantic.
7. **Request human approval** for actions.
8. **Execute tools** such as sending notifications or scheduling follow-ups.
9. **Store state** so tasks and actions can be tracked.

This approach prevents the LLM from directly triggering potentially incorrect actions.

## 🧩 RAG Pipeline

The RAG component stores meeting information as embeddings in **ChromaDB**.

```text
Meeting Data
     ↓
Chunking
     ↓
Embeddings
     ↓
ChromaDB
     ↓
Semantic Retrieval
     ↓
Relevant Context
     ↓
LLM
     ↓
Grounded Response / Task
```

RAG is used to provide the agent with relevant historical meeting context instead of relying only on the current conversation.

## 📈 Evaluation

I used **RAGAS** to evaluate the RAG pipeline, focusing on metrics such as:

* **Context Relevancy**
* **Context Recall**
* **Faithfulness**
* **Answer Relevancy**

The evaluation helped identify retrieval problems and improve the quality of context provided to the LLM.

## 🧠 Hardest Engineering Problem

The biggest challenge was making LLM-generated output reliable enough for downstream automation.

Initially, the model could produce inconsistent task formats, missing fields, or ambiguous deadlines. Directly passing this output to automation tools could result in incorrect actions.

I addressed this using:

* Structured prompting
* Pydantic schemas
* Output validation
* RAG-based context retrieval
* Explicit workflow states
* Human approval before tool execution

This created a safer pipeline where the LLM assists with reasoning, while deterministic validation and human approval control execution.

## 📁 Project Structure

```text
NoteToAction/
│
├── backend/
│   ├── api/
│   ├── agents/
│   ├── rag/
│   ├── tools/
│   ├── models/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   └── App.jsx
│
├── evaluation/
│   └── ragas_evaluation.py
│
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/NoteToAction.git
cd NoteToAction
```

### 2. Create environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_uri
```

### 5. Start the backend

```bash
uvicorn backend.main:app --reload
```

### 6. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

## 🔐 Security

API keys and credentials are stored using environment variables and are **not committed to the repository**.

Add `.env` to `.gitignore`:

```text
.env
venv/
__pycache__/
node_modules/
```

## 🔮 Future Improvements

* Google Calendar integration
* More autonomous tool selection
* Multi-agent task planning
* Better long-term memory
* Improved RAG evaluation datasets
* Authentication and role-based access
* Production deployment using Docker

## 👩‍💻 Author

**Saranya Devi S**

MSc Decision and Computing Sciences
Interested in **AI/ML, RAG systems, agentic AI, and data-driven applications**.
