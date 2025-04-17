from llm.llm_config import llm
from llm.prompts.case_summary_prompt import case_summary_prompt
from llm.parsers.case_summary_parser import CaseSummaryOutput
from langchain.output_parsers import PydanticOutputParser

# Shared parser
case_summary_parser = PydanticOutputParser(pydantic_object=CaseSummaryOutput)

# Normal planner chain
case_summary_chain = (
    case_summary_prompt
    | llm.with_structured_output(CaseSummaryOutput)
)