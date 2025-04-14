from graphs.state import AgentState
from llm.chains.executor_chain import executor_chain
from utils.safe_exec import execute_python_code
import logging
from utils.sanitize import sanitize, strip_code_block

logger = logging.getLogger("stratpilot")

def executor_node(state: AgentState) -> AgentState:
    # Determine the current step index based on results accumulated
    current_index = state.current_step_index
    dataset_list = [
        f"{sanitize(name)}_df" for name in state.datasets
    ]
    available_dfs = {f"{sanitize(name)}_df": df['data'].copy() for name, df in state.datasets.items()} if not state.update_dataframes else state.update_dataframes
    # Extract the current step from the plan (assuming it is already validated)
    step = state.plan[current_index]
    variable_env = state.variable_env or {}
    
    # Prepare inputs for the executor chain using the step's details
    inputs = {
        "step": step.step,
        "description": step.description,
        "goal": step.goal or "",
        "assumptions": "\n".join(step.assumptions),
        "required_variables": ", ".join(step.required_variables),
        "expected_outputs": ", ".join(step.expected_outputs),
        "schema_context": state.schema_context,
        "dataset_list": "\n".join(dataset_list),
        "error_message": "" if state.retry_step else state.step_blocker
    }
    
    # Invoke the executor chain to generate Python code for this step
    code = executor_chain.invoke(inputs).content
    logger.info("🧠 [Executor Generated Code]\n%s", code)
    
    # Execute the generated code safely and capture output, error, and any chart produced
    output, error, chart_path, chart_title, updated_dataframes, variable_env  = execute_python_code(strip_code_block(code), available_dfs, step.expected_outputs,variable_env)
        
    logger.info("📤 [Executor Output]\n%s", output)
    logger.info("📤 [Executor Error]\n%s", error)
    logger.info("📤 [Executor Chart Path]\n%s", chart_path)
    
    # On success, update the memory log with output info
    memory_log = state.memory_log or []
    memory_log.append(f"[Step {step.step}] {step.description}\n{output if not error else error}")
    
    # Create a unique chart ID based on the current step index (starting from 1)
    chart_id = f"chart_{current_index+1}"
    
    # Build the result dictionary including the chart and its unique ID
    result = {
        "summary": output,
        "chart": chart_path,
        "chart_id": chart_id,
        "chart_title": chart_title,
        "step_description": step.description
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
        "update_dataframes": updated_dataframes if not error else state.update_dataframes,
        "variable_env": variable_env if not error else state.variable_env
    })
