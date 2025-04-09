from pydantic import BaseModel
from typing import Optional

class ReflectionSummary(BaseModel):
    replan: bool
    new_prompt: Optional[str]
    data_sufficient: Optional[bool]
    prior_summary: Optional[str]