"""
Unit tests for all business_assistant features and request routing.

Run from the sesssion2/ directory:
    python -m pytest assignments/business_assistant/tests/ -v

Run a single class:
    python -m pytest assignments/business_assistant/tests/test_features.py::TestSmartEmailWriter -v
"""
import os
import unittest
from unittest.mock import MagicMock, patch, call

# Provide a fake key so config.py loads cleanly without a real .env file.
os.environ.setdefault("OPENAI_API_KEY", "sk-test-key-for-unit-tests")

from assignments.business_assistant.features.smart_email_writer import SmartEmailWriter
from assignments.business_assistant.features.report_generator import ReportGenerator
from assignments.business_assistant.features.meeting_summarizer import MeetingSummarizer
from assignments.business_assistant.features.data_analyzer import DataAnalyzer
from assignments.business_assistant.features.client_communication_drafter import ClientCommunicationDrafter
from assignments.business_assistant.business_assistant import BusinessAssistant

# ---------------------------------------------------------------------------
# Reusable fake AI responses
# ---------------------------------------------------------------------------
FAKE_EMAIL = (
    "Subject: Product Launch Update\n\n"
    "Dear Team,\n\nExciting news to share this quarter.\n\nBest regards,\nSarah"
)
FAKE_REPORT = (
    "============================================\n"
    "Q1 2026 SALES REPORT\n"
    "============================================\n"
    "Total Revenue: $187,000"
)
FAKE_SUMMARY = (
    "===========================================\n"
    "MEETING SUMMARY\n"
    "===========================================\n"
    "Date: May 15, 2026"
)
FAKE_ANALYSIS = (
    "ANALYSIS RESULTS\n"
    "==================\n"
    "Total Revenue: $240,000\nMonthly Average: $80,000"
)
FAKE_COMMUNICATION = (
    "Dear Acme Corp,\n\nWe are pleased to present our proposal.\n\n"
    "Best regards,\n[Your Name]"
)

MEETING_NOTES = (
    "Discussed Q1 results. Revenue up 15%. "
    "Sarah to prepare investor deck. James to upgrade CRM. "
    "Next meeting: June 1."
)


# ===========================================================================
# Feature Tests
# ===========================================================================

class TestSmartEmailWriter(unittest.TestCase):

    def setUp(self):
        self.writer = SmartEmailWriter()

    # --- Return value ---
    def test_write_returns_complete_result(self):
        with patch.object(self.writer, '_complete', return_value=FAKE_EMAIL):
            result = self.writer.write("announce product launch", "team", "professional")
        self.assertEqual(result, FAKE_EMAIL)

    # --- Prompt content ---
    def test_write_prompt_contains_purpose(self):
        with patch.object(self.writer, '_complete', return_value=FAKE_EMAIL) as mock_c:
            self.writer.write("quarterly review", "stakeholder", "formal")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("quarterly review", user_prompt)

    def test_write_prompt_contains_recipient(self):
        with patch.object(self.writer, '_complete', return_value=FAKE_EMAIL) as mock_c:
            self.writer.write("budget update", "client", "formal")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("client", user_prompt)

    def test_write_prompt_contains_tone(self):
        with patch.object(self.writer, '_complete', return_value=FAKE_EMAIL) as mock_c:
            self.writer.write("check-in", "team", "friendly")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("friendly", user_prompt)

    # --- Research topic ---
    def test_write_with_research_topic_included_in_prompt(self):
        with patch.object(self.writer, '_complete', return_value=FAKE_EMAIL) as mock_c:
            self.writer.write("market update", "client", "professional", research_topic="AI trends 2026")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("AI trends 2026", user_prompt)

    def test_write_without_research_topic_omits_research_hint(self):
        with patch.object(self.writer, '_complete', return_value=FAKE_EMAIL) as mock_c:
            self.writer.write("check-in", "team", "friendly", research_topic=None)
        _, user_prompt = mock_c.call_args[0]
        self.assertNotIn("Research this topic", user_prompt)

    # --- _complete called exactly once ---
    def test_write_calls_complete_once(self):
        with patch.object(self.writer, '_complete', return_value=FAKE_EMAIL) as mock_c:
            self.writer.write("test", "team", "professional")
        mock_c.assert_called_once()


class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ReportGenerator()

    def test_generate_returns_complete_result(self):
        with patch.object(self.generator, '_complete', return_value=FAKE_REPORT):
            result = self.generator.generate("sales", "Jan:50000,Feb:65000,Mar:70000", "Q1 2026")
        self.assertEqual(result, FAKE_REPORT)

    def test_generate_prompt_contains_report_type(self):
        with patch.object(self.generator, '_complete', return_value=FAKE_REPORT) as mock_c:
            self.generator.generate("performance", "85,90,88", "March 2026")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("performance", user_prompt)

    def test_generate_prompt_contains_period(self):
        with patch.object(self.generator, '_complete', return_value=FAKE_REPORT) as mock_c:
            self.generator.generate("revenue", "100000,120000", "Q2 2026")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("Q2 2026", user_prompt)

    def test_generate_prompt_contains_data(self):
        with patch.object(self.generator, '_complete', return_value=FAKE_REPORT) as mock_c:
            self.generator.generate("sales", "50000,65000,72000", "Q1 2026")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("50000,65000,72000", user_prompt)

    def test_sales_report_convenience_wrapper(self):
        with patch.object(self.generator, '_complete', return_value=FAKE_REPORT) as mock_c:
            result = self.generator.generate_sales_report("50000,65000", "Q1 2026")
        self.assertEqual(result, FAKE_REPORT)
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("sales", user_prompt)

    def test_revenue_report_convenience_wrapper(self):
        with patch.object(self.generator, '_complete', return_value=FAKE_REPORT) as mock_c:
            self.generator.generate_revenue_report("100000,110000", "H1 2026")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("revenue", user_prompt)

    def test_performance_report_convenience_wrapper(self):
        with patch.object(self.generator, '_complete', return_value=FAKE_REPORT) as mock_c:
            self.generator.generate_performance_report("85,90,92", "Q1 2026")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("performance", user_prompt)


class TestMeetingSummarizer(unittest.TestCase):

    def setUp(self):
        self.summarizer = MeetingSummarizer()

    def test_summarize_returns_complete_result(self):
        with patch.object(self.summarizer, '_complete', return_value=FAKE_SUMMARY):
            result = self.summarizer.summarize(MEETING_NOTES, "May 15, 2026")
        self.assertEqual(result, FAKE_SUMMARY)

    def test_summarize_prompt_contains_notes(self):
        with patch.object(self.summarizer, '_complete', return_value=FAKE_SUMMARY) as mock_c:
            self.summarizer.summarize(MEETING_NOTES, "May 15, 2026")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn(MEETING_NOTES, user_prompt)

    def test_summarize_prompt_contains_date(self):
        with patch.object(self.summarizer, '_complete', return_value=FAKE_SUMMARY) as mock_c:
            self.summarizer.summarize(MEETING_NOTES, "May 15, 2026")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("May 15, 2026", user_prompt)

    def test_summarize_with_attendees_included_in_prompt(self):
        with patch.object(self.summarizer, '_complete', return_value=FAKE_SUMMARY) as mock_c:
            self.summarizer.summarize(MEETING_NOTES, "May 15, 2026", attendees="Sarah, James, Maria")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("Sarah, James, Maria", user_prompt)

    def test_summarize_without_attendees_shows_not_specified(self):
        with patch.object(self.summarizer, '_complete', return_value=FAKE_SUMMARY) as mock_c:
            self.summarizer.summarize(MEETING_NOTES, "May 15, 2026", attendees=None)
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("Not specified", user_prompt)


class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DataAnalyzer()

    def test_analyze_returns_complete_result(self):
        with patch.object(self.analyzer, '_complete', return_value=FAKE_ANALYSIS):
            result = self.analyzer.analyze("sales", "Jan:50000,Feb:55000,Mar:62000", "average monthly revenue?")
        self.assertEqual(result, FAKE_ANALYSIS)

    def test_analyze_prompt_contains_query(self):
        with patch.object(self.analyzer, '_complete', return_value=FAKE_ANALYSIS) as mock_c:
            self.analyzer.analyze("sales", "50000,55000", "What is the growth rate?")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("What is the growth rate?", user_prompt)

    def test_analyze_prompt_contains_data(self):
        with patch.object(self.analyzer, '_complete', return_value=FAKE_ANALYSIS) as mock_c:
            self.analyzer.analyze("financial", "80000,90000,95000", "trend?")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("80000,90000,95000", user_prompt)

    def test_analyze_prompt_contains_data_type(self):
        with patch.object(self.analyzer, '_complete', return_value=FAKE_ANALYSIS) as mock_c:
            self.analyzer.analyze("time-series", "100,110,120", "trend?")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("time-series", user_prompt)

    def test_analyze_sales_wrapper(self):
        with patch.object(self.analyzer, '_complete', return_value=FAKE_ANALYSIS) as mock_c:
            result = self.analyzer.analyze_sales("50000,55000,60000", "average?")
        self.assertEqual(result, FAKE_ANALYSIS)
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("sales", user_prompt)

    def test_analyze_financial_wrapper(self):
        with patch.object(self.analyzer, '_complete', return_value=FAKE_ANALYSIS) as mock_c:
            self.analyzer.analyze_financial("costs: 30000,35000", "total costs?")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("financial", user_prompt)

    def test_analyze_performance_wrapper(self):
        with patch.object(self.analyzer, '_complete', return_value=FAKE_ANALYSIS) as mock_c:
            self.analyzer.analyze_performance("nps:72,churn:3", "are we healthy?")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("performance", user_prompt)

    def test_analyze_timeseries_wrapper(self):
        with patch.object(self.analyzer, '_complete', return_value=FAKE_ANALYSIS) as mock_c:
            self.analyzer.analyze_timeseries("2024:800000,2025:1000000", "YoY growth?")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("time-series", user_prompt)


class TestClientCommunicationDrafter(unittest.TestCase):

    def setUp(self):
        self.drafter = ClientCommunicationDrafter()

    def test_draft_returns_complete_result(self):
        with patch.object(self.drafter, '_complete', return_value=FAKE_COMMUNICATION):
            result = self.drafter.draft("project proposal", "Acme Corp", "CRM, $45k, 3 months", "professional")
        self.assertEqual(result, FAKE_COMMUNICATION)

    def test_draft_prompt_contains_client_name(self):
        with patch.object(self.drafter, '_complete', return_value=FAKE_COMMUNICATION) as mock_c:
            self.drafter.draft("status update", "TechCorp", "80% done", "professional")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("TechCorp", user_prompt)

    def test_draft_prompt_contains_context(self):
        with patch.object(self.drafter, '_complete', return_value=FAKE_COMMUNICATION) as mock_c:
            self.drafter.draft("follow-up message", "GlobalInc", "No response after 2 weeks", "friendly")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("No response after 2 weeks", user_prompt)

    def test_draft_project_proposal_wrapper(self):
        with patch.object(self.drafter, '_complete', return_value=FAKE_COMMUNICATION) as mock_c:
            result = self.drafter.draft_project_proposal("StartupXYZ", "Mobile app, 3 months, $80k")
        self.assertEqual(result, FAKE_COMMUNICATION)
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("project proposal", user_prompt)

    def test_draft_status_update_wrapper(self):
        with patch.object(self.drafter, '_complete', return_value=FAKE_COMMUNICATION) as mock_c:
            self.drafter.draft_status_update("RetailCo", "Phase 2 complete, on track")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("status update", user_prompt)

    def test_draft_inquiry_response_wrapper(self):
        with patch.object(self.drafter, '_complete', return_value=FAKE_COMMUNICATION) as mock_c:
            self.drafter.draft_inquiry_response("BlueSky", "Client asking about GDPR compliance")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("response to inquiry", user_prompt)

    def test_draft_followup_wrapper(self):
        with patch.object(self.drafter, '_complete', return_value=FAKE_COMMUNICATION) as mock_c:
            self.drafter.draft_followup("RetailCo", "No reply after 2 weeks")
        _, user_prompt = mock_c.call_args[0]
        self.assertIn("follow-up", user_prompt)


# ===========================================================================
# Routing Tests
# ===========================================================================

class TestBusinessAssistantRouting(unittest.TestCase):

    def setUp(self):
        self.assistant = BusinessAssistant()

    # --- Email routing ---
    def test_routes_write_email(self):
        with patch.object(self.assistant, 'write_email') as mock_email:
            self.assistant.process_request("write an email to my investors")
        mock_email.assert_called_once()

    def test_routes_draft_email(self):
        with patch.object(self.assistant, 'write_email') as mock_email:
            self.assistant.process_request("draft an email to the team")
        mock_email.assert_called_once()

    def test_routes_compose_email(self):
        with patch.object(self.assistant, 'write_email') as mock_email:
            self.assistant.process_request("compose a thank-you email for clients")
        mock_email.assert_called_once()

    def test_email_keyword_alone(self):
        with patch.object(self.assistant, 'write_email') as mock_email:
            self.assistant.process_request("I need to send an email")
        mock_email.assert_called_once()

    # --- Report routing ---
    def test_routes_generate_report(self):
        with patch.object(self.assistant, 'generate_report') as mock_report:
            self.assistant.process_request("generate a report for investors")
        mock_report.assert_called_once()

    def test_routes_create_report(self):
        with patch.object(self.assistant, 'generate_report') as mock_report:
            self.assistant.process_request("create report for Q1 2026")
        mock_report.assert_called_once()

    def test_routes_report_keyword_alone(self):
        with patch.object(self.assistant, 'generate_report') as mock_report:
            self.assistant.process_request("I need a sales report")
        mock_report.assert_called_once()

    # --- Meeting routing ---
    def test_routes_summarize_meeting(self):
        with patch.object(self.assistant, 'summarize_meeting') as mock_meeting:
            self.assistant.process_request("summarize last meeting")
        mock_meeting.assert_called_once()

    def test_routes_meeting_notes(self):
        with patch.object(self.assistant, 'summarize_meeting') as mock_meeting:
            self.assistant.process_request("I have meeting notes to process")
        mock_meeting.assert_called_once()

    def test_routes_action_items(self):
        with patch.object(self.assistant, 'summarize_meeting') as mock_meeting:
            self.assistant.process_request("extract action items from meeting")
        mock_meeting.assert_called_once()

    def test_routes_minutes_keyword(self):
        with patch.object(self.assistant, 'summarize_meeting') as mock_meeting:
            self.assistant.process_request("process the meeting minutes")
        mock_meeting.assert_called_once()

    # --- Data analysis routing ---
    def test_routes_analyze_data(self):
        with patch.object(self.assistant, 'analyze_business_data') as mock_data:
            self.assistant.process_request("analyze my sales data")
        mock_data.assert_called_once()

    def test_routes_financial_analysis(self):
        with patch.object(self.assistant, 'analyze_business_data') as mock_data:
            self.assistant.process_request("I need a financial data analysis")
        mock_data.assert_called_once()

    def test_routes_analysis_keyword(self):
        with patch.object(self.assistant, 'analyze_business_data') as mock_data:
            self.assistant.process_request("run an analysis on my data")
        mock_data.assert_called_once()

    # --- Client communication routing ---
    def test_routes_client_proposal(self):
        with patch.object(self.assistant, 'draft_client_communication') as mock_comm:
            self.assistant.process_request("draft a client proposal")
        mock_comm.assert_called_once()

    def test_routes_status_update(self):
        with patch.object(self.assistant, 'draft_client_communication') as mock_comm:
            self.assistant.process_request("send a status update to the client")
        mock_comm.assert_called_once()

    def test_routes_follow_up(self):
        with patch.object(self.assistant, 'draft_client_communication') as mock_comm:
            self.assistant.process_request("write a follow-up for a client")
        mock_comm.assert_called_once()

    # --- Quit / exit routing ---
    def test_quit_returns_false(self):
        result = self.assistant.process_request("quit")
        self.assertFalse(result)

    def test_exit_returns_false(self):
        result = self.assistant.process_request("exit")
        self.assertFalse(result)

    def test_bye_returns_false(self):
        result = self.assistant.process_request("bye")
        self.assertFalse(result)

    def test_goodbye_returns_false(self):
        result = self.assistant.process_request("goodbye")
        self.assertFalse(result)

    def test_stop_returns_false(self):
        result = self.assistant.process_request("stop")
        self.assertFalse(result)

    def test_quit_case_insensitive(self):
        result = self.assistant.process_request("QUIT")
        self.assertFalse(result)

    # --- Return value for normal requests ---
    def test_process_request_returns_true_for_email(self):
        with patch.object(self.assistant, 'write_email'):
            result = self.assistant.process_request("write an email")
        self.assertTrue(result)

    def test_process_request_returns_true_for_report(self):
        with patch.object(self.assistant, 'generate_report'):
            result = self.assistant.process_request("generate a report")
        self.assertTrue(result)

    def test_unknown_request_returns_true(self):
        # Unrecognised input should not crash and should return True (keep looping)
        result = self.assistant.process_request("what is the weather today?")
        self.assertTrue(result)

    def test_empty_string_after_strip_is_skipped_in_run(self):
        # run() skips blank input — verify process_request is not called for ""
        # We test by ensuring an empty stripped query falls through to unknown
        result = self.assistant.process_request("   ")
        self.assertTrue(result)  # returns True (not a quit command)


if __name__ == "__main__":
    unittest.main()
