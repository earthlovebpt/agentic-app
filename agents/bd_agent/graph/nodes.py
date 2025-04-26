from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from typing import Literal
from langgraph.prebuilt import ToolNode

from .state import BDState
from .tools import search_summary, advise_from_insights, answer_from_insights
from agents.llm_config import bd_llm
from ..prompt.bd_prompt import get_bd_prompt
import ast
import logging

logger = logging.getLogger("stratpilot")

tools = [search_summary, advise_from_insights, answer_from_insights]
tool_node = ToolNode(tools)
def route_to_tools(
    state: BDState,
) -> Literal["tools", "__end__"]:
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route back to the agent.
    """

    if messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"

def call_model(state: BDState):
    logger.info(state)
    logger.info(f"[Current State] {state['messages']}")
    runnable = get_bd_prompt(schema_context = state["schema_context"], business_profile = state["business_profile"]) | bd_llm.bind_tools(tools, tool_choice="any")

    #Invoke with messages
    msg = runnable.invoke({"messages": state["messages"]})

    logger.info(f"[Model Call] {msg}")
    return {"messages": msg}


def call_tools(state: BDState):
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls'):
        for tool_call in last_message.tool_calls:
            tool_call["args"] = {**tool_call["args"], "graph_state": state}

    logger.info(f"[Tool Call Args] :{tool_call}")
    responses = tool_node.invoke(state["messages"])
    logger.info(f"[Tool Call Response]: {responses}")
    state_updates = {}

    for tc, response in zip(last_message.tool_calls, responses):
        if isinstance(response, Exception):
            raise response
        
        content = ast.literal_eval(response.content)
        msg = content.pop("messages")
        response.content = msg

        state_updates.update(content)

    if 'messages' not in state_updates:
        state_updates["messages"] = []

    state_updates["messages"] = responses
    return state_updates