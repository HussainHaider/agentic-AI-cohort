import json


def web_search(query):
    results = {
        "ai trends": "Latest AI: Advanced reasoning, multimodal models",
        "technology": "Tech news: AI adoption accelerating",
        "email tips": "Email tips: Clear subject, concise content",
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
