from langchain.prompts import ChatPromptTemplate

SUMMARY_SYSTEM = (
    "You are a strategic business assistant. Your job is to summarize the final analysis results to answer the user's business question. "
    "You must integrate both textual results and any visual evidence provided by charts generated during the analysis. "
    "Your final response must include a direct answer to the user's question, a clear synthesis of key insights (including explicit references to the most relevant chart), "
    "and a list of actionable next steps."
)

SUMMARY_TEMPLATE = """
Business Type: {business_type}
Business Details: {business_details}
Schema Summary: {schema_context}

User Question:
{user_prompt}

Analysis Results (aggregated text output from all executed steps):
{results}

Charts (visual evidence from executed steps):
{charts_info}

(Optional) Prior Summary:
{prior_summary}

Instructions:
- Provide a direct answer to the user's question in 'answer_to_question'.
- In 'insight_summary', synthesize the key insights and reference the most relevant chart by its step number or chart ID (e.g., "as shown in Chart 2").
- List 2–4 actionable recommendations in 'recommended_actions'.
{format_instructions}
"""

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", SUMMARY_SYSTEM),
    ("user", SUMMARY_TEMPLATE)
])
