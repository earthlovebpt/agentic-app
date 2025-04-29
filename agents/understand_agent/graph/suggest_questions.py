from ...llm_config import llm
from agents.understand_agent.graph.suggest_questions_prompt import suggest_questions_prompt
from agents.understand_agent.graph.suggest_questions_parser import QuestionSuggestions
from langchain.output_parsers import PydanticOutputParser

# 🧠 Create the parser
parser = PydanticOutputParser(pydantic_object=QuestionSuggestions)

# 🔁 Build chain with parser format instructions
suggest_questions_chain = (
    suggest_questions_prompt.partial(format_instructions=parser.get_format_instructions())
    | llm.with_structured_output(QuestionSuggestions)
)