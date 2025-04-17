from langchain.prompts import ChatPromptTemplate

# SYSTEM_VALIDATE_DATA_PROMPT = (
#     "You are a data validator AI. Given the available data schema and a user question, determine "
#     "whether the current data, when properly processed and analyzed, is sufficient to provide a meaningful answer to the question.\n\n"
#     "Specifically:\n"
#     "- Consider if the data has the necessary columns and structure to be transformed (e.g., via aggregation, joins, filtering) into a form that can answer the question.\n"
#     "- If yes, return `data_sufficient: true`.\n"
#     "- If not, suggest specific tables, columns, or types of data processing that are missing, OR propose similar questions that could be answered with the available data.\n\n"
#     "Respond in this format:\n"
#     "{format_instructions}"
# )

SYSTEM_VALIDATE_DATA_PROMPT = """You are a professional data scientist who has abundance of experience working with data across various business domains.
You are exceptionally proficient in identifying whether the available data is sufficient to provide a meaningful answer to a user question.
"""

# USER_VALIDATE_DATA_PROMPT = "Available schema:\n{schema_context}\n\nUser Question:\n{user_prompt}"

USER_VALIDATE_DATA_PROMPT = """Take a deep breath and think step-by-step. Think in gradually increasing complexity.

You are given a schema description of a business's internal data under the tag <schema_context></schema_context> and a user question under the tag <user_prompt></user_prompt>.
Your task is to determine whether the available data, when properly processed and feature-engineered, is enough to do modeling or data manipulation or visualization to answer the user prompt in a meaningful way.

Here's the detailed instruction:

1. **Step 1: Understand the User Prompt**
   - Read the <user_prompt> carefully.
   - Ask: What is the user really trying to understand or achieve?
   - Is it a metric they’re tracking? A trend? A segmentation? A forecast?
   - ⚠️ *Caution:* Be mindful of implicit expectations in the prompt — e.g., time granularity, aggregation, entity relationships, or business definitions.

2. **Step 2: Review the Schema Context**
   - Read the <schema_context> and identify:
     - Relevant tables
     - Key fields (e.g., timestamps, IDs, categories, numerical metrics)
     - Existing relationships or business logic embedded in the schema
   - Look for missing elements: Is a necessary table or field absent? Can it be inferred or engineered?

3. **Step 3: Match the Prompt with the Schema**
   - Map elements of the user’s request to the schema:
     - Are all needed data points present (directly or indirectly)?
     - Are transformations or joins possible to create the right view?
     - Is time, granularity, or scope aligned?
   - ⚠️ *Caution:* Do not assume fields exist unless explicitly listed or clearly inferable from schema relationships.

4. **Step 4: Determine Sufficiency**
   - Ask yourself: Can I reasonably build a dataset from this schema that answers the prompt — even with extra processing?
   - If **yes**, mark `"data_sufficient": true`
   - If **no**, mark `"data_sufficient": false`, and explain why in the `thoughts` and `suggestions`.

5. **Step 5: Provide Actionable Suggestions**
   - What would help the user get closer to their answer?
     - Additional columns?
     - A new table?
     - Clarification of business logic?
     - A time filter or derived metric?
   - ⚠️ *Caution:* Keep suggestions practical and relevant to the schema and the user's business context.


You MUST respond in the following JSON format

```json
{{
    "thoughts": "(str) Your understanding of the user prompt and your thought on whether the available data is sufficient to answer the user question: what they are missing, what can be done to help this",
    "data_sufficient": "(bool) Whether the available data is sufficient to answer the user question",
    "recommendations": "(str) A list of suggestions to help the user question be answered with the available data"
}}   
```
If you do this task well, I will tip you 200 U.S.Dollars.

<schema_context>
{schema_context}
</schema_context>

<user_prompt>
{user_prompt}
</user_prompt>
"""

validate_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_VALIDATE_DATA_PROMPT),
    ("user", USER_VALIDATE_DATA_PROMPT)
])
