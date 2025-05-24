# app/agents/engineering.py
from app.agents.base import BaseAgent

class EngineeringAgent(BaseAgent):
    def __init__(self):
        super().__init__("Engineering", "Provide a Engineering analysis of the user's scenario.")
