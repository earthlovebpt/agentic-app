from graphs.state import AgentState
from llm.chains.summary_chain import summary_chain
import logging

logger = logging.getLogger(__name__)

def summary_node(state: AgentState) -> AgentState:
    if state.retry_exceeded:
        logger.warning("⚠️ Max retry attempts exceeded. Generating fallback summary.")

        return state.model_copy(update={
            "answer_to_question": "The assistant attempted to analyze your question but encountered limitations in the available data or encountered repeated execution errors.",
            "insight_summary": "Despite multiple attempts, the system could not complete the required analysis steps due to either missing context or incompatible data.",
            "recommended_actions": [
                "Try rephrasing your question to be more specific or focused.",
                "Review your datasets to ensure they include the necessary columns and structure.",
                "Consider uploading additional data that supports the question you're asking."
            ]
        })

    # ✅ Otherwise, proceed normally
    summaries = "\n".join([r.get("summary", "") for r in state.results or []])
    highlights = "\n".join([r.get("insight_highlights", "") for r in state.results or []])

    inputs = {
        "user_prompt": state.user_prompt,
        "business_type": state.business_profile.get("type", ""),
        "business_details": state.business_profile.get("details", ""),
        "schema_context": state.business_profile.get("schema_context", ""),
        "results": summaries,
        "insight_highlights": highlights,
        "prior_summary": state.prior_summary or "",
    }

    logger.info("📤 [Summary Node Input]\n%s", inputs)
    response = summary_chain.invoke(inputs)
    logger.info("📥 [Summary Output]\n%s", response)

    return state.model_copy(update={
        "answer_to_question": response.answer_to_question,
        "insight_summary": response.insight_summary,
        "recommended_actions": response.recommended_actions
    })
