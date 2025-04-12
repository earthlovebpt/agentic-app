from langgraph.graph import StateGraph, END
from graphs.state import AgentState

# 🧩 Import node functions (to be implemented or connected)
from nodes.validate_data import validate_data_node
from nodes.planner import planner
from nodes.executor import executor_node
from nodes.step_reflect import step_reflect_node
from nodes.reflect import reflect_on_results_node
from nodes.summary import summary_node

def build_answer_graph():
    builder = StateGraph(state_schema=AgentState)

    # ✅ Add all nodes
    builder.add_node("validate_data", validate_data_node)
    builder.add_node("planner", planner)
    builder.add_node("executor", executor_node)
    builder.add_node("step_reflect", step_reflect_node)
    builder.add_node("planner_retry", planner)
    builder.add_node("reflect_on_results", reflect_on_results_node)
    builder.add_node("summary", summary_node)

    # ✅ Set entry point
    builder.set_entry_point("validate_data")

    builder.add_conditional_edges("validate_data", lambda state:
        "planner" if state.data_sufficient else END
    )

    builder.add_edge("planner", "executor")
    builder.add_edge("executor", "step_reflect")

    builder.add_conditional_edges("step_reflect", lambda state:
        ("reflect_on_results" if state.plan_successful else "executor" ) if state.step_successful else (
            "plan_retry" if state.replan_step else "reflect_on_results"
        )
    )


    builder.add_edge("planner_retry", "executor")

    builder.add_conditional_edges("reflect_on_results", lambda state:
        "plan_retry" if state.replan else "summary"
    )
    
    builder.add_edge("summary", END)

    return builder.compile()
