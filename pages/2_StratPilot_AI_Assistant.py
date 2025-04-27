import streamlit as st
from graphs.understand_graph import build_understand_graph
from graphs.state import AgentState
import pandas as pd
import re
from copy import deepcopy
from agents.bd_agent.bd_agent import run_bd_agent

def sanitize(name):
    """
    Convert a string into a valid Python variable name.
    """
    name = name.lower().strip()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub(r"\W", "", name)
    if re.match(r"^\d", name):
        name = f"df_{name}"
    return name

def normalize_text(text):
    normalized_text = text.replace("$","\$")
    return normalized_text

def display_answer_section(final_state):
    st.subheader("📌 Answer to Your Question")
    st.markdown(normalize_text(final_state['answer_to_question']) or "No direct answer was generated.")
    
def display_key_insights_section(final_state):
    st.subheader("🔍 Key Insights")
    st.markdown(normalize_text(final_state['insight_summary']) or "No insights were generated.")
        
def display_recommendations_section(final_state):
    st.subheader("✅ Recommended Actions")
    if final_state['recommended_actions']:
        for action in final_state['recommended_actions']:
            st.markdown(f"- {normalize_text(action)}")
    else:
        st.markdown("No specific recommendations provided.")
        
def display_analysis_section(final_state):
    # Only show charts that are referenced in the final summary texts
    combined_summary = (final_state['answer_to_question'] or "") + " " + (final_state['insight_summary'] or "")
    
    st.subheader("📊 Analysis Visualization")
    chart_found = False
    for i, res in enumerate(final_state['results']):
        # Expect that executor_node sets a chart_id in each result (e.g. "chart_1", "chart_2", etc.)
        chart_id = res.get("chart_id")
        # Only show the chart if the chart_id is mentioned in the final summary text
        if chart_id and chart_id in combined_summary:
            st.markdown(f'{res.get("chart_id")}: {res.get("chart_title")}')
            st.image(res.get("chart"), use_container_width=True, caption=f"Chart from Step {i+1} ({chart_id})")
            chart_found = True
    if not chart_found:
        st.info("No charts were referenced in the final summary.")
        
def display_results(final_state):
    with st.container(border=True):
        display_answer_section(final_state)
    with st.container(border=True):
        display_key_insights_section(final_state)
    with st.container(border=True):
        display_recommendations_section(final_state)
    with st.container(border=True):
        display_analysis_section(final_state)

st.set_page_config(page_title="StratPilot - AI Assistant", layout="wide")
st.title("StratPilot – Your AI Business Consultant")

# Check business profile
if "business_profile" not in st.session_state or not st.session_state.business_profile:
    st.warning("Please fill in your business and data details first.")
    st.stop()

# Display business profile
st.subheader("📋 Your Business Profile")
st.markdown(f"**Business Type:** {st.session_state.business_profile.get('type', '')}")
st.markdown(f"**Business Details:** {st.session_state.business_profile.get('details', '')}")

# Display schema summaries and load datasets
st.subheader("🧠 Data Schema Summary")
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

# Display strategic suggestions (from understand phase)
if "strategic_suggestions" in st.session_state:
    st.subheader("💡 Smart Starter: Strategic Questions You Might Ask")
    for s in st.session_state.strategic_suggestions:
        st.markdown(f"- {s}")

# Prompt input for the answer phase
st.subheader("💬 Ask Your Business Question")
user_question = st.text_input("👉 *Use these as inspiration, or ask anything you'd like below.*")

if st.button("Analyze"):
    if validation_errors:
        st.error("❌ Please fix the following issues before proceeding:")
        for err in validation_errors:
            st.markdown(f"- {err}")
        st.stop()

    if "user_questions" not in st.session_state:
        st.session_state.user_questions = []
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "selected_index" not in st.session_state:
        st.session_state.selected_index = -1
    # Prepare AgentState for the answer phase using updated session_state
    profile = deepcopy(st.session_state.business_profile)
    datasets = deepcopy(st.session_state.datasets)
    schema_context = st.session_state.get("schema_context", "")

    st.session_state.user_questions.append(user_question.strip())
    with st.spinner("Generating response..."):
        response = run_bd_agent(user_question.strip(),st.session_state.business_profile,st.session_state.schema_context, st.session_state.datasets)
        st.session_state.responses.append(response)
    st.switch_page("pages/3_new_page.py") 


