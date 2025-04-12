from openai import OpenAI
import os
import logging
from dotenv import load_dotenv
import pandas as pd
import io
import contextlib
import re

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

def explore_datasets_agentically(datasets: dict, schemas: dict) -> str:
    """
    Let GPT write EDA code to run on real dataframes, then summarize the output.
    Returns a markdown summary from GPT based on real results.
    """
    code_prompt = (
        "You are a Python data analyst. You are provided with a real, pre-loaded pandas dataframe.\n"
        "You are also given a short description of each column.\n"
        "Do not create or simulate any new data. Use only the provided dataframe.\n\n"
        "Carefully read the column descriptions to understand what the data represents.\n"
        "Think about what is useful to know in order to understand the dataset better and plan future analysis steps.\n\n"
        "Write Python code to explore the structure and meaning of the data. Use pandas to:\n"
        "- Print the number of rows and columns\n"
        "- Print column names and data types\n"
        "- Print missing values per column\n"
        "- Print summary statistics for numeric columns\n"
        "- If datetime columns exist, print their min and max range\n"
        "- If any columns seem categorical, print how many unique values they contain\n"
        "- Feel free to add any additional simple checks that help explain what this dataset is about\n\n"
        "Use print() to output all findings clearly.\n"
        "Do not include markdown, comments, or explanations — only raw, executable Python code."
    )


    exec_env = {"pd": pd}
    summary_log = ""

    for name, df in datasets.items():
        df_name = f"{sanitize(name)}_df"
        exec_env[df_name] = df.copy()

        sample_context = f"""Dataset: {df_name}

Sample Rows:
{df.head(3).to_markdown()}

Schema Description:
{schemas.get(name, '')}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": code_prompt},
                    {"role": "user", "content": sample_context}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            gpt_code = response.choices[0].message.content.strip().replace("```python", "").replace("```", "")
            logger.info(f"📤 [GPT EDA Code for {df_name}]:\n{gpt_code}")

            stdout_capture = io.StringIO()
            with contextlib.redirect_stdout(stdout_capture):
                exec(gpt_code, exec_env)

            output_text = stdout_capture.getvalue().strip()
            summary_log += f"### Dataset `{df_name}`\n```\n{output_text}\n```\n\n"

        except Exception as e:
            logger.error("❌ EDA execution failed for %s: %s", df_name, e)
            summary_log += f"### Dataset `{df_name}`\n⚠️ Failed to generate EDA: {e}\n\n"

    summarizer_prompt = f"""
You are a business data analyst. Read the following EDA output logs and summarize each dataset.

Focus on:
- Row/column counts
- Key column types and ranges
- High-level patterns
- Any interesting business-related structure

Here are the results:

{summary_log}

Return a markdown-formatted summary.
"""

    try:
        summary_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful business analyst."},
                {"role": "user", "content": summarizer_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        summary_text = summary_response.choices[0].message.content
        logger.info("📥 [EDA Summary]\n%s", summary_text)
        return summary_text

    except Exception as e:
        logger.error("❌ Failed to summarize EDA output: %s", e)
        return "⚠️ Failed to summarize EDA results."
