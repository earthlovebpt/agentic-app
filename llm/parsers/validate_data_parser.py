from pydantic import BaseModel, Field

class ValidationOutput(BaseModel):
    data_sufficient: bool = Field(..., description="Can the data answer the question?")
    recommendations: list[str] = Field(..., description="What to upload or ask instead")