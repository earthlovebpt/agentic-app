from llm.llm_config import llm
from llm.prompts.suggestor.executor_prompt import executor_prompt
from llm.parsers.suggestor.executor_parser import ExecutorOutput
from langchain.output_parsers import PydanticOutputParser

# Shared parser
executor_parser = PydanticOutputParser(pydantic_object=ExecutorOutput)

# Normal planner chain
executor_chain = (
    executor_prompt
    | llm.with_structured_output(ExecutorOutput)
)