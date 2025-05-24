# app/agents/legal.py
from app.agents.base import BaseAgent

class LegalAgent(BaseAgent):
    def __init__(self):
        super().__init__("Legal", "Provide a legal analysis of the user's scenario.")
