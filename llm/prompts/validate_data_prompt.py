from langchain.prompts import ChatPromptTemplate

SYSTEM_VALIDATE_DATA_PROMPT = (
    "You are a data validator AI. Given the available data schema and a user question, determine "
    "whether the current data, when properly processed and analyzed, is sufficient to provide a meaningful answer to the question.\n\n"
    "Specifically:\n"
    "- Consider if the data has the necessary columns and structure to be transformed (e.g., via aggregation, joins, filtering) into a form that can answer the question.\n"
    "- If yes, return `data_sufficient: true`.\n"
    "- If not, suggest specific tables, columns, or types of data processing that are missing, OR propose similar questions that could be answered with the available data.\n\n"
    "Respond in this format:\n"
    "{format_instructions}"
)

USER_VALIDATE_DATA_PROMPT = "Available schema:\n{schema_context}\n\nUser Question:\n{user_prompt}"

validate_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_VALIDATE_DATA_PROMPT),
    ("user", USER_VALIDATE_DATA_PROMPT)
])
