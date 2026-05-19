# My AI Assistant

A multi-capability AI assistant powered by OpenAI's GPT-3.5-turbo with function calling. It combines email writing, text summarization, and tool-based reasoning into a single intelligent interface.

## What It Does

- **Enhanced Email Writer** — Composes professional emails with optional web research to include current information. Supports customizable tone (professional, casual, etc.).
- **Smart Text Summarizer** — Summarizes text in short, medium, or detailed styles with analytics (word count, sentence count, reduction percentage).
- **Chat with Conversation Memory** — Routes requests intelligently to the right capability using keyword-based intent detection.
- **Calculator** — Evaluates math expressions on the fly.
- **Web Search** — Simulated search tool for researching topics like AI trends, technology, and email tips.
- **Data Analyzer** — Performs sum, average, max, and min operations on numeric datasets.

## Installation

```bash
pip install -r requirements.txt
```

Dependencies:
- `openai`
- `python-dotenv`

Create a `.env` file in the project root with your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Since the project uses relative imports, run it as a module from the `sesssion2` directory:

```bash
cd sesssion2
python -m assignments.my_ai_assistant.assistant
```

Or import the classes in your own script:

```python
from assignments.my_ai_assistant.assistant import (
    EnhancedEmailWriter,
    SmartSummarizer,
    MultiCapabilityAssistant,
)

# Write an email
writer = EnhancedEmailWriter()
email = writer.write("Announce new AI features to team", tone="professional")

# Summarize text
summarizer = SmartSummarizer()
summarizer.summarize("Your long text here...", style="short")

# Use the multi-capability assistant (auto-routes requests)
assistant = MultiCapabilityAssistant()
assistant.process("Calculate 25 * 4 + 10")
assistant.process("Write an email to the marketing team about Q3 results")
```

## Examples

**1. Writing an email:**
```
📥 Request: Write an email announcing new AI features to the team
🎯 Using: EMAIL
📧 Writing email: Write an email announcing new AI features to the team
🔍 Researching: AI trends 2024

Subject: Exciting New AI Features Now Available!
Dear Team, ...
```

**2. Summarizing text:**
```
📝 Summarizing (short style)...

📊 SUMMARY ANALYSIS
Original: 52 words, ~6 sentences
Summary: 18 words
Reduction: 65.4%
Style: Short

SUMMARY
AI is transforming business through automation, data analysis, and NLP, with rapid adoption despite challenges in ethics and talent.
```

**3. Using the calculator:**
```
📥 Request: Calculate the average of 10, 20, 30, 40, 50
🎯 Using: TOOLS
Result: {"result": 30.0}
```

**4. Searching the web:**
```
📥 Request: Search for latest AI trends
🎯 Using: GENERAL
🔍 Researching: ai trends
Result: {"results": ["AI Trend 1: Large Language Models ...", ...]}
```

## Features

| Feature | Class | Description |
|---|---|---|
| Email Writing | `EnhancedEmailWriter` | Research-backed email composition with tone control |
| Summarization | `SmartSummarizer` | Multi-style summaries with word/sentence analytics |
| Smart Routing | `MultiCapabilityAssistant` | Auto-detects intent and routes to the right tool |
| Calculator | `calculate()` | Evaluates math expressions |
| Web Search | `web_search()` | Simulated topic-based search |
| Data Analysis | `analyze_data()` | Sum, average, max, min on numeric arrays |

### Planned Tools (Placeholders)

- File Reader
- Time Tools
- Unit Converter