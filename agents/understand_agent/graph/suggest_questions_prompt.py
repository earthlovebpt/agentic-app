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

Suggest 3 to 5 high-impact business questions they should consider asking, based on their business and data. 
The questions should help them uncover growth opportunities, reduce cost, or improve operations.

Respond ONLY in this format:

{format_instructions}
"""

# -- LangChain PromptTemplate --
suggest_questions_prompt = ChatPromptTemplate.from_messages([
    ("system", SUGGEST_QUESTIONS_SYSTEM),
    ("user", SUGGEST_QUESTIONS_TEMPLATE)
])