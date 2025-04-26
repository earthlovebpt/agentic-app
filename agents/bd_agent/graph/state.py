from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from operator import add


class BDState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    data_insights: Annotated[list, add]
    search_insights: Annotated[list, add]
    business_profile: dict
    schema_context: str
    strategies: list
    answer: str