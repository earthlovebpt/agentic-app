from langchain_tavily import TavilySearch
from utils.scraper import postprocess_tavily

from agents.llm_config import bd_llm
from typing import List, Dict, Any
from agents.bd_agent.prompt.web_summary_prompt import web_summary_prompt, WebSummaryOutput
from langchain_core.tools import tool
from .state import BDState
from ..prompt.advisor_prompt import advisor_chain
from ..prompt.responder_prompt import responder_chain

from typing import Annotated, Tuple
from langgraph.prebuilt import InjectedState
from langchain_core.tools.base import InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage


from tqdm import tqdm
import logging

logger = logging.getLogger("stratpilot")

# Initialize Tavily Search Tool
tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

web_summary_chain = web_summary_prompt | bd_llm.with_structured_output(WebSummaryOutput)

def search_summary_single(query: str) -> List[str]:
    result = tavily_search_tool.invoke({"query": query})
    scraped = postprocess_tavily(result)

    summaries = []
    for s in scraped:
        tmp = web_summary_chain.invoke({
            "question": query,
            "web_title": s["title"],
            "web_content": s["page_content"]
        })

        summaries.append(tmp.summary)

    return summaries

@tool(parse_docstring=True)
def search_summary(graph_state: Annotated[dict, InjectedState], thought: str, queries: List[str], tool_call_id: Annotated[str, InjectedToolCallId], show_progress: bool = True) -> Tuple[str, dict]:
    """
    Search and summarize web content for a list of queries.

    Args:
        thought (str): Your thought on how each queries would help increase the information to fullfill user's request.
        queries (List[str]): A list of search queries.
        show_progress (bool, optional): Whether to show progress bar. Defaults to False.

    Returns:
        messages (str): Formatted message to be used as tool result
        search_insights List[Dict[str, Any]]: List of insights generated from the search and summary procedures
    """
    logger.info(f"[Search and Summary]: {graph_state['messages']}")
    if show_progress:
        queries = tqdm(queries)
        
    summaries = []
    for query in queries:
        summaries.append({
            "question": query,
            "summaries": search_summary_single(query)
        })

    messages = ""
    for summary in summaries:
        messages += f"Question: {summary['question']}\n"
        tmp = "\n  - ".join(summary["summaries"])
        messages += f"Summaries: {tmp}\n"

    messages = [ToolMessage(messages, tool_call_id=tool_call_id)]
    logger.info(f"[Search Result]: {summaries}")
    return Command(update={"search_insights": graph_state.get("search_insights", []) + summaries, "messages": messages})

#Util function to assign insight ID to both data insights and search insights
def repr_data_insight(data_insights: List[Dict[str, Any]]):
    return ""

def repr_search_insight(search_insights: List[Dict[str, Any]]):

    repr_insight = []
    for i, insights in enumerate(search_insights):
        repr_insight.append(f"[q{i:02d}] {insights['question']}")
        for j, insight in enumerate(insights["summaries"]):
            repr_insight.append(f"[q{i:02d}-insight{j:02d}]{insight}")

    return "\n".join(repr_insight)


@tool(parse_docstring=True)
def advise_from_insights(graph_state: Annotated[dict, InjectedState], user_request: str, thought: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> Dict[str, Any]:
    """
    From the gathered insights from business's internal data and the search results from website, generate a list of actionable strategies that might suit the user's request

    Args:
        thought: Your thought on why do you decide that the information is sufficient for generating actionable strategies
        user_request: The user request that the strategies will try to address

    Returns:
        messages (str): Formatted message to be used as tool result containing formatted strategy
        strategies (List[Dict[str, Any]]): List of strategies in its original data structure containing description, detailed plans, ...
    """
    logger.info(f"[Advise From Insights]: {graph_state['messages']}")
    search_insight_str = repr_search_insight(graph_state.get("search_insights", []))
    data_insight_str = repr_data_insight(graph_state.get("data_insights", []))

    inputs = {"business_detail": graph_state["business_profile"],
              "schema_context": graph_state["schema_context"],
              "user_question": user_request,
              "search_insights": search_insight_str,
              "data_insights": data_insight_str}
    
    result = advisor_chain.invoke(inputs)

    strategies = [s.model_dump() for s in result.strategies]

    messages = [ToolMessage(f"Generated Strategies: {str(strategies)}", tool_call_id=tool_call_id)]
    logger.info(f"[Advise From Insights]: {strategies}")
    return Command(update={"strategies": strategies, "messages": messages})

@tool(parse_docstring=True)
def answer_from_insights(graph_state: Annotated[dict, InjectedState], user_request: str, thought: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> Dict[str, Any]:
    """
    From the gathered insights from business's internal data and the search results from website, answer the user's question in a grounded way

    Args:
        thought: Your thought on why do you decide that the information is sufficient for answering the user
        user_request: The user request that the answer will try to address

    Returns:
        messages (str): Formatted message to be used as tool result containing formatted answer
        final_answer (str): Final Answer
    """
    logger.info(f"[Answer From Insights]: {graph_state['messages']}")
    search_insight_str = repr_search_insight(graph_state.get("search_insights", []))
    data_insight_str = repr_data_insight(graph_state.get("data_insights", []))

    inputs = {"business_detail": graph_state["business_profile"],
              "schema_context": graph_state["schema_context"],
              "user_question": user_request,
              "search_insights": search_insight_str,
              "data_insights": data_insight_str}
    
    result = responder_chain.invoke(inputs)

    final_answer = result.answer_to_question

    messages = [ToolMessage(f"Final Answer: {final_answer}", tool_call_id=tool_call_id)]
    logger.info(f"[Answer From Insights]: {final_answer}")
    return Command(update={"final_answer": final_answer, "messages": messages})
    