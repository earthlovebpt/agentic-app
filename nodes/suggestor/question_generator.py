from graphs.state import AgentState
from llm.chains.suggestor.question_generate_chain import question_generate_chain
import logging

logger = logging.getLogger("stratpilot")

def question_generator_node(state: AgentState) -> AgentState:

    user_prompt = state.user_prompt or ""
    business_profile = state.business_profile or {}
    schema_context = state.schema_context or ""

    inputs = {
        "business_goal": user_prompt,
        "business_profile": business_profile,
        "schema_context": schema_context,
    }
    
    question_result = question_generate_chain.invoke(inputs)
    gen_questions = question_result.questions

    logger.info("[Question Generator Node Output]\n%s", [gq.question for gq in gen_questions])

    return state.model_copy(update={
        "gen_questions": gen_questions,
        "og_prompt": user_prompt
    })

