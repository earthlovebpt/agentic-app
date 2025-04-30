from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel

WEB_SUMMARY_SYSTEM = """
You are a helpful and analytical assistant who are very good at answering user questions from the scraped web pages obtained from search engine"""

WEB_SUMMARY_TEMPLATE = """
Take a deep breath and think step by step. Think in gradually increasing complexity

You are given a question posed by the user under the tag <question>, a web title under the tag <web_title> and a scraped HTML web content under the tag <web_content>.
Your task is to summarize the web content and title and generate the answer to the question posed by the user.

Here's the detailed instruction of how to do the task.

1. **Read and Understand**:
   - Carefully read the <question> to understand what the user wants to know.
   - Read the <web_title> to get a high-level idea of the web content.
   - Read through the <web_content>, making sure to ignore irrelevant HTML fragments or boilerplate content.

2. **Analyze Content**:
   - Identify key insights, facts, or procedures from the content.
   - Understand how the content relates to the user’s question.
   - Extract meaningful data, explanations, examples, or strategies that address the question.

3. **Construct the "thought" field**:
   - Write a reflection showing your understanding of the content.
   - Describe whether and how the content addresses the user's question.
   - If multiple key points are relevant, briefly mention them and their role in shaping the answer.

4. **Construct the "summary" field**:
   - Write a clear, concise answer to the question based strictly on the given web content.
   - If the question cannot be directly answered, infer the best possible summary from available evidence.

5. **Cautions**:
   - Do NOT hallucinate information—only use what’s present in the <web_content>.
   - Do NOT include raw HTML or unrelated parts like menus, ads, or comments.
   - Ensure your summary directly and clearly responds to the user's intent in the <question>.
   - Keep your tone informative and objective.

Be concise but insightful. Think like a helpful analyst distilling useful information from a website to give a precise answer.

Your output MUST be in the following format:

```json{{
    "thought": "(str) Your thought on understanding of the website content and how it can answer the user question",
    "summary": "(str) Brief answer to the question posed by the user",
}}```
---

<question>
{question}
</question>

<web_title>
{web_title}
</web_title>

<web_content>
{web_content}
</web_content>

"""

web_summary_prompt = ChatPromptTemplate.from_messages([
    ("system", WEB_SUMMARY_SYSTEM),
    ("user", WEB_SUMMARY_TEMPLATE)
])


class WebSummaryOutput(BaseModel):
    thought: str
    summary: str