import plotly.express as px
import pandas as pd

df_seg = pd.DataFrame({
    'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025'],
    'Segment A (25-34)': [100, 110, 125, 140, 160],
    'Segment B (35-44)': [200, 205, 208, 210, 212]
})
fig_segment_growth = px.line(df_seg, x='Quarter', y=['Segment A (25-34)', 'Segment B (35-44)'], title="Customer Segment Growth (Index)", height=350)

RESPONSE = {
    "messages": [
        {"role": "BD_agent", "action": "ask_da", "content": "Requesting best-selling product from DA."},
        {"role": "DA_agent", "action": "answer", "content": "Response from DA: The best-selling product is Matcha."},
        {"role": "BD_agent", "action": "search_internet", "content": "Performing search for query: 'Trend Matcha recipes 2025'"},
        {"role": "BD_agent", "action": "process_search_result", "content": "Search Result Finding: Coffee matcha is trending in 2025."},
        {"role": "BD_agent", "action": "advise", "content": "Recommendation: Consider adding a Coffee Matcha menu item."},
    ],
    "insights": [
        {
            "bd_question": "Which customer segments show the highest potential for growth based on recent purchase frequency and average order value?",
            "insight": {
                "text": "Analysis indicates that customers aged 25-34 who purchase during weekday lunch hours exhibit the highest growth potential, suggesting targeted promotions or loyalty offers for this group could yield significant returns.",
                "visual": fig_segment_growth
            }
        },
        {
            "bd_question": "How does our online conversion rate compare to industry benchmarks for similar SMEs, and where are users dropping off most in the sales funnel?",
            "insight": {
                "text": "Our online conversion rate (1.5%) is below the industry benchmark (2.5%), with a significant drop-off observed at the payment gateway stage. Optimizing the checkout process could notably increase online revenue."
            }
        },
    ],
    "steps": [
        {
            "thought": "aaa",
            "code": "import numpy as np\nnp.mean(x_list)"
        },
        {
            "thought": "bbb",
            "code": "import numpy as np\nnp.mean(x_list)"
        }
        
    ]
}