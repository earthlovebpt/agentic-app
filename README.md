# 🌼 DAISY

**DAISY (Data + Strategy)** is your smart agentic assistant that helps small businesses turn raw data into clear, actionable strategies — all without needing a full-time analyst.

## 🚧 Problems

> “Small business owners have data but not decisions.”

- 📊 Sales reports, spreadsheets, and dashboards are everywhere  
- ❓ But they don’t answer real business questions like:  
    - What should I promote?  
    - Where should I grow?  
    - What should I cut?  
- 💸 Hiring analysts is expensive  
- 🧩 DIY tools are overwhelming  
- ⛔ Insights often get stuck — never becoming action

## 🔍 How It Works

- 🧾 **User provides**:
  - Business data (CSV files)
  - Business profile or description

- 🤖 **DAISY processes the input**:
  - Understands the data schema
  - Suggests relevant business questions

- 💬 **User interacts**:
  - Reviews suggested questions
  - Asks additional custom questions

- 🧠 **Business Dev Agent handles**:
  - Interpreting questions
  - Calling Data Analyst Agent
  - Searching and summarizing relevant context (via tools like Tavily)
  - Generating strategy-focused answers

- 📊 **Data Analyst Agent executes**:
  - Python code for data analysis
  - Summarizes insights from the data

- ✅ **Output delivered**:
  - Actionable answers
  - Strategic recommendations

![Workflow Diagram](images/workflow.png)

## ✨ Features

- When the DAISY application is started, the main page will look like this

![Main Page](images/main_page.png)

- Next, to let DAISY understand your data, click the Business and Data Setup page and describe your business alongside uploading your csv files.

![SetUp Page](images/data_setup.png)

- The column description can be adjusted to better describe the data and allow DAISY for more accurate understanding

![Column Description](images/column_description.png)

- Click `Save & Proceed to Daisy`. DAISY will automatically explored the datasets and suggest question to the user.

![Save and Proceed](images/question_input.png)

- After the question is processed, DAISY will redirect to `Result` page. The first tab will show the final answer to the question alongside grounded strategies the owner can do to improve the business

![Result](images/result.png)
![Strat](images/strat.png)

- The `data insights` tab show both the insights extracted by DA agent from queries posed by BD agent and the insights extracted from search results. This is for transparency reason for user to check whether the answer is grounded on the insights

![Data Insights](images/data_insights.png)

- Lastly, the `Debug` shows the code run by the DA agent when extracting insights from internal data and its thought process on generating the code

![Debug](images/debug.png)

## 🚀 Getting Started

1. 🧬 Clone this repository  
```bash
git clone https://github.com/earthlovebpt/agentic-app.git
```

2. 🛠️ Set up the environment  
```bash
conda create --name daisy python=3.11 &&
conda activate daisy &&
pip install -r requirements.txt &&
playwright install
```

3. 🖥️ Launch the app  
```bash
streamlit run main.py
```

4. 🎉 Enjoy exploring your data with DAISY!

## 👥 Contributors

- Norrawee Charnpinyo (Email: *TBD*)  
- Pirat Pothavorn (Email: pirat.pot@gmail.com)  
- Supphaset Engphaiboon (Email: supphaset555@gmail.com)  