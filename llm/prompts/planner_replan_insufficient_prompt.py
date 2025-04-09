from langchain.prompts import ChatPromptTemplate

REPLAN_INSUFFICIENT_SYSTEM = (
    "You are a strategic data planner. The user's original question could not be answered due to insufficient data.\n"
    "Your job is to create a new analysis plan using the available datasets and business context.\n"
    "Suggest a new direction for analysis that still helps the business based on the original question."
)

REPLAN_INSUFFICIENT_TEMPLATE = """
Business Type: {business_type}
Business Details: {business_details}

Schema Context:
{schema_context}

Original Question:
{user_prompt}

Prior Summary:
{prior_summary}

Memory Log (what was already tried or failed):
{memory_log}

Return a new list of analysis steps in this format:

{format_instructions}

Guidelines:
- Plan steps that use available data meaningfully.
- Avoid steps that require unavailable data.
- Pivot the strategy if necessary (e.g., from user segmentation to product analysis).
- Each step should describe a valuable insight or comparison the business can act on.
"""

planner_replan_insufficient_prompt = ChatPromptTemplate.from_messages([
    ("system", REPLAN_INSUFFICIENT_SYSTEM),
    ("user", REPLAN_INSUFFICIENT_TEMPLATE)
])
