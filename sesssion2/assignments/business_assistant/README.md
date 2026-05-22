# Business Assistant

An AI-powered business assistant that routes natural language requests to the right feature automatically. Built with OpenAI's function-calling API.

---

## Real-World Scenario

Imagine: **Sarah runs a small tech company (NovaTech Solutions)**. She needs to:

1. Analyze last month's sales data
2. Generate a report for investors
3. Draft an email to stakeholders
4. Create action items from the last meeting

**Your assistant does ALL of this automatically!**

---

## Features

| # | Feature | Trigger keywords |
|---|---------|-----------------|
| 1 | **Smart Email Writer** | `email`, `draft an email`, `write an email`, `compose` |
| 2 | **Report Generator** | `report`, `generate report`, `create report`, `investor` |
| 3 | **Meeting Summarizer** | `meeting`, `summarize`, `action items`, `minutes`, `notes` |
| 4 | **Business Data Analyzer** | `analyze`, `analysis`, `data`, `sales data`, `financial data` |
| 5 | **Client Communication Drafter** | `client`, `draft`, `proposal`, `follow-up`, `status update` |

---

## Project Structure

```
business_assistant/
├── business_assistant.py       # Main class — routing loop + all features
├── features/
│   ├── base.py                 # Shared OpenAI client + _complete() helper
│   ├── smart_email_writer.py   # Feature 1: email writer
│   ├── report_generator.py     # Feature 2: report generator
│   ├── meeting_summarizer.py   # Feature 3: meeting summarizer
│   ├── data_analyzer.py        # Feature 4: data analyzer
│   └── client_communication_drafter.py  # Feature 5: client comms
├── tools/
│   ├── calculator.py           # Tool: arithmetic calculations
│   ├── web_search.py           # Tool: live web search
│   ├── data_analyzer.py        # Tool: raw data analysis helper
│   └── report_formatter.py     # Tool: report formatting helper
├── examples/
│   ├── email_examples.txt
│   ├── report_examples.txt
│   ├── meeting_examples.txt
│   ├── data_analysis_examples.txt
│   └── client_communication_examples.txt
└── tests/
    └── test_features.py        # 61 unit tests (no API calls needed)
```

---

## Setup

```bash
# 1. Activate your virtual environment
source env/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your OpenAI API key to a .env file
echo "OPENAI_API_KEY=sk-..." > .env
```

---

## Usage

### Run from the command line

From the `sesssion2/` directory:

```bash
python -m assignments.business_assistant.business_assistant
```

### Interactive loop (programmatic)

```python
from assignments.business_assistant.business_assistant import BusinessAssistant

assistant = BusinessAssistant()
assistant.run()
```

**Example session:**

```
Welcome to your Business Assistant!
I'm here to help you tackle your business tasks. Here's what I can do:

  1. Write / draft an email
  2. Generate a report (sales, revenue, performance, quarterly)
  3. Summarize a meeting and extract action items
  4. Analyze business data (sales, financial, performance)
  5. Draft client communications (proposals, follow-ups, etc.)

Type 'quit' at any time to exit.

How can I help you? > analyze last month's sales data
  ... (data analyzer runs) ...

Task complete! What would you like to do next?

How can I help you? > generate a report for investors
  ... (report generator runs) ...

Task complete! What would you like to do next?

How can I help you? > draft an email to stakeholders
  ... (email writer runs) ...

Task complete! What would you like to do next?

How can I help you? > summarize last meeting
  ... (meeting summarizer runs) ...

Task complete! What would you like to do next?

How can I help you? > quit
Goodbye! Have a productive day!
```

### Single request (programmatic)

```python
# Returns True to continue, False to quit
assistant.process_request("generate a sales report")
assistant.process_request("write an email to my client")
assistant.process_request("quit")  # → False
```

### Call features directly

```python
from assignments.business_assistant.features.smart_email_writer import SmartEmailWriter
from assignments.business_assistant.features.report_generator import ReportGenerator
from assignments.business_assistant.features.meeting_summarizer import MeetingSummarizer
from assignments.business_assistant.features.data_analyzer import DataAnalyzer
from assignments.business_assistant.features.client_communication_drafter import ClientCommunicationDrafter

# Email
writer = SmartEmailWriter()
email = writer.write(purpose="announce Q1 results", recipient="stakeholder", tone="professional")

# Report
generator = ReportGenerator()
report = generator.generate(report_type="sales", data="Jan:50000, Feb:65000, Mar:72000", period="Q1 2026")

# Meeting summary
summarizer = MeetingSummarizer()
summary = summarizer.summarize(notes="...", date="May 15, 2026", attendees="Sarah, James")

# Data analysis
analyzer = DataAnalyzer()
result = analyzer.analyze(data_type="sales", data="50000,65000,72000", query="average monthly revenue?")

# Client communication
drafter = ClientCommunicationDrafter()
comm = drafter.draft(comm_type="project proposal", client_name="Acme Corp", context="CRM, $45k, 3 months", tone="professional")
```

---

## Running Tests

Tests use `unittest.mock` — **no API key or network access required**.

```bash
# Run all tests from sesssion2/
python -m pytest assignments/business_assistant/tests/test_features.py -v
```

**61 tests across 6 classes:**

| Class | Tests | Covers |
|-------|-------|--------|
| `TestSmartEmailWriter` | 7 | return value, prompt content, research topic on/off |
| `TestReportGenerator` | 7 | return value, report type / period / data in prompt, wrappers |
| `TestMeetingSummarizer` | 5 | return value, notes / date in prompt, attendees on/off |
| `TestDataAnalyzer` | 8 | return value, query / data / type in prompt, all 4 wrappers |
| `TestClientCommunicationDrafter` | 7 | return value, client name / context in prompt, all 4 wrappers |
| `TestBusinessAssistantRouting` | 27 | all 5 routes, quit/exit/bye/stop/goodbye, case-insensitivity |

---

## Examples

See the `examples/` folder for realistic input/output samples for each feature, all based on the Sarah / NovaTech Solutions scenario.
