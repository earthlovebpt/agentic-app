from langchain.prompts import ChatPromptTemplate

SUMMARY_SYSTEM = (
    "You are a strategic business assistant. Your job is to summarize the final analysis results to guide the business owner. "
    "You must integrate both the textual results and any visual evidence provided by charts generated during the analysis. "
    "If the data is conclusive, provide a direct answer to the user's question; however, if the evidence is inconclusive or insufficient "
    "to yield a definitive answer, clearly state that uncertainty and focus on delivering a clear synthesis of insights along with actionable next steps."
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
- Provide a direct answer to the user's question in 'answer_to_question' if the data is conclusive; if not, state that the data does not allow for a definitive answer.
- In 'insight_summary', synthesize the key insights, referencing the most relevant chart by Chart ID (e.g., "as shown in chart_2"), to support your analysis.
- List 2–4 actionable recommendations in 'recommended_actions'.
{format_instructions}
"""

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", SUMMARY_SYSTEM),
    ("user", SUMMARY_TEMPLATE)
])
