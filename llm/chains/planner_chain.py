from llm.llm_config import llm
from llm.prompts.planner_prompt import planner_prompt
from llm.parsers.planner_parser import PlanOutput
from langchain.output_parsers import PydanticOutputParser

# Shared parser
planner_parser = PydanticOutputParser(pydantic_object=PlanOutput)

# Normal planner chain
planner_chain = (
    planner_prompt.partial(format_instructions=planner_parser.get_format_instructions())
    | llm.with_structured_output(PlanOutput)
)
