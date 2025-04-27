import streamlit as st
from graphs.understand_graph import build_understand_graph
from graphs.state import AgentState
import pandas as pd
from copy import deepcopy
from agents.bd_agent.bd_agent import run_bd_agent
import pickle

# change tab css (font_size = 1rem as default)
TAB_CSS = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.3rem;
    }
</style>
'''

def init_state():
    if "user_questions" not in st.session_state:
        st.session_state.user_questions = []
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "selected_index" not in st.session_state:
        st.session_state.selected_index = -1


def display_sidebar():
    """
    Display sidebar where the user can view output from selected questions.
    """
    
    st.sidebar.title("📜 History Selection")
    num_questions = len(st.session_state.user_questions)
    if num_questions == 0:
        st.sidebar.info("No history available.")
    else:
        display_labels = [f"Question: {q}" for q in st.session_state.user_questions]
        selected_label = st.sidebar.selectbox(
            "Select Index to View:",
            options=display_labels,
            index=num_questions-1,
            key="sidebar_index_selector"
        )
        st.session_state.selected_index = display_labels.index(selected_label)

def display_output(tab_css: str):
    """
    Display the output from agents.
    """
    
    # change the css of tabs.
    st.markdown(tab_css, unsafe_allow_html=True) 
    tab_result, tab_insights, tab_steps = st.tabs(["💬 Result", "📊 Data Insights", "⚙️ Debug"])
    with tab_result:
        display_agent_result_answer()
    with tab_insights:
        display_insights()
    with tab_steps:
        display_steps()
    
def display_agent_result_answer():
    """
    BD agent result
    """
    num_questions = len(st.session_state.user_questions)
    if num_questions == 0:
        pass
    else:
        response = st.session_state.responses[st.session_state.selected_index]
        strategies = response.get("strategies", None)
        final_answer = response.get("final_answer", None)
        if final_answer:
            st.markdown("### 🎯 Final Answer")
            st.markdown(final_answer['answer_to_question'])
        if strategies:
            st.markdown("### 🎯 Strategies")
            for idx, strategy in enumerate(strategies):
                with st.expander(f"Strategy {idx+1}: {strategy['title']}", expanded=True):
                    st.markdown(f"### {strategy['title']}")
                    st.markdown(strategy['description'])
                    st.markdown("#### Detailed Plans")
                    for plan in strategy['detailed_plans']:
                        st.markdown(plan)
                    st.markdown("#### Advantages and Disadvantages")
                    max_len = max(len(strategy['advantages']), len(strategy['disadvantages']))
                    advantages = strategy['advantages'] + [''] * (max_len - len(strategy['advantages']))
                    disadvantages = strategy['disadvantages'] + [''] * (max_len - len(strategy['disadvantages']))
                    df = pd.DataFrame({"Advantages": advantages, "Disadvantages": disadvantages})
                    st.table(df)
                    st.markdown("#### Follow up Questions")
                    for followup in strategy['followup']:
                        st.markdown("- {followup}")

def display_insights():
    num_questions = len(st.session_state.user_questions)
    if num_questions == 0:
        pass
    else:
        response = st.session_state.responses[st.session_state.selected_index]
        data_insights = response.get("data_insights", None)
        search_insights = response.get("search_insights", None)
        if data_insights:
            st.write("## 📊 Data Insights")
            # Display insights.
            for i, item in enumerate(data_insights):
                final_result = item["final_result"]
                question = item["question"]
                with st.expander(f"❓ {question}",expanded=True):
                    key_insights = final_result["key_insights"]
                    for j ,key_insight in enumerate(key_insights):
                        if 'insight' in key_insight:
                            st.write(key_insight['insight'])
                        if 'visualization' in key_insight:
                            for k,visualization in enumerate(key_insight['visualization']):
                                with open(visualization['path'], 'rb') as file:
                                    plotly_figure = pickle.load(file)
                                st.plotly_chart(plotly_figure,key=f"{question}_{key_insight['insight']}_{i}_{j}_{k}", use_container_width=True)
        if search_insights:
            st.write("## 🔍 Search Insights",expanded=True)
            # Display insights.
            for item in search_insights:
                summaries = item["summaries"]
                question = item["question"]
                with st.expander(f"❓ {question}"):
                    for summary_item in summaries:
                        st.write(summary_item["summary"])
                        st.write(f'reference: {summary_item["url"]}')

        

def display_steps():
    num_questions = len(st.session_state.user_questions)
    if num_questions == 0:
        pass
    else:
        response = st.session_state.responses[st.session_state.selected_index]
        data_insights = response.get("data_insights", None)
        if data_insights:
            for item_insight in data_insights:
                intermediate_outputs = item_insight["intermediate_outputs"]
                question = item_insight["question"]
                for idx, item in enumerate(intermediate_outputs):
                    with st.expander(f"Question: {question}",expanded=True):
                        if 'thought' in item:
                            st.markdown("### Thought Process")
                            st.markdown(item['thought'])
                        if 'code' in item:
                            st.markdown("### Code")
                            st.code(item['code'], language="python")

    
def debug():
    st.write(st.session_state.selected_index)
    st.write(st.session_state.user_questions)
    st.write(st.session_state.responses)
    st.divider()

def display_business_profile():
    """
    Display business profile from the user inputs.
    """
    
    st.header("📋 Your Business Profile")
    if "business_profile" not in st.session_state or not st.session_state.business_profile:
        st.warning("Please fill in your business and data details first.")
        st.stop()
    st.markdown(f"**Business Type:** {st.session_state.business_profile.get('type', '')}")
    st.markdown(f"**Business Details:** {st.session_state.business_profile.get('details', '')}")
    st.divider()
    
def display_question():
    """
    Display schema summaries and load datasets.
    """
    st.markdown(f"### 🎯 Question \n #### {st.session_state.user_questions[st.session_state.selected_index]}")

def display_suggested_questions():
    """
    Display strategic suggestions (from understand phase).
    """
    
    if "strategic_suggestions" in st.session_state:
        st.header("💡 Smart Starter: Strategic Questions You Might Ask")
        for s in st.session_state.strategic_suggestions:
            st.markdown(f"- {s}")
    st.divider()


def format_message(message):
    return f":blue-background[{message['role']}: {message['action']}]\n\n{message['content']}"


def main():
    st.set_page_config(
        page_title="Agentic Workflow App (Refactored)",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    init_state()
    display_business_profile()
    display_question()
    display_sidebar()
    display_output(tab_css=TAB_CSS)
    # debug()

if __name__ == "__main__":
    main()