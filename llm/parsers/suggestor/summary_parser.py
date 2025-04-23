from pydantic import BaseModel
from typing import List

class StrategicSummary(BaseModel):
    thought: str
    answer_to_question: str
    insights: List[str]