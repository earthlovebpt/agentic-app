from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer

from typing import List, Dict

def scrape_urls(urls):
    loader = AsyncChromiumLoader(urls, user_agent="MyAppUserAgent")
    docs = loader.load()

    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    
    return docs_transformed

def postprocess_tavily(tavily_result: Dict) -> List[Dict]:
    """
    Take in the search result from Tavily search tools -> Scrape the content of the urls
    Remove those that got errors while scraping. Optionally filter out some domains

    Args:
        tavily_result (Dict): Tavily Search result

    Returns:
        List[Dict]: List of dictionary. Each representing one search result containing the url, page_content, and relevance score assigned by tavily
    """

    scraped = scrape_urls([r["url"] for r in tavily_result["results"]])

    processed_scraped = []
    for doc, r in zip(scraped, tavily_result["results"]):
        content = doc.page_content
        if "error" in content.lower():
            continue

        tmp = {"url": r["url"], "title": r["title"], "page_content": content, "relevance": r["score"]}
        processed_scraped.append(tmp)

    return processed_scraped