from graphs.state import AgentState
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def summarize_column(col, series: pd.Series, user_desc: str) -> str:
    dtype = str(series.dtype)
    nulls = series.isnull().sum()
    n_unique = series.nunique()
    samples = series.dropna().unique()[:3]

    stats = [f"• Description: {user_desc or 'No description provided.'}"]
    stats.append(f"• Type: {dtype}")
    stats.append(f"• Nulls: {nulls}")
    stats.append(f"• Unique: {n_unique}")

    # Add min/max for datetime and numeric
    if pd.api.types.is_numeric_dtype(series):
        stats.append(f"• Min: {series.min():.2f}, Max: {series.max():.2f}")
    elif pd.api.types.is_datetime64_any_dtype(series):
        stats.append(f"• Range: {series.min().date()} → {series.max().date()}")

    stats.append(f"• Sample: {samples.tolist()}")
    return f"- `{col}`\n  " + "\n  ".join(stats)

def summarize_dataset(name, df: pd.DataFrame, table_desc: str, col_descs: dict) -> str:
    lines = [f"📁 `{name}` — {table_desc or 'No table description provided.'}"]
    for col in df.columns:
        desc = col_descs.get(col, "")
        lines.append(summarize_column(col, df[col], desc))
    return "\n".join(lines)

def explorer_node(state: AgentState) -> AgentState:
    new_datasets = state.new_datasets or {}
    explored = set(state.explored_datasets or [])

    schema_context = state.schema_context or ""
    schema_blocks = []

    updated_datasets = {**(state.datasets or {}), **new_datasets}

    for name, bundle in new_datasets.items():
        if name in explored:
            continue

        try:
            df = bundle["data"]
            table_desc = bundle.get("description", "")
            col_descs = bundle.get("column_descriptions", {})

            summary = summarize_dataset(name, df, table_desc, col_descs)
            schema_blocks.append(summary)
            explored.add(name)

        except Exception as e:
            logger.warning(f"[explorer_node] Failed to process `{name}`: {e}")

    return state.model_copy(update={
        "schema_context": (schema_context + "\n\n" + "\n\n".join(schema_blocks)).strip(),
        "datasets": updated_datasets,
        "new_datasets": {},
        "explored_datasets": list(explored),
    })
