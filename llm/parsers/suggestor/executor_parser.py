from pydantic import BaseModel
from typing import List, Optional, Dict

class ExecutorOutput(BaseModel):
    reasoning: str
    code: str