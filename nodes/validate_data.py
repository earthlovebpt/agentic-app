from graphs.state import AgentState
from llm.chains.validate_data import validate_data_chain

def validate_data_node(state: AgentState) -> AgentState:
    return {"data_sufficient": True}
    # result = validate_data_chain.invoke({
    #     "schema_context": state.schema_context or "",
    #     "user_prompt": state.user_prompt or ""
    # })

    # return state.model_copy(update={
    #     "data_sufficient": result.data_sufficient,
    #     "recommendations_if_insufficient": result.recommendations,
    # })