import streamlit as st
from agents.understand_agent.understand_graph import build_understand_graph
from agents.understand_agent.graph.state import AgentState
import pandas as pd
import re
from copy import deepcopy
from agents.bd_agent.bd_agent import run_bd_agent

st.set_page_config(page_title="Daisy - AI Assistant", layout="wide")
st.title("Daisy – Your AI Business Consultant")

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
    st.switch_page("pages/3_Result.py") 


