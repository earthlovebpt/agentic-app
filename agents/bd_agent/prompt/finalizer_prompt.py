from langchain.prompts import ChatPromptTemplate
from agents.llm_config import bd_llm

from pydantic import BaseModel
from typing import List

class Strategy(BaseModel):
    thought: str
    supported_insights: List[str]
    title: str
    description: str
    detailed_plans: List[str]
    advantages: List[str]
    disadvantages: List[str]

class FinalizerOutput(BaseModel):
    required_strategies: bool
    strategies: List[Strategy]
    answer_thought: str
    supported_insights: List[str]
    answer_to_question: str

FINALIZER_SYSTEM = """You are a professional business analyst who has abundance of experience working with data across various business domains.
You are very good at answering the user's request about their business and recommending strategy or actions the business can do to improve themselves. Your answer and recommended actions are always grounded to the insights you found in the data. That's why you are very high-regarded in your job
"""

FINALIZER_TEMPLATE = """Take a deep breath and think step-by-step. Gradually build your reasoning from basic understanding to a clear, confident answer.

You are given the following context:
- `<business_detail>`: Describes the type, scale, and goals of the business.
- `<schema_context>`: Outlines the internal data structure and available information.
- `<user_question>`: The specific question or request posed by the user.
- `<search_insights>`: Insights obtained from external web search related to the user’s question.
- `<data_insights>`: Insights obtained from analyzing the business’s internal data.

**IMPORTANT: YOU MUST GROUND YOUR ANSWER AND ADVICE ON BOTH `<data_insights>` AND `<search_insights>`.**

---

### 🎯 Objective

1. **Determine whether the user question requires strategy recommendations** to fully satisfy the request:
   - If the question asks only for a **direct factual answer** (e.g., "What is the best-selling product?"), you **do not need** to output strategies.
   - If the question is **open-ended** or **improvement-seeking** (e.g., "How can we improve sales next quarter?"), you **must** generate actionable strategies.
   - Use your best judgment. Err on the side of **providing strategies** if you are unsure.
2. **If strategies are required**, develop multiple **actionable and grounded** strategies based on the given insights.
3. **Regardless of whether strategies are required**, always **answer the user’s question** based on the internal and external insights.

---

### 🧭 Step-by-Step Instructions

1. **Understand the Business Context**  
   Carefully read the `<business_detail>` and `<schema_context>` to understand the type of business and the available data.

2. **Analyze the User's Question**  
   - Determine whether the user’s request is factual, strategic, or a mix of both.
   - Decide if strategies are needed (set `required_strategies` accordingly).

3. **Ground Yourself in the Insights**  
   - Review `<data_insights>` and `<search_insights>` carefully.
   - Identify which specific insights (by their IDs) will support your strategies and/or answers.

4. **If Strategies Are Required**  
   - Generate multiple (2–4) practical, realistic strategies.
   - Each strategy must:
     - Be clearly supported by specific insights.
     - Be really specific in the detailed plans. No more analyze in the plan since you are already given all the insights!
     - The detailed plan and plan description must be really specific and specify all names, values if possible. DO NOT BE VAGUE
     - Include detailed action plans, advantages, disadvantages

5. **Answer the User’s Question**  
   - Provide a direct and precise answer, grounded in the supporting insights.
   - If both answer and strategies are required, answer first, then propose strategies.
   - DO this in MARKDOWN FORMAT ONLY!!!

6. **Final Checks Before Output**  
   - Ensure every claim or recommendation you make is backed by specific insight IDs.
   - Keep the tone professional, practical, and action-driven.

---

### ✅ Output Format (MANDATORY)

```json
{{
  "required_strategies": "(bool) Whether this question requires you to output strategies or not",
  "strategies": [
    {{
      "thought": "(str) Why this strategy helps — explicitly identify which insights (by ID) support and validate this strategy",
      "supported_insights": [
        "(str) List of Insight IDs from <search_insights> and <data_insights> that validate this strategy"
      ],
      "title": "(str) Short and clear title for the strategy",
      "description": "(str) Detailed explanation of the strategy. BE REALLY THOROUGH KEEPING ALL NAME AND VALUE. DO NOT BE VAGUE",
      "detailed_plans": [
        "(str) Step-by-step action plan: specify team responsibilities and timelines. No more analysis should be needed since you come up with this based on all available insights"
      ],
      "advantages": [
        "(str) Key benefits of implementing this strategy"
      ],
      "disadvantages": [
        "(str) Risks, downsides, or costs associated with this strategy"
      ],
    }}.. (If not required_strategies, this should be an empty list)
  ],
  "answer_thought": "(str) Your understanding of insights and question alongside an outline of how to answer the user question",
  "supported_insights": [
    "(str) List of Insight IDs from <search_insights> and <data_insights> that validate this answer"
  ],
  "answer_to_question": "(str) Short and clear answer to the user question IN MARKDOWN FORMAT ONLY!!!"
}}```

If you do this task well, I will tip you 200 US Dollars.

<business_detail>
{business_detail}
</business_detail>

<schema_context>
{schema_context}
</schema_context>

<user_question>
{user_question}
</user_question>

<search_insights>
{search_insights}
</search_insights>

<data_insights>
{data_insights}
</data_insights>
"""

finalizer_prompt = ChatPromptTemplate.from_messages([
    ("system", FINALIZER_SYSTEM),
    ("user", FINALIZER_TEMPLATE)
])

finalizer_chain = finalizer_prompt | bd_llm.with_structured_output(FinalizerOutput)