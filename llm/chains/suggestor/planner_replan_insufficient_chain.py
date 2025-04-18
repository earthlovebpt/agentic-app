from llm.prompts.suggestor.planner_replan_insufficient_prompt import planner_replan_insufficient_prompt
from llm.parsers.suggestor.planner_parser import PlanOutput
from langchain.output_parsers import PydanticOutputParser
from llm.llm_config import llm  # your centralized LLM config

# 🧠 Create the output parser
parser = PydanticOutputParser(pydantic_object=PlanOutput)

# 🔁 Build chain
planner_replan_insufficient_chain = (
    planner_replan_insufficient_prompt
    | llm.with_structured_output(PlanOutput)
)
