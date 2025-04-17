from llm.llm_config import llm
from llm.prompts.filter_actionable_prompt import filter_actionable_prompt
from llm.parsers.filter_actionable_parser import FilterActionableOutput
from langchain.output_parsers import PydanticOutputParser

# Shared parser
filter_actionable_parser = PydanticOutputParser(pydantic_object=FilterActionableOutput)

# Normal planner chain
filter_actionable_chain = (
    filter_actionable_prompt
    | llm.with_structured_output(FilterActionableOutput)
)