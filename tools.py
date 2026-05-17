"""
CONCEPT: Tools are just Python functions you expose to Claude.
Claude reads the name + description to decide WHEN to call them.
Claude reads the input_schema to know WHAT arguments to pass.
You never call these functions yourself -- Claude decides when.
"""

import os
from tavily import TavilyClient

# --- Tool definitions (what Claude sees) ---
# This is the "menu" you hand to Claude. It describes capabilities, not implementations.

TOOLS = [
    {
        "name": "search_news",
        "description": (
            "Search the web for recent news articles on a given topic. "
            "Use this to find today's news about legal tech, AI in law, "
            "Kosovo/Albania updates, padel, or any topic requested."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query, e.g. 'legal tech AI 2026' or 'padel world rankings'"
                },
                "max_results": {
                    "type": "integer",
                    "description": "How many results to return. Default 5, max 10.",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
]


# --- Tool implementations (what actually runs) ---
# These are called by YOUR code, not by Claude directly.

def search_news(query: str, max_results: int = 5) -> list[dict]:
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    response = client.search(
        query=query,
        max_results=max_results,
        search_depth="basic",
        include_answer=False,
        days=1  # only return results from the last 24 hours
    )

    # Return only what's useful -- title, url, and a short snippet
    return [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", "")[:300]
        }
        for r in response.get("results", [])
    ]


def run_tool(tool_name: str, tool_input: dict):
    """
    CONCEPT: This is your tool dispatcher.
    Claude returns a tool_use block with a name + inputs.
    You match the name and call the right function.
    As you add more tools, you add more branches here.
    """
    if tool_name == "search_news":
        return search_news(**tool_input)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
