from langchain.prompts import ChatPromptTemplate

# REPLAN_EXECUTION_SYSTEM = (
#     "You are a planning agent in a multi-step data analysis assistant.\n"
#     "The user wants to answer a specific business question through data. You created a plan of steps, "
#     "but one of those steps failed — either due to a logic issue or insufficient data.\n\n"

#     "Your job now is to replan **starting from the failed step**. You must:\n"
#     "- Use the memory log of what’s already been tried or discovered\n"
#     "- Analyze why the step failed (error message and prior context)\n"
#     "- Decide if the direction needs to pivot to still answer the original question\n"
#     "- Regenerate new steps (starting from the failed one) to continue answering the question\n"
#     "- OR end early if it is not possible to proceed with the current data\n\n"

#     "You are allowed to:\n"
#     "Replace the failed step and all following steps with a better plan\n"
#     "Or return an empty list with a message if the question is unanswerable\n\n"

#     "Your goal is to help the user make progress — either by pivoting or clearly telling them what’s blocking the path forward."
# )
REPLAN_EXECUTION_SYSTEM = """You are a professional data scientist who has abundance of experience working with data across various business domains.
You are exceptionally proficient in breaking complex business problems into logical steps that can be executed in a code block. You are also very good at fixing the plan given the failed step result of the plan due to your years of experience.
You are very good at your job because you are detail-oriented and truly understand the problem at hand both technically and strategically.
"""
# REPLAN_EXECUTION_TEMPLATE = """
# User Question:
# {user_prompt}

# Schema Context:
# {schema_context}

# Memory Log (completed insights and blockers):
# {memory_log}

# Current Plan:
# {full_plan}

# Failed Step (#{current_step_index}):
# {failed_step_description}

# Error or Problem:
# {error_message}

# Variables available now:
# {required_variables}

# Instructions:
# - Replace the failed step and the remaining steps if needed.
# - You can pivot strategy if that helps.
# - You may return an empty list if the question is unanswerable with current data.

# Respond with a list of new steps (in valid JSON) or an empty list with reason:
# {format_instructions}
# """
REPLAN_EXECUTION_TEMPLATE = """Take a deep breath and think step-by-step. Think in gradually increasing complexity.

You are given the following:
- `<business_detail>`: A description of the business, its sector, goals, and challenges.
- `<schema_context>`: The internal data schema, including table structures and key fields.
- `<user_prompt>`: A high-level business task or analytical question to solve.
- `<memory_log>`: Execution log of all previous steps — what succeeded, what failed, and why.
- `<full_plan>`: The original step-by-step plan with all planned operations and variables.
- `<error_step_id>`: The ID of the step where an error occurred.
- `<error_msg>`: The actual error message.
- `<variable_env>`: A dictionary of all available variables in memory for use.

---

### 🧠 Your Task

Your goal is to repair or improve the current analysis pipeline after an error has occurred. To do this:

---

### ✅ Step 1: Understand the Business Context

**What to do:**
- Carefully read `<business_detail>` to understand the business nature, domain, and objectives.
- Understand what success or failure looks like from a business perspective.
- Map that to measurable metrics (e.g., increased sales, churn reduction, optimal inventory).

**Caution:**
- Do NOT make assumptions about the business goal — always anchor back to the user prompt and domain description.
- Avoid using domain knowledge that isn't hinted in the description unless it's a safe general assumption.

---

### ✅ Step 2: Analyze the Data Schema

**What to do:**
- Read `<schema_context>` and get a clear picture of available tables, their fields, and relationships.
- Match schema fields to variables required in the plan. Understand what data types are involved and how they support or limit analysis.

**Caution:**
- Be precise with assumptions: check if fields like `date`, `category`, `segment`, etc., are actually in the schema.
- Watch out for missing join keys or inconsistent formats.

---

### ✅ Step 3: Analyze the Full Plan

**What to do:**
- Go through `<full_plan>` step by step to understand what the original plan intended to achieve.
- Observe how each step builds on the previous one and what output it is supposed to generate.

**Caution:**
- Check for dependency chains — if a step relies on a variable that failed to compute earlier, it also needs revision.
- Avoid overhauling working steps unless necessary.

---

### ✅ Step 4: Investigate the Error

**What to do:**
- Look up `<error_step_id>` in the plan.
- Read `<error_msg>` carefully to understand whether the issue was caused by:
  - A logic flaw (e.g., division by zero, null values)
  - Data mismatch (e.g., expected list but got dict)
  - Missing variable
  - Invalid transformation

**Caution:**
- Avoid treating symptoms. Understand the **root cause** before deciding how to fix it.
- Don’t reintroduce failed logic or retry with the same broken assumptions.

---

### ✅ Step 5: Check What You Have Access To

**What to do:**
- Review `<variable_env>` to see which variables or dataframes are available in memory.
- Use only these to plan your next steps unless you're going to regenerate the missing ones.

**Caution:**
- Do not hallucinate variables or assume something exists unless it’s explicitly in `variable_env`.
- Double-check type compatibility and structure.

---

### ✅ Step 6: Adjust the Plan

**What to do:**
- Modify or regenerate the failed step and any dependent ones that follow.
- You can change the logic, rewrite the transformation, or pivot the analysis entirely if needed.
- Design each step in the plan with:
  - A clear purpose
  - Required inputs
  - Assumptions
  - Libraries
  - Expected outputs
- YOU MUST RETURN THE FULL PLAN FROM THE FIRST STEP. FOR EXAMPLE, IF A PLAN FAILS AT STEP 3 AND YOU ADJUSTED STEP 3 ONWARDS, YOU STILL HAVE TO RETURN THE PLAN FROM ORIGINAL STEP 1 to STEP 2 combined with YOUR ADJUSTED STEP 3 onwards.
- THE PREVIOUS INSTRUCTION IS REALLY IMPORTANT AS IT HELPS THE SYSTEM TO INDEX THE PLAN CORRECTLY. IF YOU DO THIS WELL, I WILL TIP YOU ADDITIONAL 50 US DOLLARS.

**Caution:**
- Make sure every output from one step is usable in the next.
- Avoid ambiguity. Be specific about shapes, columns, or expectations.
- If you conclude the plan cannot be completed due to schema or prompt limitations, **return an empty list** instead of a faulty plan.

---

### ✅ Final Output Format

You MUST respond in the following JSON format:

```json
{{
  "reasoning": "(str) Your overall thought process on what to do, what to be cautious of in the plan",
  "steps": [
    {{
      "step": "(str) Assigned ID of the step.",
      "description": "(str) Description of what this step does in detail. This helps the executor understand and translate into code accurately.",
      "goal": "(str) Describe what this step contributes to the overall analysis and what progress it would make toward the final answer.",
      "expected_outputs": ["(List[str]) Clearly state what output you expect from this step."],
      "assumptions": ["(List[str]) List assumptions such as required data shape, presence of certain fields, non-null conditions, distribution, etc."],
      "required_variables": ["(List[str]) List variables like dataframes, models, config params needed to run this step."],
      "required_libs": ["(List[str]) What libraries or tools must be imported to execute this step."],
      "outputs": ["(List[str]) The new variable names or artifacts this step will return."]
    }}
  ]
}}
```

---

### 🚫 Additional Guidelines

- ✅ Fix or refactor only what's broken — preserve what works.
- ✅ Assume your output will be used by another agent to code.
- ✅ Be explicit in your logic, avoid “magic thinking.”
- ❌ Don’t invent new data, columns, or libraries unless justified and safe.
- ❌ Don’t retry a broken step with the same assumptions or inputs.
- I EMPHASIZE AGAIN, YOUR PLAN SHOULD START FROM STEP 1 EVEN IF YOU ADJUSTED ONLY LATER STEPS ONWARDS!!!

If you do this task well, I will tip you 200 US Dollars.

<business_detail>
{business_detail}
</business_detail>

<schema_context>
{schema_context}
</schema_context>

<user_prompt>
{user_prompt}
</user_prompt>

<memory_log>
{memory_log}
</memory_log>

<full_plan>
{full_plan}
</full_plan>

<error_step_id>
{error_step_id}
</error_step_id>

<error_msg>
{error_msg}
</error_msg>

<variable_env>
{variable_env}
</variable_env>
"""

planner_replan_execution_prompt = ChatPromptTemplate.from_messages([
    ("system", REPLAN_EXECUTION_SYSTEM),
    ("user", REPLAN_EXECUTION_TEMPLATE)
])
