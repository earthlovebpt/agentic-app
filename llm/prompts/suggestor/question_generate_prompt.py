from langchain.prompts import ChatPromptTemplate

QUESTION_GENERATE_SYSTEM = """
You are a business-savvy data scientist with strong domain understanding and critical thinking skills that can convert business problems into data-science questions that can be answered or validated with the business’s internal data.
"""

QUESTION_GENERATE_TEMPLATE = """
Take a deep breath and think step by step. 

You are given:
- A business request under the tag <business_goal>. This describes what the user wants to achieve, such as increasing sales, improving retention, or launching a new campaign.
- Metadata about the business under the tag <business_profile>. This can include type of business, key offerings, customer types, etc.
- THe business's internal data schema under the tag <schema_context>. This is a summary of the data schema and its contents.

Your task is to generate a thoughtful and strategic list of **data-oriented questions** that must be answered to help assess the feasibility, risk, and optimization of the business goal. These questions should help guide an analysis, spark relevant insights, and support better decision-making.
Furthermore, it should be **grounded** in and **answerable** with the business's internal data and the schema.

---

### Here’s how you should think step-by-step:

#### 1. Understand the Business Goal
- Read the goal carefully to understand what the user wants to achieve.
- Identify potential KPIs or metrics that indicate success or failure (e.g., revenue, sales volume, profit margin, conversion rate).

#### 2. Analyze the Internal Schema
- Think about the data the business likely has. Consider possible **tables** and **fields**:
  - Example tables: `sales`, `transactions`, `products`, `customers`, `promotions`, `inventory`, `time`
  - Example fields: `transaction_date`, `product_category`, `discount`, `customer_segment`, `purchase_quantity`
- Map the business goal to relevant parts of the schema. Your questions must be realistically answerable using this schema.

#### 3. Generate Insightful, Actionable Questions
- Ask questions that reveal:
  - Trends and seasonality
  - Segment behavior
  - Historical effectiveness
  - Thresholds or optimization points
  - Opportunities to use forecasting, clustering, or other modeling techniques
- Structure your thinking from **general to specific**. Start broad, then narrow in:
  - General: “Which product categories sell best on Mondays?”
  - Specific: “Among loyalty customers aged 18–25, which discounted products are frequently purchased together on Mondays?”

#### 4. Avoid Invalid or Subjective Questions
- ❌ Avoid speculative or opinion-based questions like:
  - “Will customers like this?”
  - “Would this strategy go viral?”
- ✅ Stick to data-answerable questions grounded in the internal schema.

---

### ✅ Output Format

```json
{{
  "thought": "(Your reasoning about the business goal and what schema or data fields you considered when forming the questions)",
  "questions": [
    {{
      "question": "(str) A clear, concise question answerable by data",
      "related_fields": ["(str)", "(str)", "..."],
      "goal_alignment": "(str) How this question helps with the business goal",
      "suggested_method": "(List[str]) e.g. clustering, forecasting, regression, data manipulation, market basket analysis. Keep it simple. DO NOT GO INTO DETAILS ON HOW IT SHOULD BE DONE!"
    }}
  ]
}}
```


---

### 📌 Example Considerations

If the goal is:  
**“I want to make a promotion on Monday to increase sales”**  
And your schema includes tables like:
- `sales(transaction_id, date, product_id, quantity, price)`
- `products(product_id, category, cost)`
- `customers(customer_id, age_group, segment)`
- `promotions(date, product_id, discount)`

Example output

```json
{{
  "thought": "The goal is to increase Monday sales through promotions. The schema suggests we can analyze past sales, promotions, product categories, and customer segments. I’ll ask questions to explore historical performance, segment-specific behavior, and promotion effectiveness, which could guide decision-making and validation with forecasting or clustering.",
  "questions": [
    {{
      "question": "Which product categories have the highest sales on Mondays?",
      "related_fields": ["sales.date", "products.category", "sales.quantity"],
      "goal_alignment": "Helps identify which products to focus promotion efforts on.",
      "suggested_method": ["data manipulation"]
    }},
    {{
      "question": "Which customer segments are most active on Mondays?",
      "related_fields": ["sales.date", "customers.segment", "sales.customer_id"],
      "goal_alignment": "Helps personalize promotions for high-activity segments.",
      "suggested_method": ["clustering"]
    }},
    {{
      "question": "What discount ranges on Mondays have historically increased total revenue?",
      "related_fields": ["promotions.discount", "sales.price", "sales.date"],
      "goal_alignment": "Helps find the sweet spot for discounting without harming margin.",
      "suggested_method": ["regression", "data manipulation"]
    }},
    {{
      "question": "Does bundling popular products with slow-movers improve Monday sales?",
      "related_fields": ["sales.product_id", "products.category", "sales.quantity"],
      "goal_alignment": "Explore cross-selling or inventory optimization.",
      "suggested_method": ["market basket analysis"]
    }}
  ]
}}```

<business_goal>
{business_goal}
</business_goal>

<business_profile>
{business_profile}
</business_profile>

<schema_context>
{schema_context}
</schema_context>
"""

question_generate_prompt = ChatPromptTemplate.from_messages([
    ("system", QUESTION_GENERATE_SYSTEM),
    ("user", QUESTION_GENERATE_TEMPLATE),
    ("assistant", "Thank you for your instructions. I will strictly adhere to your guidelines and provide a clear and concise response.")

])