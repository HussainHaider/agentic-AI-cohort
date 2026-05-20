def file_reader(file_path: str) -> str:
    """Read the contents of a file and return it as a string."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"
    
file_reader_tool = {
    "type": "function",
    "function": {
        "name": "file_reader",
        "description": "Read the contents of a file and return it as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read."
                }
            },
            "required": ["file_path"],
        },
    },
}

# print(file_reader('assignments/my_ai_assistant/sales.json')) # Should print the contents of sales.json or an error message if it fails.