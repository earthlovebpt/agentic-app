from graphs.state import AgentState
from llm.chains.suggestor.executor_chain import executor_chain
from utils.safe_exec import execute_python_code
import logging
from utils.sanitize import sanitize, strip_code_block
from utils.safe_exec import NAME_TO_SHORT
import copy

logger = logging.getLogger("stratpilot")

def executor_node(state: AgentState) -> AgentState:
    # Determine the current step index based on results accumulated
    current_index = state.current_step_index
    logger.info("[Executor] Executing Step {}".format(current_index))
    logger.info("[Executor] Plan: {}".format("\n".join([f"{step.step}: {step.description}" for step in state.plan])))
    variable_env = {sanitize(name): df['data'].copy() for name, df in state.datasets.items()} if (state.variable_env == {}) else state.variable_env
    variables_list = [
        sanitize(name) for name in variable_env
    ]
    # Extract the current step from the plan (assuming it is already validated)
    step = copy.deepcopy(state.plan[current_index])

    step.assumptions = "\n".join(step.assumptions)
    step.required_variables = ", ".join(step.required_variables)
    step.required_libs = ", ".join(step.required_libs)
    expected_outputs = step.outputs
    step.expected_outputs = ", ".join(step.expected_outputs)

    variables_list = "\n".join(variables_list)
    # Prepare inputs for the executor chain using the step's details
    inputs = {**step.model_dump(), 
            "schema_context": state.schema_context, 
            "variables_list": variables_list,
            "name_to_short": "\n".join([f"import {k} as {v}" for k, v in NAME_TO_SHORT.items()]),
            "error_msg": state.step_blocker}

    # Invoke the executor chain to generate Python code for this step
    code = executor_chain.invoke(inputs).code
    code = strip_code_block(code)
    logger.info("🧠 [Executor Generated Code]\n%s", code)

    # Execute the generated code safely and capture output, error, and any chart produced
    output, error, chart_path, chart_title, updated_venv  = execute_python_code(strip_code_block(code), variable_env, expected_outputs)
        
    logger.info("📤 [Executor Output]\n%s", output)
    logger.info("📤 [Executor Error]\n%s", error)
    logger.info("📤 [Executor Chart Path]\n%s", chart_path)

    # On success, update the memory log with output info
    memory_log = state.memory_log or []
    memory_log.append(f"[Step {step.step}] {step.description}\n{output if not error else error}")


    # Create a unique chart ID based on the current step index (starting from 1)
    chart_id = f"chart_{current_index+1:02d}"

    # Build the result dictionary including the chart and its unique ID
    result = {
        "summary": output,
        "chart": chart_path,
        "chart_id": chart_id,
        "chart_title": chart_title,
        "step_description": step.description,
        "code": code,
        "error": error
    }
    
    # Return an updated state with the new result appended.
    # Also, flag 'plan_successful' if the last step has been reached.
    return state.model_copy(update={
        "retry_step": True if error else False,
        "replan_step": True if error and state.retry_step else False,
        "step_successful": True if not error else False,
        "step_blocker": None if not error else error,
        "results": (state.results or []) + [result] if not error else (state.results or []),
        "memory_log": memory_log,
        "current_step_index": current_index + 1 if not error else current_index,
        "plan_successful": (current_index + 1 == len(state.plan)) if not error else False,
        "variable_env": {**(state.variable_env or {}), **updated_venv} if not error else state.variable_env
    })
