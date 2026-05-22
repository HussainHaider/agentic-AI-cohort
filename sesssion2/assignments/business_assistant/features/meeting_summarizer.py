from .base import BaseFeature


class MeetingSummarizer(BaseFeature):
    """Feature 3: Converts meeting notes into structured summaries with action items."""


    def get_inputs(self) -> dict:
        """Collect all required inputs interactively from the user."""
        print("\n--- Meeting Summarizer ---")
        print("Enter your meeting notes below.")
        print("When done, type 'END' on a new line and press Enter.")

        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        notes = "\n".join(lines).strip()

        date = input("\nEnter meeting date (e.g. May 3, 2026): ").strip()
        attendees = input("Enter attendees (comma-separated, or press Enter to skip): ").strip()

        return {
            "notes": notes,
            "date": date,
            "attendees": attendees if attendees else None,
        }

    def run(self) -> str:
        """Collect inputs interactively, summarize the meeting, and print the result."""
        inputs = self.get_inputs()
        result = self.summarize(**inputs)
        print("\n--- Meeting Summary ---\n")
        print(result)
        return result

    def summarize(self, notes: str, date: str, attendees: str = None) -> str:
        """
        Summarize meeting notes into a structured report.

        Args:
            notes:     Raw meeting notes (multi-line text).
            date:      Meeting date string.
            attendees: Optional comma-separated list of attendees.

        Returns:
            Formatted summary with header, key points, decisions,
            action items, and next steps.
        """
        attendees_line = f"Attendees: {attendees}" if attendees else "Attendees: Not specified"

        system_prompt = """
        You are an expert meeting facilitator and business analyst.

        Convert raw meeting notes into a clean, structured summary.

        Do not invent information that is not explicitly mentioned in the notes.
        If information is missing, use 'None noted'.

        Always respond using the exact structure below:

        ===========================================
        MEETING SUMMARY
        ===========================================
        Date: [date]
        Attendees: [list attendees]

        SUMMARY
        [2-3 sentence overview of the meeting]

        KEY POINTS
        [Bullet list of discussion topics using •]

        DECISIONS
        [Numbered list of decisions made]

        ACTION ITEMS
        [Bullet list of tasks with owners where available]

        NEXT MEETING: [date if mentioned, otherwise 'Not scheduled']
        ===========================================
        """

        user_prompt = """
        Date: {date}
        Attendees: {attendees_line}

        Meeting Notes:
        {notes}
        """.format(date=date, attendees_line=attendees_line, notes=notes)

        return self._complete(system_prompt, user_prompt)
