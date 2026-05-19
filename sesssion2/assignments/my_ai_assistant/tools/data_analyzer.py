import json


def analyze_data(data_string, operation):
    data = json.loads(data_string)
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
