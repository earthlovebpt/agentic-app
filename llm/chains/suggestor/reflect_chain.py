from llm.prompts.suggestor.reflect_prompt import reflect_prompt
from llm.parsers.suggestor.reflect_parser import ReflectionSummary
from langchain.output_parsers import PydanticOutputParser
from llm.llm_config import llm

parser = PydanticOutputParser(pydantic_object=ReflectionSummary)

reflect_chain = (
    reflect_prompt.partial(format_instructions=parser.get_format_instructions())
    | llm.with_structured_output(ReflectionSummary)
)
