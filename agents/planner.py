from openai import OpenAI
import os
import logging
import ast
from dotenv import load_dotenv
import re
import json

def auto_fix_json(text: str):
    """
    Try to extract and clean a list of steps from messy GPT output.
    Assumes the content includes at least one list of dicts.
    """
    try:
        # Remove markdown and newlines
        cleaned = text.replace("```json", "").replace("```python", "").replace("```", "").strip()

        # Find the first list of dicts using regex
        match = re.search(r"\[\s*\{.*?\}\s*\]", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("No JSON-like list of steps found.")
    except Exception as e:
        return [{"step": "fallback", "description": f"auto_fix_json failed: {e}"}]

load_dotenv()
client = OpenAI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def plan_tasks(user_prompt, business_profile,is_replanned=False,prior_summary=None):
    business_type = business_profile.get("type", "")
    business_details = business_profile.get("details", "")
    schema_context = business_profile.get("schema_context", "")

    system_prompt = (
        "You are a smart data analyst. Your job is to help a business owner by creating an analysis plan "
        "based on their business type, details, available datasets, and their question.\n\n"
        "Return a list of steps like this:\n"
        "[\n"
        "  {\"step\": \"analyze_top_products\", \"description\": \"Analyze top-selling products by category\"},\n"
        "  {\"step\": \"compare_monthly_trends\", \"description\": \"Compare sales across months\"}\n"
        "]"
    )

    full_context = f"""
Business Type: {business_type}
Business Details: {business_details}

Data Schema:
{schema_context}

User Question:
{user_prompt}
"""

    if is_replanned and prior_summary:
        full_context += f"""

This is a continuation of a previous analysis.

What has already been done:
{prior_summary}

Do NOT repeat these steps. Your task is to plan what to do next to help answer the user's question more completely.

Focus on high-level, useful steps — not overly detailed ones.
"""

    logger.info("📤 [Planner Prompt]\n%s", full_context)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_context}
        ],
        temperature=0.3,
        max_tokens=800
    )
    raw = response.choices[0].message.content
    logger.info("📥 [Planner Response]\n%s", raw)

    # Clean markdown/code formatting if any
    cleaned = raw.replace("```json", "").replace("```python", "").replace("```", "").strip()

    try:
        # Parse into Python object safely
        return ast.literal_eval(cleaned)
    except Exception as e:
        logger.warning("🧪 literal_eval failed: trying auto_fix_json...")
        return auto_fix_json(raw)
