from llm.llm_config import llm
from llm.prompts.suggestor.question_generate_prompt import question_generate_prompt
from llm.parsers.suggestor.question_generate_parser import QuestionGenerateOutput
from langchain.output_parsers import PydanticOutputParser

# Shared parser
question_generate_parser = PydanticOutputParser(pydantic_object=QuestionGenerateOutput)

# Normal planner chain
question_generate_chain = (
    question_generate_prompt
    | llm.with_structured_output(QuestionGenerateOutput)
)