import os
from typing import Optional
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from .tools import complete_python_task, save_final_result
from .state import DAAgentState
from ...llm_config import llm


def get_da_agent():
    # Load system prompt
    _prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/da_agent_prompt.md")
    with open(_prompt_path, "r") as f:
        _system_prompt = f.read()

    # Define tools
    _tools = [complete_python_task, save_final_result]

    # Create a single ReAct agent node that uses AgentState
    agent_node = create_react_agent(
        llm,
        _tools,
        prompt=_system_prompt,
        state_schema=DAAgentState
    )

    return agent_node