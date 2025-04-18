from pydantic import BaseModel
from typing import List, Optional

class PlanStep(BaseModel):
    step: str
    description: str
    goal: str
    expected_outputs: List[str]
    assumptions: List[str]
    required_variables: List[str]
    required_libs: List[str]
    outputs: List[str]

class PlanOutput(BaseModel):
    reasoning: str
    steps: List[PlanStep]