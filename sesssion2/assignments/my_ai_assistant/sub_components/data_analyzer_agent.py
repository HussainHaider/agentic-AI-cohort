import json

from ...config import client, DEFAULT_MODEL
from ..tools.file_reader import file_reader, file_reader_tool
from ..tools.data_analyzer import analyze_data, data_analyzer_tool


class DataAnalyzer:
    """
    Data analyzer that reads a JSON file, extracts numeric fields,
    uses analyze_data tool for sum/average/max/min, then returns
    an LLM-formatted report string.
    """

    _FIELD_ALIASES = {
        "revenue":    "revenue",
        "sales":      "revenue",
        "income":     "revenue",
        "profit":     "profit",
        "earnings":   "profit",
        "units":      "units_sold",
        "units_sold": "units_sold",
        "sold":       "units_sold",
    }

    def __init__(self):
        self.tools = [file_reader_tool, data_analyzer_tool]
        self.functions = {
            "file_reader": file_reader,
            "analyze_data": analyze_data,
        }

    def _extract_numeric_field(self, text: str) -> str:
        """Return the numeric field name found in the text, defaulting to 'revenue'."""
        text_lower = text.lower()
        for keyword, field in self._FIELD_ALIASES.items():
            if keyword in text_lower:
                return field
        return "revenue"

    def analyze(self, file_path: str, numeric_field: str = "revenue") -> str:
        """Analyze data from a file and return a formatted report string."""
        print(f"\n📊 Analyzing data from '{file_path}' (field: {numeric_field})...\n")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a data analyst. Use the tools to: "
                    "1) read the file, 2) extract the numeric field values and run "
                    "sum, average, max, and min on them using analyze_data. "
                    "Then provide a clear, well-formatted report with insights."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Read '{file_path}', extract the '{numeric_field}' values, "
                    "and compute sum, average, max, and min. Then give me a formatted report."
                ),
            },
        ]

        while True:
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages,
                tools=self.tools,
            )

            response_message = response.choices[0].message
            messages.append(response_message)

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    print(f"🔧 Using {function_name}...")

                    result = self.functions[function_name](**function_args)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })
            else:
                report = response_message.content
                header = "\n" + "=" * 70 + "\n📈 DATA ANALYSIS REPORT\n" + "=" * 70
                return f"{header}\n{report}"
