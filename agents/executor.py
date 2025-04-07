from openai import OpenAI
import os
import io
import contextlib
import logging
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
import json
import re
import streamlit as st
load_dotenv()
client = OpenAI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sanitize(name):
    """
    Convert a string into a valid Python variable name:
    - Lowercase
    - Replace spaces and dashes with underscores
    - Remove invalid characters
    - Add prefix if name starts with a digit
    """
    name = name.lower().strip()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub(r"\W", "", name)  # Remove all non-alphanumeric/underscore characters
    if re.match(r"^\d", name):
        name = f"df_{name}"  # Prefix if starts with a number
    return name

def strip_code_block(content):
    return content.strip().strip("`").replace("python", "").strip()

def explain_code(code):
    prompt = (
        "Explain the following Python data analysis code in simple language. "
        "Make it clear to a business user what this code is doing and what insights it is trying to extract.\n\n"
        f"{code}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful code explainer for business users."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Failed to explain code: {e}"

def highlight_insights(output_text):
    """
    Ask GPT to summarize the key insight and decide whether to show it.
    Returns: {"show": bool, "text": str}
    """
    prompt = f"""
You are a senior business consultant reviewing the results of a data analysis task.

Your job is to:
1. Summarize the most important business insight clearly and concisely — as if you are speaking to a CEO.
2. Focus not just on what the data says, but what it means: highlight risks, opportunities, patterns, or strategic takeaways.
3. Decide whether this insight is meaningful enough to display in the user interface.

Return JSON like:
{{"show": true, "text": "This is the insight"}}

Analysis Output:
\"\"\"{output_text}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful insight summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        content = response.choices[0].message.content.strip()
        logger.info("✨ [Insight Highlight Raw]\n%s", content)

        # clean up and parse
        cleaned = content.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)

    except Exception as e:
        logger.error("⚠️ Failed to parse insight response: %s", e)
        return {"show": False, "text": f"⚠️ Failed to summarize insight: {e}"}



def execute_plan(plan, datasets, schemas,business_profile):
    results = []

    dataset_list = "\n".join([
        f"{sanitize(name)}_df: {schemas[name]}" for name in datasets
    ])
    available_dfs = {f"{sanitize(name)}_df": df.copy() for name, df in datasets.items()}

    for i, task in enumerate(plan):
        task_description = task.get("description", "")
        system_prompt = (
            "You are a Python data analyst. Use the provided dataframes to perform the task below.\n"
            "The dataframe is already loaded in memory. Use the provided variable name exactly as given.\n"
            "Do not recreate or reassign the dataframe. Only use the variable as-is.\n"
            "The available pandas DataFrames are:\n"
            f"{dataset_list}\n\n"
            "For each step in your analysis, you must use print() to describe what is being printed before printing the value itself.\n"
            "For example:\n"
            "print('Top 5 products by sales:')\n"
            "print(top_products_df.head())\n\n"
            "Avoid printing full dataframes if they are too large; use .head(), .value_counts(), etc.\n"
            "Do not include any explanations, comments, or markdown — only valid, executable Python code.\n"
            "Use pandas and matplotlib for analysis and visualization. Return only the code."
        )

        schema_context = business_profile.get("schema_context", "")
        sample_rows_context = "\n\n".join([
            f"{sanitize(name)}_df (first 3 rows):\n{df.head(3).to_markdown()}" for name, df in datasets.items()
        ])

        user_prompt = f"""
Task: {task_description}

{schema_context}
{sample_rows_context}

Respond ONLY with valid Python code.
"""
        with st.spinner(f"🧠 Running step {i+1} of {len(plan)}..."):
            try:
                logger.info("📤 [GPT PROMPT]\n%s\n---", user_prompt)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1200
                )

                code = response.choices[0].message.content
                logger.info("📥 [GPT RESPONSE]\n%s\n---", code)

                code = strip_code_block(code)
                code = code.replace("plt.show()", "")
                exec_env = {**available_dfs, "pd": pd, "plt": plt}

                stdout_capture = io.StringIO()
                chart_path = None

                with contextlib.redirect_stdout(stdout_capture):
                    exec(code, exec_env)
                    fig = plt.gcf()
                    if fig.get_axes():
                        chart_path = f"/tmp/chart_{task['step']}.png"
                        fig.savefig(chart_path)
                        plt.close(fig)

                output_text = stdout_capture.getvalue().strip()
                explanation = explain_code(code)
                highlight_result = highlight_insights(output_text)
                logger.info("🧾 [Code Explanation]\n%s", explanation)
                logger.info("✨ [Insight Highlight]\n%s", highlight_result)

                results.append({
                    "summary": output_text or "✅ Code executed.",
                    "chart": chart_path if chart_path else None,
                    "code_explanation": explanation,
                    "insight_highlights": highlight_result["text"],
                    "show_insight": highlight_result["show"]
                })

            except Exception as e:
                results.append({
                    "summary": f"⚠️ Failed to execute '{task_description}': {e}"
                })

    return results