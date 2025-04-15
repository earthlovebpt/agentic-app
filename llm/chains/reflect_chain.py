from llm.prompts.reflect_prompt import reflect_prompt
from llm.parsers.reflect_parser import ReflectionSummary
from llm.llm_config import llm

reflect_chain = (
    reflect_prompt
    | llm.with_structured_output(ReflectionSummary)
)
