from .features.base import BaseFeature
from .tools.calculator import calculator_tool, calculate
from .tools.web_search import web_search_tool, web_search
from .tools.data_analyzer import data_analyzer_tool, analyze_data
from .tools.report_formatter import report_formatter_tool, format_report

from .features.client_communication_drafter import ClientCommunicationDrafter
from .features.data_analyzer import DataAnalyzer
from .features.meeting_summarizer import MeetingSummarizer
from .features.report_generator import ReportGenerator
from .features.smart_email_writer import SmartEmailWriter


class BusinessAssistant(BaseFeature):
    """Main business assistant class"""

    def __init__(self):
        super().__init__()
        # Initialize all tools
        self.tools = [calculator_tool, web_search_tool,
                      data_analyzer_tool, report_formatter_tool]

        self.functions = {
            "calculate": calculate,
            "web_search": web_search,
            "analyze_data": analyze_data,
            "format_report": format_report,
        }

        self.communication_drafter = ClientCommunicationDrafter()
        self.data_analyzer = DataAnalyzer()
        self.meeting_summarizer = MeetingSummarizer()
        self.report_generator = ReportGenerator()
        self.email_writer = SmartEmailWriter()

    def write_email(self):
        """Feature 1: Email writer"""
        return self.email_writer.run()

    def generate_report(self):
        """Feature 2: Report generator"""
        return self.report_generator.run()

    def summarize_meeting(self):
        """Feature 3: Meeting summarizer"""
        return self.meeting_summarizer.run()

    def analyze_business_data(self):
        """Feature 4: Data analyzer"""
        return self.data_analyzer.run()

    def draft_client_communication(self):
        """Feature 5: Client communication"""
        return self.communication_drafter.run()

    def process_request(self, request: str) -> bool:
        """Route a single request string to the appropriate feature.

        Returns False if the user wants to quit, True otherwise.
        """
        query = request.lower().strip()

        # Quit intent
        quit_keywords = {"quit", "exit", "bye", "goodbye", "stop", "q"}
        if any(word in query.split() for word in quit_keywords) or query in quit_keywords:
            print("\nGoodbye! Have a productive day!")
            return False

        # Email intent
        if any(kw in query for kw in ("email", "write an email", "draft an email", "compose")):
            self.write_email()

        # Report intent
        elif any(kw in query for kw in ("report", "investor", "generate report", "create report")):
            self.generate_report()

        # Meeting intent
        elif any(kw in query for kw in ("meeting", "summarize", "action item", "minutes", "notes")):
            self.summarize_meeting()

        # Data analysis intent
        elif any(kw in query for kw in ("analyze", "analysis", "data", "sales data", "financial data")):
            self.analyze_business_data()

        # Client communication intent
        elif any(kw in query for kw in ("client", "communication", "draft", "proposal", "follow-up", "status update")):
            self.draft_client_communication()

        else:
            result = self.general_assistant(request)
            print(f"\n{result}")

        return True

    def general_assistant(self, query):
        """General purpose assistant that uses available tools."""
        return self._complete(
            system_prompt="""You are a helpful business assistant.
            Use given tools to answer the user's query if possible.
            If the query is outside the scope of the tools, provide a helpful response based on your knowledge.""",
            user_prompt=query,
            functions=self.functions,
            tools=self.tools,
        )

    def _print_capabilities(self):
        """Print the list of supported features."""
        print("  1. Write / draft an email")
        print("  2. Generate a report (sales, revenue, performance, quarterly)")
        print("  3. Summarize a meeting and extract action items")
        print("  4. Analyze business data (sales, financial, performance)")
        print("  5. Draft client communications (proposals, follow-ups, etc.)")
        print("\nType 'quit' at any time to exit.")

    def run(self):
        """Start the interactive assistant loop."""
        print("\nWelcome to your Business Assistant!")
        print("I'm here to help you tackle your business tasks. Here's what I can do:\n")
        self._print_capabilities()

        while True:
            print()
            request = input("How can I help you? > ").strip()
            if not request:
                continue
            should_continue = self.process_request(request)
            if not should_continue:
                break
            print("\nTask complete! What would you like to do next?")


if __name__ == "__main__":
    assistant = BusinessAssistant()
    assistant.run()