import logging
from graphs.state import AgentState
from llm.chains.suggestor.planner_chain import planner_chain
from llm.chains.suggestor.planner_replan_execution_chain import planner_replan_execution_chain
from llm.chains.suggestor.planner_replan_insufficient_chain import planner_replan_insufficient_chain

logger = logging.getLogger("stratpilot")

def planner(state: AgentState) -> AgentState:
    """
    Planner node: generates a multi-step plan to answer a question based on the
    user's prompt, prior summary, memory log, and business context.

    Planner chooses one of three replan strategies based on the current state:

    1. If data is insufficient to answer the question, use the insufficient-data
       replan chain.
    2. If a previous step failed to execute, use the execution replan chain.
    3. Otherwise, use the regular planner chain.

    Planner node returns an updated state with a revised plan.

    :param state: the current state
    :return: the updated state
    """
    user_prompt = state.user_prompt or ""
    prior_summary = state.prior_summary or ""
    memory_log = "\n".join(state.memory_log or [])

    # ⚖️ Choose replan strategy
    if (not state.data_sufficient) or state.replan_step:
        logger.info("📉 Reason: Data insufficient to answer. Using insufficient-data replan chain.")
        inputs = {
            "business_detail": state.business_profile,
            "schema_context": state.schema_context,
            "user_prompt": user_prompt,
            "prior_summary": prior_summary,
            "memory_log": memory_log,
        }
        chain = planner_replan_insufficient_chain
        state.retry_count += 1
    elif state.retry_step:
        logger.info("📛 Reason: Previous step failed to execute. Using execution replan chain.")
        inputs = {
            "business_detail": state.business_profile,
            "schema_context": state.schema_context,
            "full_plan": state.plan or [],
            "error_step_id": len(state.results or [])-1,
            "error_msg": state.step_blocker,
            "variable_env": ", ".join(list(state.variable_env.keys())),
            "user_prompt": user_prompt,
            "memory_log": memory_log,
        }
        chain = planner_replan_execution_chain
        state.retry_count += 1
    else:
        logger.info("🧠 [Planner] Planning...")
        inputs = {
            "business_detail": state.business_profile,
            "schema_context": state.schema_context,
            "user_prompt": user_prompt,
            "prior_summary": prior_summary,
            "memory_log": memory_log,
        }
        chain = planner_chain

    # 🔍 Generate revised plan
    steps = chain.invoke(inputs).steps

    # 🧾 Trace logging each step
    logger.info("✅ [Planned Steps]")
    for i, step in enumerate(steps):
        logger.info(f"  Step {i + 1}: {step.description if hasattr(step, 'description') else '[No description]'}")
        if hasattr(step, "goal"):
            logger.debug(f"    Goal: {step.goal}")
        if hasattr(step, "expected_outputs"):
            logger.debug(f"    Expected Outputs: {step.expected_outputs}")
        if hasattr(step, "outputs"):
            logger.debug(f"    Produces: {step.outputs}")

    return state.model_copy(update={
        "plan": steps,
        "step_blocker": None,
        "exceed_max_retries": state.retry_count >= state.max_retries
    })
