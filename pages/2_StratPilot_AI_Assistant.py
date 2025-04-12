import streamlit as st
from graphs.answer_graph import build_answer_graph
from graphs.understand_graph import build_understand_graph  # if needed in later phases
from graphs.state import AgentState
import pandas as pd
import re
from copy import deepcopy

def sanitize(name):
    """
    Convert a string into a valid Python variable name:
    - Lowercase
    - Replace spaces and dashes with underscores
    - Remove invalid characters
    - Add prefix if name starts with a digit
    """
    name = name.lower().strip()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub(r"\W", "", name)
    if re.match(r"^\d", name):
        name = f"df_{name}"
    return name

# Configure Streamlit layout and title
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

    # Basic validation
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
        from copy import deepcopy
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
        # Save updated state into session_state
        st.session_state.strategic_suggestions = result['suggested_questions']
        st.session_state.schema_context = result['schema_context']
        st.session_state.explored_datasets = result['explored_datasets']
        have_new_datasets = False

if not have_new_datasets and ("schema_context" in st.session_state):
    with st.expander("🧠 Auto-Explored Data Overview", expanded=False):
        st.markdown(st.session_state.schema_context)

# Display strategic suggestions
if "strategic_suggestions" in st.session_state:
    st.subheader("💡 Smart Starter: Strategic Questions You Might Ask")
    for s in st.session_state.strategic_suggestions:
        st.markdown(f"- {s}")
    st.markdown("👉 *Use these as inspiration, or ask anything you'd like below.*")
    # Prompt input from the user for the answer phase
    st.subheader("💬 Ask Your Business Question")
    user_question = st.text_input("For example: What should I promote this weekend?")

# Validate before proceeding
if st.button("Analyze"):
    if validation_errors:
        st.error("❌ Please fix the following issues before proceeding:")
        for err in validation_errors:
            st.markdown(f"- {err}")
        st.stop()
    
    # Prepare the state for the answer graph
    from graphs.answer_graph import build_answer_graph
    from graphs.state import AgentState

    # Deepcopy to preserve session state
    profile = deepcopy(st.session_state.business_profile)
    datasets = deepcopy(st.session_state.datasets)
    schema_context = st.session_state.get("schema_context", "")

    # Initialize the AgentState for answer_graph with the user's question
    answer_state = AgentState(
        business_profile=profile,
        datasets=datasets,
        schema_context=schema_context,
        user_prompt=user_question,
        memory_log=st.session_state.get("memory_log", [])
    )

    # Build and run the answer graph
    answer_graph = build_answer_graph()
    final_state = answer_graph.invoke(answer_state)

    print(final_state)

    # # Display outputs from the answer graph
    # st.subheader("📌 Answer to Your Question")
    # st.markdown(final_state['answer_to_question'] or "No direct answer was generated.")

    # st.subheader("🔍 Key Insights")
    # st.markdown(final_state['insight_summary'] or "No insights available.")

    # st.subheader("✅ Recommended Actions")
    # if final_state.recommended_actions:
    #     for action in final_state['recommended_actions']:
    #         st.markdown(f"- {action}")
    # else:
    #     st.markdown("No recommendations provided.")

    # # If the retry limit was exceeded or the analysis failed
    # if hasattr(final_state, "retry_exceeded") and final_state.retry_exceeded:
    #     st.warning("⚠️ The assistant could not complete the analysis after multiple attempts.")
