from langchain_tavily import TavilySearch
from utils.scraper import postprocess_tavily

from agents.llm_config import bd_llm
from typing import List, Dict, Any
from agents.bd_agent.prompt.web_summary_prompt import web_summary_prompt, WebSummaryOutput
from langchain_core.tools import tool


from tqdm import tqdm

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
            "question": args["query"],
            "web_title": s["title"],
            "web_content": s["page_content"]
        })

        summaries.append(tmp.summary)

    return summaries

@tool(parse_docstring=True)
def search_summary(queries: List[str], show_progress: bool = False) -> List[Dict[str, Any]]:
    """
    Search and summarize web content for a list of queries.

    Args:
        queries (List[str]): A list of search queries.
        show_progress (bool, optional): Whether to show progress bar. Defaults to False.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing web content summaries for each query. The keys include 'question' (The search query), 'summaries' (List of summaries)
    """

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
        messages += f"Summaries: {"\n   - ".join(summary['summaries'])}\n"

    return {"messages": messages, "search_insights": summaries}