from graphs.state import AgentState
from llm.chains.suggestor.summary_chain import summary_chain
import logging

logger = logging.getLogger("stratpilot")

def summary_node(state: AgentState) -> AgentState:
    # Aggregate textual results from executor steps.
    summaries = "\n".join([res.get("summary", "") for res in state.results or []])
    
    # Build chart references by iterating through results.
    chart_refs = []
    for idx, res in enumerate(state.results or []):
        chart_path = res.get("chart")
        if chart_path:
            # Use index-based references (adjust as needed).
            chart_refs.append(f"Step {idx+1} - Chart Title:{res.get('chart_title')}: (Chart ID: {res.get('chart_id')}): {chart_path}")
    charts_info = "\n".join(chart_refs) if chart_refs else "No visual evidence available."
    
    inputs = {
        "business_type": state.business_profile.get("type", ""),
        "business_details": state.business_profile.get("details", ""),
        "schema_context": state.schema_context,
        "user_prompt": state.user_prompt,
        "results": summaries,
        "charts_info": charts_info,
        "prior_summary": state.prior_summary or "",
    }

    logger.info("charts_info: %s", charts_info)
    
    logger.info("📤 [Summary Node Input]\n%s", inputs)
    
    response = summary_chain.invoke(inputs)
    
    logger.info("📥 [Summary Node Output]\n%s", response)
    
    return state.model_copy(update={
        "answer_to_question": response.answer_to_question,
        "insight_summary": response.insight_summary,
        "recommended_actions": response.recommended_actions
    })
