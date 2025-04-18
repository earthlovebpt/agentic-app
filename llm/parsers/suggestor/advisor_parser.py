from pydantic import BaseModel
from typing import List, Optional, Dict

class Strategy(BaseModel):
    thought: str
    title: str
    description: str
    detailed_plans: List[str]
    advantages: List[str]
    disadvantages: List[str]
    followup: List[str]

class AdvisorOutput(BaseModel):
    strategies: List[Strategy]