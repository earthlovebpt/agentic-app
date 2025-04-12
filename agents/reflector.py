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
        "You are a reflection agent. Your job is to review the output from an analysis plan and determine:\n"
        "- Whether it sufficiently answers the user's question\n"
        "- If not, suggest a better follow-up version of the question\n"
        "- Provide a summary of what was learned so far to inform the next planning step\n\n"
        "You must respond in the following JSON format:\n"
        "{\n"
        "  \"replan\": true or false,\n"
        "  \"new_prompt\": \"...\",         // a refined question if replan is needed\n"
        "  \"prior_summary\": \"...\"       // what was learned, in a way useful for the planner\n"
        "}\n\n"
        "Do not explain or add commentary. Only return valid JSON."
    )

    reflection_prompt = f"""
User Question:
{user_prompt}

Analysis Results:
{summaries}

Insight Highlights:
{insight_highlight}

Based on the above, decide if further planning is needed. If yes, suggest a better next question and summarize what was already discovered.
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