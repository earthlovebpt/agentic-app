from langchain.prompts import ChatPromptTemplate
from agents.llm_config import bd_llm

from pydantic import BaseModel
from typing import List, Optional, Dict

class Strategy(BaseModel):
    thought: str
    supported_insights: List[str]
    title: str
    description: str
    detailed_plans: List[str]
    advantages: List[str]
    disadvantages: List[str]
    followup: List[str]

class AdvisorOutput(BaseModel):
    strategies: List[Strategy]

ADVISOR_SYSTEM = """You are a professional business analyst who has abundance of experience working with data across various business domains.
You are very good at recommending strategy or actions the business can do to improve themselves. Your recommended actions are always grounded to the insights you found in the data. That's why you are very high-regarded in your job"""

ADVISOR_TEMPLATE = """Take a deep breath and think step-by-step. Think in gradually increasing complexity.

You are given a business profile and supporting analysis with the following tags:
- `<business_detail>`: Describes the business type and its operational context.
- `<schema_context>`: A schema representing the internal data structure of the business.
- `<user_question>`: The question or request posed by the user.
- `<search_insights>`: A list of insights generated from performing querying on search engine 
- `<data_insights>`: A list of insights generated from analysis on the business's internal data 
**YOU MUST GROUND YOUR ADVISE ON <data_insights> and <search_insights>**.

---

### 🎯 Objective

Develop **multiple actionable business improvement strategies** that are fully grounded in the insights provided. Your strategies must reflect a real understanding of the business context, available data, and user request.

---

### 🧭 Step-by-Step Instructions

#### ✅ Step 1: Understand the Business
- Read `<business_detail>` carefully:
  - Identify what type of business it is (e.g., restaurant, retail, service).
  - Understand its scale, environment, and priorities.

**Caution**:  
- ❌ Do not assume resources or capabilities beyond what’s described.
- ✅ Keep strategies realistic for the business profile.

---

#### ✅ Step 2: Understand the Data Schema
- Parse `<schema_context>`:
  - Identify the available data fields and relationships.
  - Know what can be measured, analyzed, or influenced.

**Caution**:  
- ❌ Don’t base strategies on data that isn't in the schema.
- ✅ Stay grounded in what’s actually available.

---

#### ✅ Step 3: Understand the User's Concern
- Read `<user_question>`:
  - Understand what improvement or outcome the user seeks.
  - Frame your strategies to answer this need directly.

**Caution**:  
- ❌ Avoid general advice. Stay tightly focused on the user’s goal.
- ✅ Ensure strategies are customized to the user's specific request.

---

#### ✅ Step 4: Analyze the Insights
- Carefully review `<search_insights>` and `<data_insights>`.
- Identify patterns, opportunities, problems, and advantages.
- Use the insights in detail: reference product names, numbers, sales data, times of day, etc.

**Caution**:  
- ❌ Never invent new insights. Stick only to what’s provided.
- ✅ Cross-reference multiple insights to strengthen your strategies.

---

#### ✅ Step 5: Generate Specific, Actionable Strategies
For each strategy:
- Clearly explain how it ties to the user’s goal and what insights support it.
- Provide a **step-by-step action plan**:
  - Specify what to do, who is responsible (e.g., marketing, sales, operations), and expected timeline.
- Be very **detailed**:
  - For example, recommend **specific products** for promotions, **specific loyalty program designs**, or **specific customer segments**.
- Discuss **pros and cons**.

**Caution**:  
- ❌ No high-level fluff like "improve customer service" without detailed action steps.
- ✅ Make it detailed enough that a manager could immediately assign work based on your plan.


---

### ✅ Output Format (MANDATORY)

```json
{{
  "strategies": [
    {{
      "thought": "(str) Why this strategy helps — explicitly identify which insights (by ID) support and validate this strategy",
      "supported_insights": [
        "(str) List of Insight IDs from <search_insights> and <data_insights> that validate this strategy"
      ],
      "title": "(str) Short and clear title for the strategy",
      "description": "(str) Detailed explanation of the strategy",
      "detailed_plans": [
        "(str) Step-by-step action plan: specify team responsibilities and timelines"
      ],
      "advantages": [
        "(str) Key benefits of implementing this strategy"
      ],
      "disadvantages": [
        "(str) Risks, downsides, or costs associated with this strategy"
      ],
      "followup": [
        "(str) Potential follow-up questions the user might ask"
      ]
    }}
  ]
}}

If you do this task well, I will tip you 200 US DOllars.

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

advisor_prompt = ChatPromptTemplate.from_messages([
    ("system", ADVISOR_SYSTEM),
    ("user", ADVISOR_TEMPLATE)
])

advisor_chain = advisor_prompt | bd_llm.with_structured_output(AdvisorOutput)

