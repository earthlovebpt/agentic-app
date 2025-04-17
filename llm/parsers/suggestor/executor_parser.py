from pydantic import BaseModel
from typing import List, Optional

class ExecutorOutput(BaseModel):
    reasoning: str
    code: str