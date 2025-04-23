from langgraph.graph import StateGraph, END
from graphs.state import AgentState

# 🧩 Import node functions (to be implemented or connected)
from nodes.suggestor.question_generator import question_generator_node
from nodes.suggestor.selector import selector_node
from nodes.suggestor.planner import planner
from nodes.suggestor.executor import executor_node
from nodes.suggestor.reflect import reflect_on_results_node
from nodes.suggestor.summary import summary_node
from nodes.suggestor.advisor import advisor_node
from nodes.validate_data import validate_data_node

#Question Generator -> Gen from user prompt + business profile + schema + generator, Set the og question, gen_question
#Selector  -> Select the user prompt based on length of insights
#Then -> Do planner -> executor loop -> until it reaches summary
#Summary -> extract insights -> append insight -> if len(insights) != num_question -> Loop back to selector -> Else -> Go to advisor
#Advisor would take business_profile, schema_context, insights, generated question, og_question -> Action (title, description, detailed plan, advantage, disadvantage, next question to ask)

def build_suggestor_graph():
    builder = StateGraph(state_schema=AgentState)

    # ✅ Add all nodes
    builder.add_node("question_generator", question_generator_node)
    builder.add_node("planner", planner)
    builder.add_node("executor", executor_node)
    builder.add_node("reflect_on_results", reflect_on_results_node)
    builder.add_node("summary", summary_node)
    builder.add_node("advisor", advisor_node)
    builder.add_node("selector", selector_node)
    builder.add_node("validate_data", validate_data_node)
    
    # ✅ Set entry point
    builder.set_entry_point("question_generator")
    
    #Add edge -> Question Generator -> Selector (Outer loop) -> 
    builder.add_edge("question_generator", "selector")
    builder.add_edge("selector", "validate_data")

    #Then, inner loop 
    builder.add_conditional_edges("validate_data", lambda state:
        "planner" if state.data_sufficient else END
    )

    builder.add_edge("planner", "executor")

    builder.add_conditional_edges("executor", lambda state:
        "reflect_on_results" if (state.plan_successful or state.exceed_max_retries) else ("executor" if state.step_successful else "planner")
    )

    builder.add_conditional_edges("reflect_on_results", lambda state:
        "planner" if state.replan else "summary"
    )
    
    builder.add_conditional_edges("summary", lambda state:
        "advisor" if state.complete_gen_question else "selector"
    )

    builder.add_edge("advisor", END)


    return builder.compile()
