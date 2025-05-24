# app/schemas.py
from pydantic import BaseModel

class ScenarioRequest(BaseModel):
    scenario: str

class AgentResponse(BaseModel):
    role: str
    message: str

class ScenarioResponse(BaseModel):
    summary: str
    responses: list[AgentResponse]
