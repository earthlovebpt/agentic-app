from graphs.state import AgentState
import logging

logger = logging.getLogger("stratpilot")


integrate_method = lambda x: f"Using {' and/or '.join(x.suggested_method)} and emphasizing on these columns: {', '.join(x.related_fields)}, {x.question}"


def selector_node(state: AgentState) -> AgentState:

    #This node select and set the user_prompt
    curr_index = len(state.insights)
    state.current_step_index = 0

    logger.info("[Selector] Selecting Question {}".format(curr_index))
    logger.info("[Selector] Available Questions: {}".format([gq.question for gq in state.gen_questions]))
    curr_question = state.gen_questions[curr_index]
    curr_question = integrate_method(curr_question)
    logger.info("📤 [Selector Node Input]\n%s", curr_question)

    return state.model_copy(update={
        "user_prompt": curr_question
    })