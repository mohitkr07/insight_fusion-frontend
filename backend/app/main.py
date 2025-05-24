# app/main.py
from fastapi import FastAPI, Request
from app.services.orchestrator import run_agents
from app.schemas import ScenarioRequest, ScenarioResponse
import uvicorn
from fastapi.responses import StreamingResponse
from app.schemas import ScenarioRequest
from app.services.orchestrator import stream_all_agents

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}


@app.post("/analyze", response_model=ScenarioResponse)
async def analyze_scenario(scenario: ScenarioRequest):
    result = await run_agents(scenario.scenario)
    return result

@app.post("/analyze-stream")
async def analyze_stream(scenario: ScenarioRequest):
    # agent = LegalAgent()

    # def event_stream():
    #     for chunk in agent.stream_respond(scenario.scenario):
    #         yield chunk

    # return StreamingResponse(event_stream(), media_type="text/plain")
    
    def event_stream():
        yield from stream_all_agents(scenario.scenario)
    return StreamingResponse(event_stream(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
