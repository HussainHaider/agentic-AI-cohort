import json


def analyze_data(data_string, operation):
    try:
        data = json.loads(data_string)
    except json.JSONDecodeError:
        # Fallback: handle comma-separated values like "10, 20, 30, 40" (not valid JSON)
        data = [float(x.strip()) for x in data_string.strip("[]").split(",")]
    if operation == "sum":
        result = sum(data)
    elif operation == "average":
        result = sum(data) / len(data)
    elif operation == "max":
        result = max(data)
    elif operation == "min":
        result = min(data)
    else:
        result = None
    return json.dumps({"result": result})


data_analyzer_tool = {
    "type": "function",
    "function": {
        "name": "analyze_data",
        "description": "Analyze data",
        "parameters": {
            "type": "object",
            "properties": {
                "data_string": {"type": "string"},
                "operation": {
                    "type": "string",
                    "enum": ["sum", "average", "max", "min"],
                },
            },
            "required": ["data_string", "operation"],
        },
    },
}
