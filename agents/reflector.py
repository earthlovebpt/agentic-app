from openai import OpenAI
import os
import logging
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reflect_on_results(user_prompt, results):
    summaries = "\n".join([r.get("summary", "") for r in results])

    insight_highlight = "\n".join([r.get("insight_highlights", "") for r in results])

    system_prompt = (
        "You are a reflection agent. Your job is to review the output from an analysis plan and determine "
        "if it sufficiently addresses the user's question. If not, suggest a new improved version of the question."
    )

    reflection_prompt = f"""
User Question:
{user_prompt}

Analysis Results:
{summaries}

Insight Highlights:
{insight_highlight}

Do the results answer the question effectively? If not, suggest how to replan. Respond with:
{{"replan": true/false, "new_prompt": "..."}}
"""

    try:
        logger.info("📤 [Reflection Prompt]\n%s", reflection_prompt)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": reflection_prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )
        result = response.choices[0].message.content
        logger.info("📥 [Reflection Response]\n%s", result)
        return json.loads(result)
    except Exception as e:
        return {"replan": False, "error": str(e)}