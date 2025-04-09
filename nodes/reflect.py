from graphs.state import AgentState
from llm.chains.reflect_chain import reflect_chain
import logging

logger = logging.getLogger(__name__)

def reflect_on_results_node(state: AgentState) -> AgentState:
    summaries = "\n".join([r.get("summary", "") for r in state.results or []])
    insight_highlights = "\n".join([r.get("insight_highlights", "") for r in state.results or []])

    inputs = {
        "user_prompt": state.user_prompt,
        "summaries": summaries,
        "insight_highlights": insight_highlights,
    }

    logger.info("📤 [Reflect Input]\n%s", inputs)

    reflection = reflect_chain.invoke(inputs)

    logger.info("📥 [Reflect Output]\n%s", reflection)

    # Increment retry count if a replan is needed
    current_retry = state.retry_count or 0
    max_allowed = state.max_retries or 2
    new_retry_count = current_retry + 1

    if reflection.replan and new_retry_count > max_allowed:
        logger.warning(f"🚫 Max retry limit reached ({max_allowed}). Not replanning again.")
        # Stop replanning
        replan = False
    else:
        replan = reflection.replan

    return state.model_copy(update={
        "replan": replan,
        "new_prompt": reflection.new_prompt,
        "data_sufficient": reflection.data_sufficient,
        "prior_summary": reflection.prior_summary,
        "retry_count": new_retry_count if replan else current_retry
    })
