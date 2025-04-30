from pydantic import BaseModel
from typing import List

class QuestionSuggestions(BaseModel):
    questions: List[str]