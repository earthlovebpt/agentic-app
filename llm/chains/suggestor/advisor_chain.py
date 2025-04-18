from llm.llm_config import llm
from llm.prompts.suggestor.executor_prompt import advisor_prompt
from llm.parsers.suggestor.executor_parser import AdvisorOutput
from langchain.output_parsers import PydanticOutputParser

# Shared parser
advisor_parser = PydanticOutputParser(pydantic_object=AdvisorOutput)

# Normal planner chain
advisor_chain = (
    advisor_prompt
    | llm.with_structured_output(AdvisorOutput)
)