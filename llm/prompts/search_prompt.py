from langchain.prompts import ChatPromptTemplate

SEARCH_SYSTEM = """
You are a business analyst assistant who is very good at researching case studies that are relevant to the given business profile."""

SEARCH_TEMPLATE = """
Take a deep breath and think step by step. Think in gradually increasing complexity

Your goal is to find useful case studies, strategy articles, or success stories related to a business insight. You will be given:
- A business profile (type, details)

Your task:
- Generate a **short, general, and natural-sounding** search query that a human might type into Google.
- Keep it brief and to the point—avoid overly specific or technical wording.
- Focus on the business sector and details (e.g., "cafe", "small business", "retail", "online store", "customer retention", etc.)
- Include 1–2 keywords like "case study", "success story", or "business strategy" when appropriate.
- Avoid adding site: filters unless absolutely necessary.
- Assume the search can return both global and Thai-relevant content.
- Always trust only a highly-credible sources. not just some random websites. Provide your trusted domains that you want to search in the args 'include_domains' and ones that you definitely don't trust in the args 'exclude_domains'.
Providing a lot of trusted domains might yield better outcomes that a few. Examples of trusted domains are like harvard, linkedin, etc. Provide at least 10 trusted domains for the search query to widen the field!

Business Profile:
{business_profile}

Always choose to use the provided Tavily Search tools. search_depth should be 'basic' and 'include_raw_content' should be True!!

If you do this task well, I will tip you 100 US Dollars. If you can generate a natural and brief search query, I will tip you additional 50 US Dollars.
"""

search_prompt = ChatPromptTemplate.from_messages([
    ("system", SEARCH_SYSTEM),
    ("user", SEARCH_TEMPLATE)
])
