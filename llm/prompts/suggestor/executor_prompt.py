from langchain.prompts import ChatPromptTemplate

from llm.prompts.executor_prompt import EXECUTOR_TEMPLATE

# EXECUTOR_SYSTEM = (
#     "You are a Python data analyst. Use the provided dataframes to perform the task below.\n"
#     "The dataframe is already loaded in memory. Use the provided variable name exactly as given and only work with the column names in the provided schema context.\n"
#     "Do not recreate or reassign the dataframe; only use it as-is.\n"
#     "The available pandas DataFrames are:\n"
#     "{dataset_list}\n\n"
#     "For each step in your analysis, you must use print() to describe what is being printed before printing the actual value.\n"
#     "For example:\n"
#     "print('Top 5 products by sales:')\n"
#     "print(top_products_df.head())\n\n"
#     "Avoid printing full dataframes if they are too large; use .head(), .value_counts(), etc.\n"
#     "Do not include any explanations, comments, or markdown — return only valid, executable Python code.\n"
#     "Use pandas and matplotlib for analysis and visualization. If a chart would help answer the question or clarify insights, include code to generate, set a title (e.g. using plt.title('Your Chart Title')), and display (or save) the chart.\n"
#     "Return only the code."
# )
EXECUTOR_SYSTEM = """You are a professional data scientist who has abundance of experience working with data across various business domains.
You are exceptionally proficient in Python coding from a given detailed instruction written in natural language.
You are very good at your job because you are detail-oriented and truly understand the problem at hand both technically and strategically and can translate to Python language very well.
"""

# EXECUTOR_TEMPLATE = """
# Step ID: {step}
# Description: {description}
# Goal: {goal}
# Expected Outputs: {expected_outputs}
# Assumptions: {assumptions}
# Required Variables: {required_variables}

# Schema Context:
# {schema_context}

# Error Message from Previous Run (if any): {error_message}

# If an error message is provided (i.e. it is not empty), generate new code that addresses and fixes this error.
# If a chart visualization would help answer the question or clarify insights, include code using matplotlib to generate and display (or save) the chart, and set an appropriate title for the chart.

# Respond with valid Python code only.
# """

EXECUTOR_TEMPLATE = """
You are given a task that describes what you need to do and what would you expect when finishing the task. A given task has these attributes 
- <step_id>: A unique ID specifying this task
- <task_description>: Task description describing what is done in this step — with enough detail that an analyst or coder can implement it correctly.
- <task_goal>: Task goal specifying why this step is important
- <task_expected_outputs>: A concrete description of what result this step should return (e.g., a dataframe, model object, or aggregated metric).
- <task_assumptions>: Important assumptions about data format, column presence, types, or distributions.
- <task_required_variables>: What variables are required to execute the step (e.g., dataframe names, parameters, models).
- <task_required_libs>: What library or packages are necessary to perform this task.
- <outputs>: What variables will be produced by this step and passed to the next step(s).

Apart from the task, you are also given the business's internal data schema as well to help you understand what you're dealing with under the tag <schema_context></schema_context>

Your task is to create a single code block that starts with ```python and ends with ``` that performs the given task as described by all its attribute. You can comment your code to help with your understanding but it's not necessary.
Within your code block, you MUST print whatever insights or analysis you find by first printing the description and then the actual value as these will be gathered from stdout and used in later process. For example, print('Top 5 products by sales:') followed by
print(top_products_df.head()). Avoid printing the whole dataframe which would take up a lot of memory in stdout. Instead, print only head or use describe. If a chart visualization would help answer the question or clarify insights, include code using matplotlib to generate and display (or save) the chart, and set an appropriate title for the chart.

All the necessary variables are loaded within your execution environment already so you don't have to load anything or read any files within your code. The available variables are {variables_list}.

You are also given an error message under the tag <error_msg> which specifies what error occurred on the previous attempt at doing this task step. If the provided error message is not an empty string, you MUST write the code that addresses and fix the error as well! This is REALLY IMPORTANT. If you do this well, I will tip you an additional 50 US DOllars.
Here's the detailed instruction:

You MUST respond in the following JSON format
```json{{
    "reasoning": "(str) Your reasoning on what you need to do with this code including common pitfalls, cautions, etc."
    "code": "(str) Your Python code doing the given task. The code should start with ```python and end with ```.
}}
```

<step_id>{step}</step_id>
<task_description>{description}</task_description>
<task_goal>{goal}</task_goal>
<task_expected_outputs>{expected_outputs}</task_expected_outputs>
<task_assumptions>{assumptions}</task_assumptions>
<task_required_variables>{required_variables}</task_required_variables>
<task_required_libs>{required_libs}</task_required_libs>
<outputs>{outputs}</outputs>

<dataset_list>{variables_list}</dataset_list>
<schema_context>{schema_context}</schema_context>
<error_msg>{error_msg}</error_msg>
"""

executor_prompt = ChatPromptTemplate.from_messages([
    ("system", EXECUTOR_SYSTEM),
    ("user", EXECUTOR_TEMPLATE)
])
