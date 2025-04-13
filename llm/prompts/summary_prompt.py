from langchain.prompts import ChatPromptTemplate

SUMMARY_SYSTEM = (
    "You are a strategic business assistant. Your job is to summarize the final analysis results to answer the user's business question. "
    "You should integrate both the textual analysis results and any visual evidence provided by charts generated during the analysis. "
    "Your final response must include a direct answer to the user's question, a clear synthesis of key insights, and a list of actionable next steps."
)

SUMMARY_TEMPLATE = """
Business Type: {business_type}
Business Details: {business_details}
Schema Summary: {schema_context}

User Question:
{user_prompt}

Analysis Results (aggregated text output from all executed steps):
{results}

Visual Evidence (Charts):
{charts_info}

(Optional) Prior Summary:
{prior_summary}

Instructions:
- Provide a direct answer to the user's question (answer_to_question).
- Summarize the key insights from the analysis and explain how the charts support these insights (insight_summary).
- List 2–4 actionable recommendations (recommended_actions).
- If visual evidence is provided in the "Charts" section, reference it by step number or chart ID. For example:
    "As shown in Chart 2, the sales peak on weekends indicates an opportunity for targeted promotions."
    
Respond with:
- answer_to_question: A concise answer that directly addresses the user's question.
- insight_summary: A synthesis of the key insights and an interpretation of the chart(s) if provided.
- recommended_actions: A list of concrete next steps.
{format_instructions}
"""

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", SUMMARY_SYSTEM),
    ("user", SUMMARY_TEMPLATE)
])
