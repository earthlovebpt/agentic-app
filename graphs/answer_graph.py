from langgraph.graph import StateGraph, END
from graphs.state import AgentState

# 🧩 Import node functions (to be implemented or connected)
from nodes.planner import planner
from nodes.executor import executor_node
from nodes.reflect import reflect_on_results_node
from nodes.summary import summary_node

def build_answer_graph():
    builder = StateGraph(state_schema=AgentState)

    # ✅ Add all nodes
    builder.add_node("planner", planner)
    builder.add_node("executor", executor_node)
    builder.add_node("reflect_on_results", reflect_on_results_node)
    builder.add_node("summary", summary_node)

    # ✅ Set entry point
    builder.set_entry_point("planner")

    builder.add_edge("planner", "executor")

    builder.add_conditional_edges("executor", lambda state:
        "reflect_on_results" if (state.plan_successful or state.exceed_max_retries) else ("executor" if state.step_successful else "planner")
    )

    builder.add_conditional_edges("reflect_on_results", lambda state:
        "planner" if state.replan else "summary"
    )
    
    builder.add_edge("summary", END)

    return builder.compile()
