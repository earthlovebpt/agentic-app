from langgraph.graph import StateGraph, END
from graphs.state import AgentState
from nodes.explorer import explorer_node
from nodes.suggest_questions import suggest_questions_node

def build_understand_graph():
    builder = StateGraph(state_schema=AgentState) 

    builder.add_node("explorer", explorer_node)
    builder.add_node("suggest_questions", suggest_questions_node)

    builder.set_entry_point("explorer")
    builder.add_edge("explorer", "suggest_questions")
    builder.add_edge("suggest_questions", END)

    return builder.compile()