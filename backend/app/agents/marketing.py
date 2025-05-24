from app.agents.base import BaseAgent

class MarketingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Marketing", "Provide a Market analysis of the user's scenario.")
