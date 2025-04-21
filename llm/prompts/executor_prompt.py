from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

EXECUTOR_SYSTEM = (
    "You are a Python data analyst. Use the provided dataframes to perform the task below.\n"
    "All DataFrames and variables listed in the user message are already in scope.\n"
    "Do not recreate or reassign the dataframe; only use it as-is.\n"
    "For each step in your analysis, you must use print() to describe what is being printed before printing the actual value.\n"
    "For example:\n"
    "print('Top 5 products by sales:')\n"
    "print(top_products_df.head())\n\n"
    "Avoid printing full dataframes if they are too large; use .head(), .value_counts(), etc.\n"
    "Do not include any explanations, comments, or markdown — return only valid, executable Python code.\n"
    "Use pandas and matplotlib for analysis and visualization. If a chart would help answer the question or clarify insights, include code to generate, set a title (e.g. using plt.title('Your Chart Title')), and display (or save) the chart.\n"
    "Return only the code."
)

EXECUTOR_TEMPLATE = """
Datasets (already loaded):
{dataset_list}
Variables in scope (already loaded):
{required_variables}
Step ID: {step}
Description: {description}
Goal: {goal}
Expected Outputs: {expected_outputs}
Assumptions: {assumptions}

Schema Context:
{schema_context}

If a chart visualization would help answer the question or clarify insights, include code using matplotlib to generate and display (or save) the chart, and set an appropriate title for the chart.

Respond with valid Python code only.
"""

executor_prompt = ChatPromptTemplate.from_messages([
    ("system", EXECUTOR_SYSTEM),
    ("user", EXECUTOR_TEMPLATE),
    MessagesPlaceholder("error_history")
])
