from llm.prompts.executor_prompt import executor_prompt
from llm.llm_config import llm

executor_chain = executor_prompt | llm