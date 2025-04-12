from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

from jinja2 import Template
import json

load_dotenv()
client = OpenAI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_path = __file__
prompt_dir = os.path.join(os.path.dirname(os.path.dirname(_path)), "prompts")

#Utility for loading prompt
def load_prompt(file_path):
    with open(file_path, "r") as file:
        return Template(file.read())

def generate_advice(user_prompt, results, business_profile):
    insight_highlight = "\n".join([r.get("insight_highlights", "") for r in results])

    context = load_prompt(os.path.join(prompt_dir, "advisor", "advisor_prompt.md"))
    context = context.render({
        "user_prompt": user_prompt,
        "insight_highlights": insight_highlight,
        "business_profile": business_profile})

    try:
        logger.info("📤 [Advisor Prompt]\n%s", context)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful and strategic business advisor."},
                {"role": "user", "content": context}
            ],
            temperature=0.7,
            max_tokens=4096
        )
        result = response.choices[0].message.content
        cleaned = result.replace("```json", "").replace("```", "").strip()
        logger.info("📥 [Advisor Response]\n%s", result)
        return json.loads(cleaned)
    except Exception as e:
        return f"⚠️ Failed to generate advice: {e}"
