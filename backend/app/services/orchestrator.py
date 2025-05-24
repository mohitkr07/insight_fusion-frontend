from app.agents.legal import LegalAgent
from app.agents.finance import FinanceAgent
from app.agents.marketing import MarketingAgent
from app.agents.engineering import EngineeringAgent
from app.schemas import ScenarioResponse, AgentResponse
import asyncio

agents = [
    LegalAgent(),
    FinanceAgent(),
    MarketingAgent(),
    EngineeringAgent()
]

async def run_agents(scenario: str) -> ScenarioResponse:
    # Run all agents in parallel using asyncio.to_thread
    responses = await asyncio.gather(
        *[asyncio.to_thread(agent.respond, scenario) for agent in agents]
    )

    agent_responses = [
        AgentResponse(role=agent.role, message=msg)
        for agent, msg in zip(agents, responses)
    ]

    summary = "This plan involves " + ", ".join([f"{a.role} considerations" for a in agents])
    return ScenarioResponse(summary=summary, responses=agent_responses)

def stream_all_agents(scenario: str):
    for agent in agents:
        # Prefix with agent role
        yield f"\n--- {agent.role} Analysis ---\n"
        for chunk in agent.stream_respond(scenario):
            yield chunk