from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from dataclasses import field
from langgraph.prebuilt.chat_agent_executor import AgentState


class BDState(AgentState):
    data_insights: list = field(default_factory=list)
    search_insights: list = field(default_factory=list)
    business_profile: dict = field(default_factory=dict)
    schema_context: str = ""
    strategies: list = field(default_factory=list)
    answer: str = ""