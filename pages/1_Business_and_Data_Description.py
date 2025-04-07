import streamlit as st
import pandas as pd

st.set_page_config(page_title="StratPilot - Business Setup", layout="wide")
st.title("StratPilot – Business & Data Setup")

# Init state
if "business_profile" not in st.session_state:
    st.session_state.business_profile = {"type": "", "details": ""}
if "datasets" not in st.session_state:
    st.session_state.datasets = {}

# Business info (editable)
st.header("1. Describe Your Business")
business_types = ["Cafe", "Bakery", "Retail", "Other"]
default_type = st.session_state.business_profile.get("type", "Cafe")
selected_index = business_types.index(default_type) if default_type in business_types else 0
st.session_state.business_profile["type"] = st.selectbox("Business type", business_types, index=selected_index)
st.session_state.business_profile["details"] = st.text_area(
    "Describe your business (products, goals, seasons, etc.)", 
    value=st.session_state.business_profile.get("details", "")
)

# Upload data
st.header("2. Upload and Describe Your Data")
uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file)
        dataset_label = file.name.split(".")[0]

        inferred = {col: col for col in df.columns}
        column_descriptions = {}
        for col, guess in inferred.items():
            column_descriptions[col] = f"This column likely represents {guess}."

        st.session_state.datasets[dataset_label] = {
            "data": df,
            "description": "",
            "column_descriptions": column_descriptions
        }

# Manage datasets
if st.session_state.datasets:
    st.subheader("📦 Manage Uploaded Datasets")
    to_delete = []
    for name, bundle in list(st.session_state.datasets.items()):
        with st.expander(f"📁 {name}"):
            st.dataframe(bundle["data"].head(), use_container_width=True)
            bundle["description"] = st.text_area(
                f"📝 What is this dataset? (e.g., Sales from Jan–Mar)", 
                value=bundle.get("description", ""), 
                key=f"{name}_description"
            )
            for col in bundle["data"].columns:
                bundle["column_descriptions"][col] = st.text_area(
                    f"Description for `{col}`", 
                    value=bundle["column_descriptions"].get(col, ""), 
                    key=f"{name}_{col}"
                )
            if st.button(f"🗑️ Delete `{name}`", key=f"delete_{name}"):
                to_delete.append(name)
    for name in to_delete:
        del st.session_state.datasets[name]
        st.success(f"Deleted dataset `{name}`")

# Save and proceed
if st.button("Save & Proceed to StratPilot"):
    st.success("Business information and schema saved.")
    st.switch_page("pages/2_StratPilot_AI_Assistant.py") 