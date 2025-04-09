from langchain.prompts import ChatPromptTemplate

# -- SYSTEM --
PLANNER_SYSTEM = (
    "You are a strategic data planner helping a business owner analyze their data in multiple steps. "
    "Your job is to break the problem into smart, executable steps based on their goal and data.\n\n"
    "Each step must be:\n"
    "- A complete, logical unit of analysis\n"
    "- Executable in one code block\n"
    "- Focused on moving the analysis forward (avoid tiny substeps)\n\n"
    "Include:\n"
    "- `step`: machine-friendly name\n"
    "- `description`: instruction of what to do\n"
    "- `goal`: the purpose of the step\n"
    "- `expected_outputs`: names or types of output\n"
    "- `assumptions`: expected data shape or availability\n"
    "- `required_variables`: inputs from prior steps\n"
    "- `outputs`: variables to produce for next steps"
)

# -- TEMPLATE: First Plan --
PLANNER_TEMPLATE = """
Business Type: {business_type}
Business Details: {business_details}

Available Datasets and Schema:
{schema_context}

User Question:
{user_prompt}

Return a list of analysis steps in this format:
{format_instructions}

Guidelines:
- Only include necessary, high-impact steps
- Reuse outputs from prior steps when helpful
"""

planner_prompt = ChatPromptTemplate.from_messages([
    ("system", PLANNER_SYSTEM),
    ("user", PLANNER_TEMPLATE)
])
