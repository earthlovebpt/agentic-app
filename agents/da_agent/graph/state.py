from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from langgraph.prebuilt.chat_agent_executor import AgentState

class DAAgentState(AgentState):
    schema_context: str = ""
    datasets: Dict[str, Any] = field(default_factory=dict)
    current_variables: List[str] = field(default_factory=list)
    output_image_paths: List[Any] = field(default_factory=list)
    intermediate_outputs: List[str] = field(default_factory=list)
    header_injected: bool = False
    final_result: Optional[Dict[str, Any]] = None