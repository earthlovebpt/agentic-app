# agents/suggestion.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def get_strategic_question_suggestions(business_profile):
    business_type = business_profile.get("type", "")
    business_details = business_profile.get("details", "")
    schema_context = business_profile.get("schema_context", "")

    prompt = f"""
You are a strategic consultant helping a business owner make better decisions.

Business Type: {business_type}
Business Details: {business_details}

Data Schema:
{schema_context}

Suggest 3 to 5 high-impact business questions they should consider asking, based on their business and data. 
The questions should help them uncover growth opportunities, reduce cost, or improve operations.

Return as a plain list, like:
- Which products drive the most profit?
- What time of day has the highest sales?
- ...
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart strategic consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        raw_text = response.choices[0].message.content
        suggestions = [line.strip("- ").strip() for line in raw_text.strip().splitlines() if line.startswith("-")]
        return suggestions or [raw_text]
    except Exception as e:
        return [f"⚠️ Failed to generate suggestions: {e}"]
