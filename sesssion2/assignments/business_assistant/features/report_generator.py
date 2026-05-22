from ..tools.data_analyzer import analyze_data, data_analyzer_tool
from ..tools.calculator import calculate, calculator_tool

from .base import BaseFeature

REPORT_TYPES = {
    "sales": "Sales Report",
    "revenue": "Revenue Report",
    "performance": "Performance Report",
    "quarterly": "Quarterly Report",
}


class ReportGenerator(BaseFeature):
    """Feature 2: Creates professional business reports from data analysis."""


    def get_inputs(self) -> dict:
        """Collect all required inputs interactively from the user."""
        print("\n--- Business Report Generator ---")
        print("Available report types:")
        for i, (key, label) in enumerate(REPORT_TYPES.items(), 1):
            print(f"  {i}. {key.title()} — {label}")

        report_type = input("\nEnter report type (e.g. sales, revenue, performance, quarterly): ").strip()
        print('Enter your data as JSON or comma-separated values.')
        print('  e.g. {"Jan": 50000, "Feb": 65000, "Mar": 70000}')
        print('  or   50000, 65000, 70000')
        data = input("Data: ").strip()
        period = input("Enter time period (e.g. Q1 2026, Monthly, January 2026): ").strip()

        return {
            "report_type": report_type,
            "data": data,
            "period": period,
        }

    def run(self) -> str:
        """Collect inputs interactively, generate the report, and print it."""
        inputs = self.get_inputs()
        result = self.generate(**inputs)
        print("\n--- Generated Report ---\n")
        print(result)
        return result

    def generate(self, report_type: str, data: str, period: str) -> str:
        """
        Generate a professional business report.

        Args:
            report_type: Category of report (sales, revenue, performance, quarterly).
            data:        Raw data as a JSON string or comma-separated values.
            period:      Time period the report covers (e.g. Q1 2026).

        Returns:
            Formatted report with title, executive summary, key metrics,
            analysis, and recommendations.
        """
        system_prompt = """
        You are an expert business analyst who writes professional reports.

        When given data and a report type, you must:
        1. Calculate key metrics (totals, averages, growth rates, best/worst periods) using tools like calculate and analyze_data.
        2. Derive meaningful business insights from the numbers.
        3. Provide 3-5 concrete, actionable recommendations.

        Always respond in EXACTLY this format (keep the separator lines):

        ============================================
        [PERIOD] [REPORT TYPE TITLE]
        ============================================
        Date: [today's date or end of period]

        EXECUTIVE SUMMARY
        [2-3 sentences covering overall performance, total figures, and growth vs prior period]

        KEY METRICS
        [Bullet list with - prefix, one metric per line, formatted values with $ or % as appropriate]

        ANALYSIS
        [1-2 paragraphs of detailed analysis covering trends, patterns, and notable observations]

        RECOMMENDATIONS
        [Numbered list of 3-5 actionable recommendations]
        ============================================

        If a metric cannot be calculated from the data provided, omit it.
        """

        user_prompt = """
        Report type: {report_type}
        Time period: {period}
        Data: {data}
        """.format(report_type=report_type, period=period, data=data)

        return self._complete(
            system_prompt,
            user_prompt,
            functions={"calculate": calculate, "analyze_data": analyze_data},
            tools=[data_analyzer_tool, calculator_tool],
        )

    # ------------------------------------------------------------------
    # Convenience wrappers for each report type
    # ------------------------------------------------------------------

    def generate_sales_report(self, data: str, period: str) -> str:
        """Generate a sales report."""
        return self.generate("sales", data, period)

    def generate_revenue_report(self, data: str, period: str) -> str:
        """Generate a revenue report."""
        return self.generate("revenue", data, period)

    def generate_performance_report(self, data: str, period: str) -> str:
        """Generate a performance report."""
        return self.generate("performance", data, period)

    def generate_quarterly_report(self, data: str, period: str) -> str:
        """Generate a quarterly report."""
        return self.generate("quarterly", data, period)
