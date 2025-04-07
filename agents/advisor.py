from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_advice(user_prompt, results, business_profile):
    summaries = "\n".join([res["insight_highlights"] for res in results if "summary" in res])
    context = f"""
You are a strategic business advisor. Based on the business details, user question, and analysis results below — 
your job is to give clear, actionable recommendations.

• Do not summarize the data — instead, interpret what the business should do next.
• Focus on helping the user grow their business, solve a problem, or seize an opportunity.
• Be specific: Recommend strategies, changes, or next steps.
• If needed, explain your reasoning in one or two sentences.

---

Business Type: {business_profile.get("type")}
Details: {business_profile.get("details")}
Schema Summary: {business_profile.get("schema_context", "")}

User Question:
{user_prompt}

Analysis Results:
{summaries}
"""

    try:
        logger.info("📤 [Advisor Prompt]\n%s", context)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful and strategic business advisor."},
                {"role": "user", "content": context}
            ],
            temperature=0.7,
            max_tokens=500
        )
        result = response.choices[0].message.content
        logger.info("📥 [Advisor Response]\n%s", result)
        return result
    except Exception as e:
        return f"⚠️ Failed to generate advice: {e}"
