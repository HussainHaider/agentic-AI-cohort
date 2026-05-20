from .base import BaseFeature

DATA_TYPES = {
    "sales": "sales data (revenue, units sold)",
    "financial": "financial data (expenses, profit)",
    "performance": "performance metrics (conversion rates, KPIs)",
    "time-series": "time-series data (monthly, quarterly)",
}


class DataAnalyzer(BaseFeature):
    """Feature 4: Analyzes business data with natural language queries."""


    def get_inputs(self) -> dict:
        """Collect all required inputs interactively from the user."""
        print("\n--- Business Data Analyzer ---")
        print("Available data types:")
        for i, (key, desc) in enumerate(DATA_TYPES.items(), 1):
            print(f"  {i}. {key.title()} — {desc}")

        data_type = input("\nEnter data type (e.g. sales, financial, performance, time-series): ").strip()
        print("Enter your data as comma-separated values (e.g. 50000, 55000, 60000)")
        print("  or as label:value pairs (e.g. Jan:50000, Feb:55000, Mar:60000)")
        data = input("Data: ").strip()
        query = input("Enter your query (e.g. What is the average monthly revenue and growth rate?): ").strip()

        return {
            "data_type": data_type,
            "data": data,
            "query": query,
        }

    def run(self) -> str:
        """Collect inputs interactively, analyze the data, and print the result."""
        inputs = self.get_inputs()
        result = self.analyze(**inputs)
        print("\n--- Analysis Results ---\n")
        print(result)
        return result

    def analyze(self, data_type: str, data: str, query: str) -> str:
        """
        Analyze business data using a natural language query.

        Args:
            data_type: Category of data (sales, financial, performance, time-series).
            data:      Raw data as a comma-separated string of values or label:value pairs.
            query:     Natural language question about the data.

        Returns:
            Formatted analysis string with results, interpretation, and recommendations.
        """
        system_prompt = (
            "You are an expert business data analyst.\n\n"
            "When given data and a query, you must:\n"
            "1. Calculate relevant metrics (totals, averages, max, min, growth %, trends).\n"
            "2. Compare periods where applicable.\n\n"
            "Always respond in EXACTLY this format:\n\n"
            "ANALYSIS RESULTS\n"
            "==================\n"
            "[List every calculated metric, one per line, with clear labels and formatted values]\n\n"
            "INTERPRETATION\n"
            "[2-3 sentences explaining what the numbers mean in plain business language]\n\n"
            "RECOMMENDATION\n"
            "[1-2 actionable recommendations based on the analysis]"
        )

        user_prompt = (
            f"Data type: {data_type}\n"
            f"Data: {data}\n\n"
            f"Query: {query}"
        )

        return self._complete(system_prompt, user_prompt)

    # ------------------------------------------------------------------
    # Convenience wrappers for each supported data type
    # ------------------------------------------------------------------

    def analyze_sales(self, data: str, query: str) -> str:
        """Analyze sales data."""
        return self.analyze("sales", data, query)

    def analyze_financial(self, data: str, query: str) -> str:
        """Analyze financial data."""
        return self.analyze("financial", data, query)

    def analyze_performance(self, data: str, query: str) -> str:
        """Analyze performance metrics."""
        return self.analyze("performance", data, query)

    def analyze_timeseries(self, data: str, query: str) -> str:
        """Analyze time-series data."""
        return self.analyze("time-series", data, query)
