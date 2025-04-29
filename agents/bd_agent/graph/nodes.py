from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from typing import Literal
from langgraph.prebuilt import ToolNode

from .state import BDState
from .tools import search_summary, advise_from_insights, answer_from_insights, analyze_internal_data, finalize_from_insights
from agents.llm_config import bd_llm
from ..prompt.bd_prompt_v2 import get_bd_prompt
import ast
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