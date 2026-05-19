import json


def calculate(expression):
    try:
        return json.dumps({"result": eval(expression)})
    except:
        return json.dumps({"error": "Invalid expression"})


calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Do math",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"],
        },
    },
}
