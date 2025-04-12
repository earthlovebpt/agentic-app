from graphs.state import AgentState
import logging

logger = logging.getLogger(__name__)

def step_reflect_node(state: AgentState) -> AgentState:
    results = state.results or []
    current_index = state.current_step_index or 0

    if current_index >= len(results):
        logger.warning("❗ step_reflect_node: No result found for current step.")
        return state.model_copy(update={"step_successful": False, "replan_step": True})

    step_result = results[current_index]
    summary = step_result.get("summary", "").lower()

    # Increment retry count if a replan is needed
    current_retry = state.retry_count or 0
    max_allowed = state.max_retries or 2
    new_retry_count = current_retry + 1

    # 🚨 Heuristic: Detect error
    if "traceback" in summary or "error" in summary or "exception" in summary:
        if new_retry_count > max_allowed:
            logger.warning(f"🚫 Max retry limit reached ({max_allowed}). Not replanning again.")
            return state.model_copy(update={
                "step_successful": False,
                "retry_step": False,
                "replan_step": False,
                "step_blocker": summary
            })
        else:
            logger.info("❌ Step execution failed — will attempt replan")
            return state.model_copy(update={
                "step_successful": False,
                "retry_step": False,
                "replan_step": True,
                "step_blocker": summary
            })

    # ✅ Success: continue
    logger.info("✅ Step completed successfully.")
    return state.model_copy(update={
        "step_successful": True,
        "retry_step": False,
        "replan_step": False,
        "step_blocker": None,
        "current_step_index": current_index + 1
    })
