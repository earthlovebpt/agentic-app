from pydantic import BaseModel
from typing import List

class StrategicSummary(BaseModel):
    answer_to_question: str
    insight_summary: str
    recommended_actions: List[str]