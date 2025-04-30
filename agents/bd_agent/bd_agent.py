from agents.bd_agent.graph.state import BDState
from agents.bd_agent.graph.nodes import get_bd_agent
from langchain_core.messages import HumanMessage

def run_bd_agent(user_prompt, business_profile, schema_context, datasets):
    bd_state = BDState(
        messages=[HumanMessage(content=f"<question>{user_prompt}</question>")],
        schema_context=schema_context,
        business_profile = business_profile,
        datasets = datasets
    )

    agent_node = get_bd_agent()
    result = agent_node.invoke(bd_state)
    return result
