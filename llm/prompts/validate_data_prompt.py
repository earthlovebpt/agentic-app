from langchain.prompts import ChatPromptTemplate

SYSTEM_VALIDATE_DATA_PROMPT = (
    "You are a data validator AI. Given the available data schema and a user question, "
    "determine whether the current data is sufficient to answer the question.\n\n"
    "- If yes, return `data_sufficient: true`\n"
    "- If not, suggest specific tables or columns that are missing OR suggest similar questions "
    "that can be answered with the current data.\n\n"
    "Respond in this format:\n"
    "{format_instructions}"
)

USER_VALIDATE_DATA_PROMPT = "Available schema:\n{schema_context}\n\nUser Question:\n{user_prompt}"

validate_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_VALIDATE_DATA_PROMPT),
    ("user", USER_VALIDATE_DATA_PROMPT)
])
