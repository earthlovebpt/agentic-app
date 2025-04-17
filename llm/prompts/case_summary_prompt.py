from langchain.prompts import ChatPromptTemplate

CASE_SUMMARY_SYSTEM = """
You are a business analyst assistant who is very good at summarizing scraped case studies which might contain a lot of noises and unwanted information into concise actionable items and their respective effect on the business."""

CASE_SUMMARY_TEMPLATE = """
Take a deep breath and think step by step. Think in gradually increasing complexity

You are given a business profile under the tag <business_profile> and a case study under the tag <case_study> and a case study title under the tag <case_study_title>.
Your task is to extract list of actionables steps and their impact on the business in the case study. However, the case study is scraped from the internet and might contain irrelevant information. In that case,
identify only the relevant information based on your knowledge and the given case study title. You need to also extract a business profile from the case study as well. This will be usefull in later process.

Here's the detailed instruction of how to do the task.

### STEP 1: Understand the Case Study
- Read the title and scan through the full content.
- Ask yourself: *What was this business trying to do? What was the challenge, and what solution did they try?*
- Do **not** focus on general descriptions or introductions unless they provide business-specific actions or outcomes.

### STEP 2: Construct Business Profile from Case Study
- Based on the information you gathered from the case study, construct a business profile that captures the essence of the case study.
- This will be used to guide the analysis of actionable steps and their impact on the business.
- Furthermore, this will be used to compare with the target business profile to see if the case study is relevant to the target business.

### STEP 2: Identify Actionable Steps
- Look for **concrete decisions** or **experiments** that were implemented (e.g. launching a loyalty program, redesigning a menu, relocating, changing suppliers, partnering with influencers).
- Each step should be:
  - **Specific** (not vague or general business advice)
  - **Intentional** (a deliberate strategy or tactic)
  - **Measurable** (ideally, it resulted in a clear change or outcome)

### STEP 3: Understand the Impact
- For each step, examine how it affected the business in the case study.
- Look for mentions of results (e.g., increased revenue, improved retention, reduced costs, more foot traffic).
- If metrics are not available, infer plausible impact based on the change described.

### STEP 4: Be Cautious
- If the case study includes speculation or vague claims, avoid treating them as verified results.
- Do not include any steps that are purely opinion-based or unrelated to business performance.

### STEP 5: Structure Your Output
- Summarize your thoughts on the case study at the beginning.
  - Mention how many relevant actionables you found.
  - Mention your general understanding of what the business did and why it worked (or didn’t).
- Then, list each actionable with its impact, in JSON format.

Your output MUST be in the following format:

```json{{
    "thoughts": "(str) Your thought on understanding of the case study and briefly list out how many actionables steps and their impact on the business are there",
    "business_profile": "(str) The business profile constructed from the case study",
    "actionables": [
        {{
            "step": "(str) The actionable step",
            "impact": "(str) The impact of the step on the business"
        }}
    ]
}}```
---

<business_profile>
{business_profile}
</business_profile>

<case_study_title>
{case_study_title}
</case_study_title>

<case_study>
{case_study_text}
</case_study>

"""

case_summary_prompt = ChatPromptTemplate.from_messages([
    ("system", CASE_SUMMARY_SYSTEM),
    ("user", CASE_SUMMARY_TEMPLATE)
])