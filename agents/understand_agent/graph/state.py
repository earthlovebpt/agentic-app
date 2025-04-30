from typing import Any, Dict, List, Optional
from pydantic import BaseModel,Field


class AgentState(BaseModel):
    business_profile: Dict[str, str] = Field(default_factory=dict)
    datasets: Dict[str, Any] = Field(default_factory=dict)       # full dataset pool
    new_datasets: Dict[str, Any] = Field(default_factory=dict)   # newly added datasets
    schema_context: Optional[str] = None
    explored_datasets: List[str] = []
    suggested_questions: List[str] = Field(default_factory=list)