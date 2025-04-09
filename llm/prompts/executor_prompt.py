from langchain.prompts import ChatPromptTemplate

EXECUTOR_SYSTEM = (
    "You are a Python data analyst. Your job is to write Python code using pandas (and optionally matplotlib) "
    "to execute the analysis step below. The dataframes are already loaded and available by variable name.\n\n"
    "Each step should:\n"
    "- Use any required variables or inputs from previous steps\n"
    "- Use important columns mentioned\n"
    "- Produce the expected outputs\n"
    "- Follow assumptions and analysis goals if given\n\n"
    "Use print() before each result to explain what's being printed.\n"
    "Do not add comments or markdown. Return only executable code."
)

EXECUTOR_TEMPLATE = """
Step ID: {step}
Description: {description}
Goal: {goal}
Expected Outputs: {expected_outputs}
Assumptions: {assumptions}
Required Variables: {required_variables}

Schema Context:
{schema_context}

Respond with valid Python code only.
"""

executor_prompt = ChatPromptTemplate.from_messages([
    ("system", EXECUTOR_SYSTEM),
    ("user", EXECUTOR_TEMPLATE)
])
