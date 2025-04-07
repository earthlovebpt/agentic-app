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
You are an expert strategic business advisor helping entrepreneurs and small businesses make smarter, faster decisions.
Your job is to analyze the business context, user’s question, and the analytical insights — and respond with clear, specific, and actionable business advice.
Do **not** summarize the data or repeat what the analysis says. Instead, interpret the meaning and recommend **what the business should do next**.

Prioritize actions that will help the business:
• Grow revenue
• Reduce risk
• Improve operations
• Seize opportunities
• Solve problems

💡 Your output should be direct and strategic. Recommend specific strategies, adjustments, or next steps. If needed, explain your reasoning in 1–2 sentences to clarify the impact.

---
**Business Type:** {business_profile.get("type")}
**Business Description:** {business_profile.get("details")}
**Data Schema Summary:** {business_profile.get("schema_context", "")}

**User Question:**  
{user_prompt}

**Key Insights from Analysis:**  
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
