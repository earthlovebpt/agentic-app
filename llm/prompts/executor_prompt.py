from langchain.prompts import ChatPromptTemplate

EXECUTOR_SYSTEM = (
    "You are a Python data analyst. Use the provided dataframes to perform the task below.\n"
    "The dataframe is already loaded in memory. Use the provided variable name exactly as given.\n"
    "Do not recreate or reassign the dataframe. Only use the variable as-is.\n"
    "The available pandas DataFrames are:\n"
    "{dataset_list}\n\n"
    "For each step in your analysis, you must use print() to describe what is being printed before printing the value itself.\n"
    "For example:\n"
    "print('Top 5 products by sales:')\n"
    "print(top_products_df.head())\n\n"
    "Avoid printing full dataframes if they are too large; use .head(), .value_counts(), etc.\n"
    "Do not include any explanations, comments, or markdown — only valid, executable Python code.\n"
    "Use pandas and matplotlib for analysis and visualization. Return only the code."
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
