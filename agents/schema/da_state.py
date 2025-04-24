from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from operator import add
from pydantic import BaseModel


class DAState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    visuals: list
    data_insights: list[str]
    summary: str