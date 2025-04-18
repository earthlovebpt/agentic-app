from pydantic import BaseModel
from typing import List, Optional

class PlanStep(BaseModel):
    step: str
    description: str
    goal: str
    expected_outputs: List[str]
    assumptions: List[str]
    required_variables: List[str]
    outputs: List[str]

class PlanOutput(BaseModel):
    steps: List[PlanStep]