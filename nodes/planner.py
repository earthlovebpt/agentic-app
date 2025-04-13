import logging
from graphs.state import AgentState
from llm.chains.planner_chain import planner_chain
from llm.chains.planner_replan_execution_chain import planner_replan_execution_chain
from llm.chains.planner_replan_insufficient_chain import planner_replan_insufficient_chain

from llm.prompts.planner_prompt import planner_prompt
from llm.prompts.planner_replan_execution_prompt import planner_replan_execution_prompt
from llm.prompts.planner_replan_insufficient_prompt import planner_replan_insufficient_prompt

from llm.parsers.planner_parser import PlanOutput
from langchain.output_parsers import PydanticOutputParser

logger = logging.getLogger("stratpilot")
parser = PydanticOutputParser(pydantic_object=PlanOutput)

def planner(state: AgentState) -> AgentState:
    user_prompt = state.user_prompt or ""
    prior_summary = state.prior_summary or ""
    memory_log = "\n".join(state.memory_log or [])

    # ⚖️ Choose replan strategy
    if (not state.data_sufficient) or state.replan_step:
        logger.info("📉 Reason: Data insufficient to answer. Using insufficient-data replan chain.")
        inputs = {
            "business_type": state.business_profile.get("type", ""),
            "business_details": state.business_profile.get("details", ""),
            "schema_context": state.schema_context,
            "user_prompt": user_prompt,
            "prior_summary": prior_summary,
            "memory_log": memory_log,
        }
        chain = planner_replan_insufficient_chain
        selected_prompt = planner_replan_insufficient_prompt
        state.retry_count += 1
    elif state.retry_step:
        logger.info("📛 Reason: Previous step failed to execute. Using execution replan chain.")
        inputs = {
            "schema_context": state.schema_context,
            "full_plan": state.plan or [],
            "current_step_index": len(state.results or [])-1,
            "failed_step_description": state.plan[len(state.results or [])-1].description,
            "required_variables": state.plan[len(state.results or [])-1].required_variables,
            "error_message": state.step_blocker,
            "user_prompt": user_prompt,
            "prior_summary": prior_summary,
            "memory_log": memory_log,
        }
        chain = planner_replan_execution_chain
        selected_prompt = planner_replan_execution_prompt
        state.retry_count += 1
    else:
        logger.info("🧠 [Planner] Planning...")
        inputs = {
            "business_type": state.business_profile.get("type", ""),
            "business_details": state.business_profile.get("details", ""),
            "schema_context": state.schema_context,
            "user_prompt": user_prompt,
            "prior_summary": prior_summary,
            "memory_log": memory_log,
        }
        chain = planner_chain
        selected_prompt = planner_prompt

    try:
        formatted_prompt = selected_prompt.format(**inputs,format_instructions=parser.get_format_instructions())
        logger.info("📤 [Planner Prompt]:\n%s", formatted_prompt)
    except Exception as e:
        logger.error("Error formatting planner prompt: %s", e)

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
