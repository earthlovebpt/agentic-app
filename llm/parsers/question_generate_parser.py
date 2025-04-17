from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str
    related_fields: List[str]
    goal_alignment: str
    suggested_method: List[str]

class QuestionGenerateOutput(BaseModel):
    thought: str
    questions: List[Question]
