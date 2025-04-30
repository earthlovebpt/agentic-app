from .graph.state import AgentState
from agents.understand_agent.graph.suggest_questions import suggest_questions_chain

def suggest_questions_node(state: AgentState) -> AgentState:
    result = suggest_questions_chain.invoke({
        "business_type": state.business_profile.get("type", ""),
        "business_details": state.business_profile.get("details", ""),
        "schema_context": state.schema_context or "",
    })

    return state.model_copy(update={
        "suggested_questions": result.questions,
    })
