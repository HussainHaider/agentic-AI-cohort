import json


def web_search(query):
    results = {
        "market trends": "Tech sector showing 15% growth in Q1 2026",
        "industry news": "AI adoption increasing across all sectors",
        "best practices": "Email best practices: personalization, clear CTAs",
        "competitor": "Main competitors expanding to new markets"
    }
    for keyword in results:
        if keyword in query.lower():
            return json.dumps({"results": results[keyword]})
    return json.dumps({"results": f"Info about {query}"})


web_search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search web",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"],
        },
    },
}
