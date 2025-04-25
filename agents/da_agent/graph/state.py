import operator
from typing import Sequence, TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from pydantic import Field
from typing import Dict, Any


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    datasets: Dict[str, Any] = Field(default_factory=dict)  
    schema_context: str
    intermediate_outputs: Annotated[List[dict], operator.add]
    current_variables: dict
    output_image_paths: Annotated[List[str], operator.add]
    final_result: dict