from llm.prompts.search_prompt import search_prompt
from llm.llm_config import llm
from langchain_tavily import TavilySearch
from utils.scraper import postprocess_tavily

# Initialize Tavily Search Tool
tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

llm_bind_tools = llm.bind_tools([tavily_search_tool])

search_chain = search_prompt | llm_bind_tools | (lambda x: x.tool_calls[0]["args"]) | tavily_search_tool.invoke | postprocess_tavily