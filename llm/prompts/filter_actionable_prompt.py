from langchain.prompts import ChatPromptTemplate

FILTER_ACTIONABLE_SYSTEM = """
You are a data scientist who is very good at comparing the business profile from the case study and your target business profile to determine if the case study is relevant to the target business. You are also very proficient in adapting actionables from relevant case study to be usable with your target business and improve it"""

FILTER_ACTIONABLE_TEMPLATE = """
Take a deep breath and think step by step. Think in gradually increasing complexity

You are given a business profile under the tag <business_profile>, the insight from business analysis under the tag <insight>
and the case study business profile under the tag <case_study_business_profile> and list of actionables and their effects of those case studies under the tag <actionables>.
Your task is to first check if the case study is relevant to the target business by comparing <business_profile> and <case_study_business_profile>. You are also provided with <schema_context> to provide you with the context of the schema to help you plan more **grounded** actionables
If the case study is relevant, you will then iterate through the list of provided <actionables> and try to adapt the actionables that are relevant to solving the problem or improve from the business insight.
For the adapted actionables, since you are a prolific data scientist, they must be grounded and are specific and clear enough to be implemented in a data scientist workflow such as validation and customer segmentation or that a data scientist could validate. 

Here's the detailed instruction of how to do the task.

### STEP 1: Understand the Target Business
- Read the `<business_profile>` carefully to understand the business’s nature, size, context, and goals.
- Then read the `<insight>` to identify key challenges, opportunities, or points of improvement uncovered through analysis.

Ask yourself:
> What kind of business is this? What does the insight tell me about its current situation or needs?

### STEP 2: Check Case Study Relevance
- Read the `<case_study_business_profile>` and compare it with the `<business_profile>`.
- The case study should be considered **relevant** if:
  - It is from a business of similar type or scale (e.g., a café vs. a coffee shop).
  - It addresses similar customer segments, services, or operational problems.
  - It tackles challenges or goals aligned with the target business’s insight.

If it is not relevant (e.g., different industry, completely different audience or goals), set `"relevant_case_study": false` and leave `"adapted_actionables"` as an empty list.

If it is relevant, proceed.

### STEP 3: Review and Filter the Actionables
- Iterate over the list under `<actionables>`.
- For each actionable, ask:
  - *Does this directly or indirectly help address the insight?*
  - *Can this strategy be reasonably implemented in the target business’s context?*

If yes, continue to adapt it.

### STEP 4: Adapt Each Relevant Actionable
For each chosen actionable, do the following:

- Write your **thought process** for selecting it. Include reasoning about how it fits the business profile and insight. State the index of the original actionables that you adapt from as well.
- Rephrase the **step** to suit the target business.
- Provide a list of **detailed implementation steps** that would be suitable for the target business. Be practical.
- State the **expected impact** — how this step could benefit the target business, especially in relation to the insight.
- YOU DON'T HAVE TO ADAPT EVERY ACTIONABLE. YOU MUST CHOOSE TO ADAPT ONLY A FEW THAT WILL ADDRESS THE INSIGHT PROVIDED ONLY!!!\
- Your adapted actionables should be **grounded** and **specific** and **clear enough** to be implemented in a data scientist workflow such as validation and customer segmentation or that a data scientist could validate.
  - For example, if your solution is to introduce **combo** promotion, you should explain what a data scientist need to do to find out what **combo** should work best from the data of the business


Your output MUST be in the following format:

```json
{{
  "thought": "(str) Your reasoning about relevance, including business type comparison and connection to the insight.",
  "relevant_case_study": "(bool) True if relevant, otherwise False",
  "adapted_actionables": [
    {{
      "thought": "(str) Why this step is applicable to the current business, linked to the insight.",
      "step": "(str) The adapted actionable step",
      "detailed_steps": [
        "(str) Step-by-step instruction #1",
        "(str) Step-by-step instruction #2",
        "(str) ..."
      ],
      "expected_impact": "(str) What effect this would likely have on the business, and how it addresses the insight)"
    }}
    ...
  ]
}}```
---

<business_profile>
{business_profile}
</business_profile>

<insight>
{insight}
</insight>

<case_study_business_profile>
{case_study_business_profile}
</case_study_business_profile>

<actionables>
{actionables}
</actionables>

<schema_context>
{schema_context}
</schema_context>
"""

filter_actionable_prompt = ChatPromptTemplate.from_messages([
    ("system", FILTER_ACTIONABLE_SYSTEM),
    ("user", FILTER_ACTIONABLE_TEMPLATE)
])