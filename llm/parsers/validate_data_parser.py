from pydantic import BaseModel, Field

class ValidationOutput(BaseModel):
    thoughts: str
    data_sufficient: bool
    recommendations: list[str]