from langchain.prompts import ChatPromptTemplate

# -- SYSTEM ROLE --
SUGGEST_QUESTIONS_SYSTEM = (
    "You are a strategic business assistant helping users explore their data. "
    "Your job is to suggest clear, specific, and high-impact questions based on business goals and data structure."
)

# -- USER PROMPT TEMPLATE --
SUGGEST_QUESTIONS_TEMPLATE = """
A business owner is using an AI assistant to explore their datasets.

Business Type: {business_type}
Business Details: {business_details}

Available Datasets and Schema:
{schema_context}

Based on this information, suggest 3–5 questions they could ask to gain insights or make better decisions.

The questions should:
- Be relevant to the business type and data
- Encourage grouping, filtering, time-series, or customer behavior analysis
- Mention relevant dataset or column names where possible
- Avoid overly generic questions like "What should I do?"

Respond ONLY in this format:

{format_instructions}
"""

# -- LangChain PromptTemplate --
suggest_questions_prompt = ChatPromptTemplate.from_messages([
    ("system", SUGGEST_QUESTIONS_SYSTEM),
    ("user", SUGGEST_QUESTIONS_TEMPLATE)
])