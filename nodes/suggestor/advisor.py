from graphs.state import AgentState
from llm.chains.suggestor.advisor_chain import advisor_chain
import logging

logger = logging.getLogger("stratpilot")

def advisor_node(state: AgentState) -> AgentState:
    #Generated questions and their insights
    analysis = []
    for i, (q, ins) in enumerate(zip(state.gen_questions, state.insights)):
        tmp = f"Question {i+1}: {q.question}\nAligned with request {i+1}: {q.goal_alignment}"
        tmp += "\n" + "\n".join([f"Insight {i+1:02d} - {j+1:02d}: {ins[j]}" for j in range(len(ins))])
        analysis.append(tmp)

    analysis = "\n".join(analysis)

    inputs = {
        "business_detail": state.business_profile or {},
        "schema_context": state.schema_context,
        "original_request": state.og_prompt,
        "analysis": analysis,
    }
    
    logger.info("📤 [Advisor Node Input]\n%s", inputs)
    
    response = advisor_chain.invoke(inputs)
    
    logger.info("📥 [Advisor Node Output]\n%s", response)
    
    return state.model_copy(update={
        "strategies": response.strategies.model_dump()
    })
