from pydantic import BaseModel
from typing import List, Optional

class AdaptedActionable(BaseModel):
    thought: str
    step: str
    detailed_steps: List[str]
    expected_impact: str

class FilterActionableOutput(BaseModel):
    thought: str
    relevant_case_study: bool
    adapted_actionables: List[AdaptedActionable]

