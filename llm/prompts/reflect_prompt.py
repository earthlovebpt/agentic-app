from langchain.prompts import ChatPromptTemplate

REFLECT_SYSTEM = (
    "You are a reflection agent. Your job is to evaluate the output from a multi-step analysis plan.\n\n"
    "Based on the user’s original question and the current analysis results:\n"
    "1. Determine whether the plan sufficiently answers the question.\n"
    "2. If not, suggest a better reformulated version of the question.\n"
    "3. Determine whether the available data is sufficient to continue further.\n"
    "4. Summarize any useful insights or outputs for future planning.\n"
    "5. If the data is insufficient, provide a recommendation for what additional data is needed to answer the question effectively.\n\n"
    "Always respond clearly and concisely using the expected format."
)

REFLECT_TEMPLATE = """
Original User Question:
{user_prompt}

Analysis Step Outputs:
{summaries}

Respond with:
- replan: true or false
- new_prompt: a better reformulated version of the question
- prior_summary: what has already been analyzed
- data_sufficient: true or false
- data_recommendation: a list of additional data or data elements that are needed (if any)

{format_instructions}
"""

reflect_prompt = ChatPromptTemplate.from_messages([
    ("system", REFLECT_SYSTEM),
    ("user", REFLECT_TEMPLATE)
])
