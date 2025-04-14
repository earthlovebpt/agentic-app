from langchain_core.runnables import Runnable
from llm.llm_config import llm
from llm.prompts.validate_data_prompt import validate_prompt
from llm.parsers.validate_data_parser import ValidationOutput
from langchain.output_parsers import PydanticOutputParser


parser = PydanticOutputParser(pydantic_object=ValidationOutput)

validate_data_chain: Runnable = (
    validate_prompt.partial(format_instructions=parser.get_format_instructions())
    | llm.with_structured_output(ValidationOutput)
)
