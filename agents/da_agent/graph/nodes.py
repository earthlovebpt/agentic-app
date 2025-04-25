import os
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from .tools import complete_python_task, save_final_result
from ...llm_config import llm

# 1) Load your system prompt
_prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/ds_agent_prompt.md")
with open(_prompt_path, "r") as f:
    _system_prompt = f.read()

# 2) Instantiate the ReAct agent node
_tools = [complete_python_task, save_final_result]
agent_node = create_react_agent(llm, _tools, prompt=_system_prompt)


# 3) Helper to print out which variables are still unused
def create_available_variables(state: dict) -> str:
    summary = ""
    for v in state.get("current_variables", []):
        if v not in state.get("datasets", {}):
            summary += f"\n\nVariable: {v}"
    return summary
