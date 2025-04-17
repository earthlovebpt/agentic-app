from pydantic import BaseModel
from typing import List, Optional

class Actionable(BaseModel):
    step: str
    impact: str

class CaseSummaryOutput(BaseModel):
    thoughts: str
    business_profile: str
    actionables: List[Actionable]
