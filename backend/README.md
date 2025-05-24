
# Multi-Agent Streaming Chatbot Backend

**Author:** Mohitkumar Mahto  
**Date:** Tuesday, May 13, 2025

This repository contains the **FastAPI backend** for a multi-agent chatbot application.  
It orchestrates several specialized AI agents (Legal, Finance, Marketing, Engineering) using OpenAI's GPT models and streams their analyses in real-time to the frontend.

---

## 🚀 Features

- **Multi-agent orchestration:** Each agent provides a unique perspective on the user's scenario.
- **Streaming responses:** Uses FastAPI's `StreamingResponse` for real-time data delivery.
- **OpenAI integration:** Agents are powered by GPT models via the OpenAI API.
- **Environment-based configuration:** API keys and secrets are managed securely.
- **Ready for frontend integration:** Works seamlessly with React/Next.js or any frontend that supports streaming.

---

## 📦 Project Structure

```
app/
  agents/
    base.py           # Base agent class (OpenAI integration)
    legal.py          # LegalAgent definition
    finance.py        # FinanceAgent definition
    marketing.py      # MarketingAgent definition
    engineering.py    # EngineeringAgent definition
  services/
    orchestrator.py   # Orchestrates agent responses (incl. streaming)
  schemas.py          # Pydantic models for requests/responses
  main.py             # FastAPI app entrypoint
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/multi-agent-chatbot-backend.git
cd multi-agent-chatbot-backend
```

### 2. Create a virtual environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

**Sample `requirements.txt`:**
```
fastapi
uvicorn
openai
python-dotenv
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
```

### 5. Run the FastAPI server

```
uvicorn app.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

## 🔑 API Usage

### `POST /analyze-stream`

**Description:**  
Streams analyses from all agents for a given scenario.

**Request Body (JSON):**
```
{
  "scenario": "Describe your business scenario here."
}
```

**Response:**  
A plain text stream. Each agent's analysis is sectioned, e.g.:

```
--- Legal Analysis ---
[Legal agent's streaming response]

--- Finance Analysis ---
[Finance agent's streaming response]

--- Marketing Analysis ---
[Marketing agent's streaming response]

--- Engineering Analysis ---
[Engineering agent's streaming response]
```

**Example with `curl`:**
```
curl -N -X POST http://localhost:8000/analyze-stream \
  -H "Content-Type: application/json" \
  -d '{"scenario": "Launching a fintech app in Europe."}'
```

---

## 🛡️ CORS Configuration

If your frontend runs on a different origin (e.g., `localhost:3000` for Next.js),  
CORS is enabled in `main.py`:

```
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧠 Code Overview

### Agent Example (`app/agents/legal.py`)
```
from app.agents.base import BaseAgent

class LegalAgent(BaseAgent):
    def __init__(self):
        super().__init__("Legal", "Provide a legal analysis of the user's scenario.")
```

### Streaming Orchestrator (`app/services/orchestrator.py`)
```
from app.agents.legal import LegalAgent
# ... other imports

def stream_all_agents(scenario: str):
    agents = [LegalAgent(), FinanceAgent(), MarketingAgent(), EngineeringAgent()]
    for agent in agents:
        yield f"\n--- {agent.role} Analysis ---\n"
        for chunk in agent.stream_respond(scenario):
            yield chunk
```

### FastAPI Streaming Endpoint (`app/main.py`)
```
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.services.orchestrator import stream_all_agents
from app.schemas import ScenarioRequest

app = FastAPI()

@app.post("/analyze-stream")
async def analyze_stream(scenario: ScenarioRequest):
    def event_stream():
        yield from stream_all_agents(scenario.scenario)
    return StreamingResponse(event_stream(), media_type="text/plain")
```

---

## 📝 Tips

- **Keep your API key secret:** Never commit `.env` files or API keys to version control.
- **Error handling:** Add try/except blocks for production use, especially around API calls.
- **Streaming:** The backend streams data as soon as it’s generated for a responsive frontend experience.

---



## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

