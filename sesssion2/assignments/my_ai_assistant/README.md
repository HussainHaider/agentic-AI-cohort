# My AI Assistant

A multi-capability AI assistant powered by OpenAI's GPT models with function calling. It combines email writing, text summarization, data analysis, and tool-based reasoning into a single intelligent interface that automatically routes requests to the right capability.

## Capabilities

| Capability | Class / Tool | Description |
|---|---|---|
| Email Writing | `EnhancedEmailWriter` | Composes emails with web research support; supports `formal`, `friendly`, and `casual` tones |
| Text Summarization | `SmartSummarizer` | Summarizes text in `short`, `medium`, or `detailed` styles with word-count analytics |
| Data Analysis | `DataAnalyzer` | Reads JSON/CSV/TXT files and computes sum, average, max, and min on any numeric field |
| Calculator | `calculate()` | Evaluates math expressions |
| Web Search | `web_search()` | Topic-based web search for research |
| Data Stats | `analyze_data()` | Sum, average, max, min on inline numeric arrays |
| Time Converter | `time_converter()` | Converts times across timezones |
| Unit Converter | `unit_converter()` | Converts between units (length, weight, temperature, etc.) |
| File Reader | `file_reader()` | Reads and returns the contents of a file |
| Smart Routing | `MultiCapabilityAssistant` | Auto-detects intent and routes to the right capability |

## Project Structure

```
my_ai_assistant/
├── assistant.py              # MultiCapabilityAssistant — main entry point
├── sales.json                # Sample data file for testing DataAnalyzer
├── examples.txt              # Sample inputs and outputs
├── sub_components/           # Higher-level AI agents
│   ├── email_writer.py       # EnhancedEmailWriter
│   ├── summarizer.py         # SmartSummarizer
│   └── data_analyzer_agent.py  # DataAnalyzer
└── tools/                    # Low-level function-calling tools
    ├── calculator.py
    ├── web_search.py
    ├── data_analyzer.py
    ├── time_tools.py
    ├── unit_converter.py
    └── file_reader.py
```

## Installation

**1. Create and activate a virtual environment:**

```bash
python -m venv env
source env/bin/activate        # macOS / Linux
env\Scripts\activate           # Windows
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

Dependencies: `openai`, `python-dotenv`

**3. Set up your API key:**

Create a `.env` file in the `sesssion2/` directory:

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run directly from the `sesssion2` directory (required for relative imports):

```bash
cd sesssion2
python -m assignments.my_ai_assistant.assistant
```

Or import in your own script:

```python
from assignments.my_ai_assistant.assistant import MultiCapabilityAssistant
from assignments.my_ai_assistant.sub_components.email_writer import EnhancedEmailWriter
from assignments.my_ai_assistant.sub_components.summarizer import SmartSummarizer
from assignments.my_ai_assistant.sub_components.data_analyzer_agent import DataAnalyzer

# Auto-routing assistant
assistant = MultiCapabilityAssistant()
assistant.process("Calculate 25 * 4 + 10")
assistant.process("Write a friendly email to the marketing team about Q3 results")
assistant.process("Convert 100 meters to feet")
assistant.process("What is the current time in Tokyo?")

# Use sub-components directly
writer = EnhancedEmailWriter()
email = writer.write("Announce new AI features to team", tone="formal")

summarizer = SmartSummarizer()
report = summarizer.summarize("Your long text here...", style="medium")

analyzer = DataAnalyzer()
report = analyzer.analyze("assignments/my_ai_assistant/sales.json", numeric_field="revenue")
```

## Examples

**Email writing:**
```
📥 Request: Write a friendly email to Sarah updating her on the project
🎯 Using: EMAIL
📧 Writing email...  Tone: friendly

Subject: Project Update & Next Steps
Hi Sarah, ...
```

**Text summarization:**
```
📥 Request: Summarize the following text: AI is transforming...
🎯 Using: SUMMARIZE
📝 Summarizing (short style)...

======================================================================
📊 SUMMARY ANALYSIS
======================================================================
Original: 58 words, ~6 sentences
Summary:  22 words
Reduction: 62.1%
Style: Short
```

**Tools (calculator, time, units, file):**
```
📥 Request: Calculate what is 15% of 250?
🎯 Using: TOOLS
🔧 Using calculate...
💬 Response: 15% of 250 is 37.5.

📥 Request: Convert 100 meters to feet
🎯 Using: TOOLS
🔧 Using unit_converter...
💬 Response: 100 meters is equal to 328.084 feet.

📥 Request: What is the current time in Tokyo?
🎯 Using: TOOLS
🔧 Using time_converter...
💬 Response: The current time in Tokyo (JST) is 10:45 AM.
```