from graphs.state import AgentState
from llm.chains.executor_chain import executor_chain
from utils.safe_exec import execute_python_code
import logging

logger = logging.getLogger(__name__)

def executor_node(state: AgentState) -> AgentState:
    current_index = len(state.results or [])
    step = state.plan[current_index]

    inputs = {
        "step": step.step,
        "description": step.description,
        "goal": step.goal or "",
        "assumptions": "\n".join(step.assumptions),
        "required_variables": ", ".join(step.required_variables),
        "expected_outputs": ", ".join(step.expected_outputs),
        "schema_context": state.business_profile.get("schema_context", "")
    }

    logger.info("📤 [Executor Prompt Inputs]\n%s", inputs)

    code = executor_chain.invoke(inputs)
    logger.info("🧠 [Executor Generated Code]\n%s", code)

    output, error, chart_path = execute_python_code(code, state.datasets)

    if error and not state.retry_step:
        logger.warning("⚠️ Code failed, retrying with error context.")
        return state.model_copy(update={
            "step_successful": False,
            "retry_step": True,
            "step_blocker": error
        })

    if error and state.retry_step:
        logger.error("❌ Retry failed, trigger replan.")
        return state.model_copy(update={
            "step_successful": False,
            "retry_step": False,
            "replan_step": True,
            "step_blocker": error
        })

    # ✅ Success
    memory_log = state.memory_log or []
    memory_log.append(f"[Step {step.step}] {step.description}\n{output}")

    result = {
        "summary": output,
        "chart": chart_path,
        "step_description": step.description
    }

    return state.model_copy(update={
        "step_successful": True,
        "retry_step": False,
        "replan_step": False,
        "step_blocker": None,
        "results": (state.results or []) + [result],
        "memory_log": memory_log,
        "plan_successful": current_index+1 == len(state.plan)
    })
