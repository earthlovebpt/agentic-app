from langchain.prompts import ChatPromptTemplate

SUMMARY_SYSTEM = (
    "You are a strategic business assistant. Your job is to:\n"
    "- Directly answer the user's business question using the analysis results\n"
    "- Summarize broader insights from the data\n"
    "- Recommend 2–4 actionable next steps the business owner can take\n\n"
    "Avoid repeating raw data. Focus on interpretation and strategy."
)

SUMMARY_TEMPLATE = """
Business Type: {business_type}
Details: {business_details}
Schema Summary: {schema_context}

User Question:
{user_prompt}

Analysis Results:
{results}

Insight Highlights:
{insight_highlights}

(Optional) Prior Summary:
{prior_summary}

Respond with:
- answer_to_question: directly answer the user’s original question
- insight_summary: any broader important findings
- recommended_actions: a list of 2–4 concrete business actions

{format_instructions}
"""

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", SUMMARY_SYSTEM),
    ("user", SUMMARY_TEMPLATE)
])
