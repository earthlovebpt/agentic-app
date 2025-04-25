from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from .state import AgentState
import json
from typing import Literal
from .tools import complete_python_task
from langgraph.prebuilt import ToolInvocation, ToolExecutor
import os
from llm_config import llm

tools = [complete_python_task]

model = llm.bind_tools(tools)
tool_executor = ToolExecutor(tools)

with open(os.path.join(os.path.dirname(__file__), "../prompts/main_prompt.md"), "r") as file:
    prompt = file.read()

chat_template = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("placeholder", "{messages}"),
])
model = chat_template | model

def create_available_variables(state: AgentState) -> str:
    summary = ""
    if "current_variables" in state:
        remaining_variables = [v for v in state["current_variables"] if v not in state["datasets"]]
        for v in remaining_variables:
            summary += f"\n\nVariable: {v}"
    return summary

def route_to_tools(
    state: AgentState,
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

def call_model(state: AgentState):

    current_data_template  = """The following data is available:\n{schema_context}{available_variables}"""
    current_data_message = HumanMessage(content=current_data_template.format(schema_context=state["schema_context"], available_variables=create_available_variables(state)))
    state["messages"] = [current_data_message] + state["messages"]

    llm_outputs = model.invoke(state)

    return {"messages": [llm_outputs], "intermediate_outputs": [current_data_message.content]}

def call_tools(state: AgentState):
    last_message = state["messages"][-1]
    tool_invocations = []
    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls'):
        tool_invocations = [
            ToolInvocation(
                tool=tool_call["name"],
                tool_input={**tool_call["args"], "graph_state": state}
            ) for tool_call in last_message.tool_calls
        ]

    responses = tool_executor.batch(tool_invocations, return_exceptions=True)
    tool_messages = []
    state_updates = {}

    for tc, response in zip(last_message.tool_calls, responses):
        if isinstance(response, Exception):
            raise response
        message, updates = response
        tool_messages.append(ToolMessage(
            content=str(message),
            name=tc["name"],
            tool_call_id=tc["id"]
        ))
        state_updates.update(updates)

    if 'messages' not in state_updates:
        state_updates["messages"] = []

    state_updates["messages"] = tool_messages 
    return state_updates