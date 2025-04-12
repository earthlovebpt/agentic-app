from llm.prompts.summary_prompt import summary_prompt
from llm.parsers.summary_parser import StrategicSummary
from langchain.output_parsers import PydanticOutputParser
from llm.llm_config import llm

parser = PydanticOutputParser(pydantic_object=StrategicSummary)

summary_chain = (
    summary_prompt.partial(format_instructions=parser.get_format_instructions())
    | llm.with_structured_output(StrategicSummary)
)
