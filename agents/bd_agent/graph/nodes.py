from .state import BDState
from .tools import search_summary, analyze_internal_data, finalize_from_insights
from agents.llm_config import bd_llm
from ..prompt.bd_prompt import get_bd_prompt
import logging

logger = logging.getLogger("Daisy")

from langgraph.prebuilt import create_react_agent


def get_bd_agent():
    tools = [search_summary, finalize_from_insights, analyze_internal_data]

    agent_node = create_react_agent(
        bd_llm,
        tools,
        prompt=get_bd_prompt,
        state_schema=BDState
    )

    return agent_node