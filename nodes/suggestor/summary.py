from graphs.state import AgentState
from llm.chains.suggestor.summary_chain import summary_chain
import logging

logger = logging.getLogger("stratpilot")

def summary_node(state: AgentState) -> AgentState:
    # Aggregate textual results from executor steps.
    summaries = "\n".join([res.get("summary", "") for res in state.results or []])
      
    inputs = {
        "business_detail": state.business_profile or {},
        "schema_context": state.schema_context,
        "user_prompt": state.user_prompt,
        "results": summaries,
    }
    
    logger.info("📤 [Summary Node Input]\n%s", inputs)
    
    response = summary_chain.invoke(inputs)
    
    logger.info("📥 [Summary Node Output]\n%s", response)
    tmp = state.insights + response.insights
    
    return state.model_copy(update={
        "answer_to_question": response.answer_to_question,
        "insight_summary": tmp,
        "complete_gen_question": len(tmp) == len(state.gen_questions),
    })
