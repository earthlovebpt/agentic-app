from graphs.state import AgentState
from llm.chains.executor_chain import executor_chain
from utils.safe_exec import execute_python_code
import logging
from utils.sanitize import sanitize, strip_code_block

logger = logging.getLogger("stratpilot")

def executor_node(state):
    # Preprocess inputs.
    current_step = state.plan[state.current_step_index]
    inputs = preprocess_input(state, current_step)
    
    # Run code.
    output, error, chart_path, chart_title, updated_dataframes, updated_variable_env, code = generate_and_execute_code(state, inputs)
    log_data(code=code, output=output, error=error, chart_path=chart_path)
    
    # Get other outputs.
    memory_log = get_memory_log(state, current_step, output, error)
    result = get_result(state, current_step, output, chart_path, chart_title)
    
    return {
        "retry_step": True if error else False,
        "replan_step": True if error and state.retry_step else False,
        "step_successful": True if not error else False,
        "step_blocker": None if not error else error,
        "results": (state.results or []) + [result] if not error else (state.results or []),
        "memory_log": memory_log,
        "current_step_index": state.current_step_index + 1 if not error else state.current_step_index,
        "plan_successful": (state.current_step_index + 1 == len(state.plan)) if not error else False,
        "update_dataframes": updated_dataframes if not error else state.update_dataframes,
        "variable_env": updated_variable_env if not error else state.variable_env
    }

def preprocess_input(state, current_step):
    return {
        "step": current_step.step,
        "description": current_step.description,
        "goal": current_step.goal or "",
        "assumptions": "\n".join(current_step.assumptions),
        "required_variables": ", ".join(current_step.required_variables),
        "expected_outputs": ", ".join(current_step.expected_outputs),
        "schema_context": state.schema_context,
        "dataset_list": "\n".join([f"{sanitize(name)}_df" for name in state.datasets]),
        "error_message": "" if state.retry_step else state.step_blocker
    }
    
def log_data(**data_to_log):
    for key, value in data_to_log.items(): 
        logger.info(f"📤 [Executor-{key}]\n%s", value)
        
def generate_and_execute_code(state, inputs):
    # 1. Generaete code.
    code = executor_chain.invoke(inputs).content
    
    # 2. Execute code.
    available_dfs = {f"{sanitize(name)}_df": df['data'].copy() for name, df in state.datasets.items()} if not state.update_dataframes else state.update_dataframes
    expected_outputs = state.plan[state.current_step_index].expected_outputs
    variable_env = state.variable_env or {}
    output, error, chart_path, chart_title, updated_dataframes, updated_variable_env  = execute_python_code(
        strip_code_block(code), 
        available_dfs, 
        expected_outputs, 
        variable_env
    )
    return output, error, chart_path, chart_title, updated_dataframes, updated_variable_env, code

def get_memory_log(state, current_step, output, error):
    memory_log = state.memory_log or []
    memory_log.append(f"[Step {current_step.step}] {current_step.description}\n{output if not error else error}")
    return memory_log

def get_result(state, current_step, output, chart_path, chart_title):
    return {
        "summary": output,
        "chart": chart_path,
        "chart_id": f"chart_{state.current_step_index+1}",
        "chart_title": chart_title,
        "step_description": current_step.description
    }
    
