import streamlit as st
from agents.planner import plan_tasks
from agents.executor import execute_plan
from agents.reflector import reflect_on_results
from agents.advisor import generate_advice
from agents.explorer import explore_datasets_agentically
from agents.suggestion import get_strategic_question_suggestions
import pandas as pd
import re

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
    name = re.sub(r"\W", "", name)  # Remove all non-alphanumeric/underscore characters
    if re.match(r"^\d", name):
        name = f"df_{name}"  # Prefix if starts with a number
    return name

st.set_page_config(page_title="StratPilot - AI Assistant", layout="wide")
st.title("StratPilot – Your AI Business Consultant")

if "business_profile" not in st.session_state or not st.session_state.business_profile:
    st.warning("Please fill in your business and data details first.")
    st.stop()

# Display business profile
st.subheader("📋 Your Business Profile")
st.markdown(f"**Business Type:** {st.session_state.business_profile.get('type', '')}")
st.markdown(f"**Business Details:** {st.session_state.business_profile.get('details', '')}")

# Display schema summaries
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

    # Validation
    if df.empty:
        validation_errors.append(f"Dataset `{dataset_name}` is empty.")
    if not description:
        validation_errors.append(f"Dataset `{dataset_name}` has no description.")
    if not column_descriptions or any(not desc.strip() for desc in column_descriptions.values()):
        validation_errors.append(f"Dataset `{dataset_name}` has incomplete column descriptions.")



# 🔍 Generate Smart Strategic Question Suggestions after EDA
if "strategic_suggestions" not in st.session_state.business_profile:
    with st.spinner("🤖 Exploring your datasets..."):
        st.session_state.exploration_summary = explore_datasets_agentically(all_dataframes, all_column_schemas)
    with st.spinner("💡 Thinking of strategic questions you might ask..."):
        st.session_state.business_profile["strategic_suggestions"] = get_strategic_question_suggestions(
            st.session_state.business_profile
        )

# 💡 Display suggestions
suggestions = st.session_state.business_profile.get("strategic_suggestions", [])
if suggestions:
    st.subheader("💡 Smart Starter: Strategic Questions You Might Ask")
    for s in suggestions:
        st.markdown(f"- {s}")
    st.markdown("👉 *Use these as inspiration, or ask anything you'd like below.*")

# Prompt input
st.subheader("💬 Ask Your Business Question")
prompt = st.text_input("For example: What should I promote this weekend?")

if st.button("Analyze"):
    if validation_errors:
        st.error("❌ Please fix the following issues before proceeding:")
        for err in validation_errors:
            st.markdown(f"- {err}")
        st.stop()

    # Show the EDA summary in UI (optional but helpful)
    with st.expander("🧠 Auto-Explored Data Overview", expanded=False):
        st.markdown(st.session_state.exploration_summary)

    # Pass that as the schema_context to the planner
    st.session_state.business_profile["schema_context"] = st.session_state.exploration_summary

    # Now run the planner with EDA-aware context
    with st.spinner("🧠 Planning your analysis..."):
        plan = plan_tasks(prompt, st.session_state.business_profile)
        all_results = execute_plan(plan, all_dataframes, all_column_schemas,st.session_state.business_profile)
        reflection = reflect_on_results(prompt, all_results)

        if reflection["replan"]:
            st.info("🔁 Replanning based on reflection...")
            plan = plan_tasks(reflection["new_prompt"], st.session_state.business_profile)
            all_results = execute_plan(plan, all_dataframes, all_column_schemas,st.session_state.business_profile)

    advice = generate_advice(prompt, all_results, st.session_state.business_profile)
    st.subheader("📊 Analysis Results")
    for i, res in enumerate(all_results):
        step_desc = plan[i]["description"]
        with st.expander(f"🧠 Step {i + 1}: {step_desc}", expanded=True):

            if res.get("chart"):
                st.image(res["chart"])

            if res.get("show_insight") and res.get("insight_highlights"):
                st.success(res["insight_highlights"])

        if "code_explanation" in res and res["code_explanation"].strip():
            with st.expander(f"🧾 Show code explanation for Step {i}", expanded=False):
                st.markdown(res["code_explanation"])


    st.subheader("📈 Strategic Advice")
    st.markdown(advice)
