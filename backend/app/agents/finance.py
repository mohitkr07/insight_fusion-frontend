# app/agents/finance.py
from app.agents.base import BaseAgent

class FinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Finance", "Provide a Finance analysis of the user's scenario.")
