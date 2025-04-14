from graphs.state import AgentState
from llm.chains.reflect_chain import reflect_chain
import logging

logger = logging.getLogger("stratpilot")

def reflect_on_results_node(state: AgentState) -> AgentState:
    summaries = "\n".join([r.get("summary", "") for r in state.results or []])

    inputs = {
        "user_prompt": state.user_prompt,
        "summaries": summaries,
    }

    logger.info("📤 [Reflect Input]\n%s", inputs)

    reflection = reflect_chain.invoke(inputs)

    logger.info("📥 [Reflect Output]\n%s", reflection)


    if reflection.replan and state.exceed_max_retries:
        logger.warning(f"🚫 Max retry limit reached ({state.max_retries}). Not replanning again.")
        # Stop replanning
        replan = False
    else:
        replan = reflection.replan

    return state.model_copy(update={
        "replan": replan,
        "new_prompt": reflection.new_prompt,
        "data_sufficient": reflection.data_sufficient,
        "prior_summary": reflection.prior_summary,
        "recommendations_if_insufficient": reflection.recommendations_if_insufficient
    })
