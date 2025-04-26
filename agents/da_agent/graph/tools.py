from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from typing import Annotated, Tuple
from langgraph.prebuilt import InjectedState
import sys
from io import StringIO
import os
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import pandas as pd
import numpy as np
import sklearn
import pickle
import re
from typing import Annotated, Tuple, List, Dict, Optional
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from langchain_core.tools.base import InjectedToolCallId

persistent_vars = {}

@tool(parse_docstring=True)
def complete_python_task(
        graph_state: Annotated[dict, InjectedState], thought: str, python_code: str, tool_call_id: Annotated[str, InjectedToolCallId]
) -> Tuple[str, dict]:
    """Completes a python task

    Args:
        thought: Internal thought about the next action to be taken, and the reasoning behind it. This should be formatted in MARKDOWN and be high quality.
        python_code: Python code to be executed to perform analyses, create a new dataset or create a visualization.
    """
    current_variables = graph_state.get("current_variables", {})
    if not os.path.exists("images/plotly_figures/pickle"):
        os.makedirs("images/plotly_figures/pickle")

    try:
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Execute the code
        exec_globals = globals().copy()
        exec_globals.update(persistent_vars)
        exec_globals.update(current_variables)
        exec_globals.update(graph_state.get("datasets", {}))
        exec_globals["plotly_figures"] = {}

        exec(python_code, exec_globals)

        persistent_vars.update({k: v for k, v in exec_globals.items() if k not in globals()})

        # Get stdout
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        updated_state = {
            "intermediate_outputs": [{"thought": thought, "code": python_code, "output": output}],
            "current_variables": persistent_vars
        }

        # Save figures and paths
        if "plotly_figures" in exec_globals and isinstance(exec_globals["plotly_figures"], dict):
            image_records = []
            for name, fig in exec_globals["plotly_figures"].items():
                safe_name = re.sub(r"[^\w\-]+", "_", name.strip())  # make it filename-safe
                pickle_filename = f"images/plotly_figures/pickle/{safe_name}.pickle"
                with open(pickle_filename, "wb") as f:
                    pickle.dump(fig, f)
                image_records.append({
                    "name": name,
                    "path": pickle_filename
                })

            if image_records:
                updated_state["output_image_paths"] = image_records

            persistent_vars["plotly_figures"] = {}

        messages = [ToolMessage(output, tool_call_id=tool_call_id)]
        return Command(update={**updated_state, "messages": messages})

    except Exception as e:
        sys.stdout = old_stdout
        print(f"Exception: {e}")
        messages = [ToolMessage(str(e), tool_call_id=tool_call_id)]
        return Command(update={"messages": messages, "intermediate_outputs": [{"thought": thought, "code": python_code, "output": str(e)}]})

@tool(parse_docstring=True)
def save_final_result(
    graph_state: Annotated[dict, InjectedState],
    key_insights: List[dict],
    answers: str,
    blocker: Optional[str],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Tuple[str, dict]:
    """
    Saves the final structured result of the analysis.

    Args:
        key_insights: A list of dicts, each with: 'insight': str — the finding or conclusion. 'visualization' (optional): List[str] of plot names matching keys in plotly_figures.
        answers: A final answer strings derived from the analysis.
        blocker: An optional message describing any blocker encountered during analysis.
    """
    output_image_paths = graph_state.get("output_image_paths", [])
    # Map from plot name to stored path
    name_to_path = {entry["name"]: entry["path"] for entry in output_image_paths}

    # Resolve visualization names to their paths within each insight
    for insight_dict in key_insights:
        if "visualization" in insight_dict and insight_dict["visualization"]:
            resolved = []
            for name in insight_dict["visualization"]:
                if name not in name_to_path:
                    raise ValueError(f"Visualization '{name}' not found in saved output_image_paths.")
                resolved.append({"name": name, "path": name_to_path[name]})
            insight_dict["visualization"] = resolved

    # Build final result payload
    final_result = {
        "key_insights": key_insights,
        "answers": answers
    }
    if blocker:
        final_result["blocker"] = blocker

    # Update state and confirm
    return Command(update={
        "final_result": final_result,
        "messages": [
            ToolMessage("Final result saved.", tool_call_id=tool_call_id)
        ]
    })
