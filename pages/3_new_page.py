import streamlit as st
from graphs.understand_graph import build_understand_graph
from graphs.state import AgentState
import pandas as pd
from copy import deepcopy
from agents.sample import RESPONSE
from agents.da_agent.da_agent import DA_Agent
import pickle

# change tab css (font_size = 1rem as default)
TAB_CSS = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.3rem;
    }
</style>
'''
def bd_agent_run(quetion,schema_context,datasets):
    questions = ["Which products have the highest sales volume",
                 "What are the peak transaction times during the day",
                 "How do sales and customer visits vary across the different sales outlets"]
    da_results = []
    for question_ in questions:
        da_agent = DA_Agent()
        da_result = da_agent.user_sent_message(question_, schema_context, datasets)
        da_results.append({'question':question_,'response':da_result})
    result = {'da_result':da_results,'user_question':quetion}
    return result
    

def init_session_states():
    if "user_questions" not in st.session_state:
        st.session_state.user_questions = []
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "selected_index" not in st.session_state:
        st.session_state.selected_index = -1
        
def display_user_input():
    st.header("User questions")
    with st.form("question_form", clear_on_submit=True):
        user_question = st.text_input(
            label="Enter your business goal or question:",
            key="question_input"
        )
        submitted = st.form_submit_button("Submit Question")

        if submitted:
            if user_question and user_question.strip():
                st.session_state.user_questions.append(user_question.strip())
                with st.spinner("Generating response..."):
                    response = bd_agent_run(user_question.strip(),st.session_state.schema_context, st.session_state.datasets)
                    st.session_state.responses.append(response)
                    st.rerun()
            else:
                st.warning("Please enter a question before submitting.")
    st.divider()

def display_sidebar():
    """
    Display sidebar where the user can view output from selected questions.
    """
    
    st.sidebar.title("📜 History Selection")
    num_questions = len(st.session_state.user_questions)
    if num_questions == 0:
        st.sidebar.info("No history available.")
    else:
        display_labels = [f"Question: {q[:50]}" for q in st.session_state.user_questions]
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
    tab_chat, tab_insights, tab_steps = st.tabs(["💬 Chat History", "📊 Data Insights", "⚙️ Debug"])
    with tab_chat:
        display_chat_container()
    with tab_insights:
        display_insights()
    with tab_steps:
        display_steps()
    
def display_chat_container():
    """
    Display chat history of the user and the agents.
    """
    
    # chat_container = st.container()
    # with chat_container:
    #     num_questions = len(st.session_state.user_questions)
    #     if num_questions == 0:
    #         pass
    #     else:
    #         question = st.session_state.user_questions[st.session_state.selected_index]
    #         response = st.session_state.responses[st.session_state.selected_index]

    #         with st.chat_message("User"):
    #             st.markdown(f"{question}")
            
    #         # Display agent chats.
    #         for message in response["messages"]:
    #             with st.chat_message("Ai"):
    #                 st.markdown(format_message(message))


def display_insights():
    num_questions = len(st.session_state.user_questions)
    if num_questions == 0:
        pass
    else:
        response = st.session_state.responses[st.session_state.selected_index]
         # Display insights.
        for item in response["da_result"]:
            da_responses = item["response"]
            question = item["question"]
            with st.expander(f"❓ {question}"):
                final_result = da_responses["final_result"]
                key_insights = final_result["key_insights"]
                for key_insight in key_insights:
                    if 'insight' in key_insight:
                        st.write(key_insight['insight'])
                    if 'visualization' in key_insight:
                        for visualization in key_insight['visualization']:
                            with open(visualization['path'], 'rb') as file:
                                plotly_figure = pickle.load(file)
                            st.plotly_chart(plotly_figure, use_container_width=True)

        

def display_steps():
    pass
    # num_questions = len(st.session_state.user_questions)
    # if num_questions == 0:
    #     pass
    # else:
    #     response = st.session_state.responses[st.session_state.selected_index]
    #     for idx, item in enumerate(response["steps"]):
    #         with st.expander(f"Step {idx+1}"):
    #             if 'thought' in item:
    #                 st.markdown("### Thought Process")
    #                 st.markdown(item['thought'])
    #             if 'code' in item:
    #                 st.markdown("### Code")
    #                 st.code(item['code'], language="python")

    
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
    
def display_data_summary():
    """
    Display schema summaries and load datasets.
    """
    
    st.header("🧠 Data Schema Summary")
    all_dataframes = {}
    all_column_schemas = {}
    validation_errors = []

    for dataset_name, bundle in st.session_state.datasets.items():
        description = bundle.get("description", "").strip()
        df = bundle["data"]
        column_descriptions = bundle.get("column_descriptions", {})

        all_dataframes[dataset_name] = df
        all_column_schemas[dataset_name] = column_descriptions

        with st.expander(f"📁 {dataset_name} – {description or 'No description'}"):
            schema_df = pd.DataFrame(
                [{"Column": col, "Description": desc} for col, desc in column_descriptions.items()]
            )
            st.table(schema_df)

        # Validation checks
        if df.empty:
            validation_errors.append(f"Dataset `{dataset_name}` is empty.")
        if not description:
            validation_errors.append(f"Dataset `{dataset_name}` has no description.")
        if not column_descriptions or any(not desc.strip() for desc in column_descriptions.values()):
            validation_errors.append(f"Dataset `{dataset_name}` has incomplete column descriptions.")

    # Check for new datasets (i.e. those that haven’t been explored)
    new_datasets = {}
    have_new_datasets = False
    explored = set(st.session_state.get("explored_datasets", []))

    for name, bundle in st.session_state.datasets.items():
        if name not in explored:
            new_datasets[name] = bundle
            have_new_datasets = True

    if new_datasets:
        with st.spinner("🤖 Analyzing new datasets..."):
            profile = deepcopy(st.session_state.business_profile)
            datasets = deepcopy(st.session_state.datasets)

            state = AgentState(
                business_profile=profile,
                datasets=datasets,
                new_datasets=new_datasets,
                schema_context=st.session_state.get("schema_context", ""),
                explored_datasets=explored,
                memory_log=st.session_state.get("memory_log", [])
            )
            understand_graph = build_understand_graph()
            result = understand_graph.invoke(state)
            # Update session_state with new schema context and suggestions
            st.session_state.strategic_suggestions = result['suggested_questions']
            st.session_state.schema_context = result['schema_context']
            st.session_state.explored_datasets = result['explored_datasets']
            have_new_datasets = False

    if not have_new_datasets and "schema_context" in st.session_state:
        with st.expander("🧠 Auto-Explored Data Overview", expanded=False):
            st.markdown(st.session_state.schema_context)
    st.divider()

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
    init_session_states()
    display_business_profile()
    display_data_summary()
    display_suggested_questions()
    display_sidebar()
    display_user_input()
    display_output(tab_css=TAB_CSS)
    # debug()

if __name__ == "__main__":
    main()