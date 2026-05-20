from ...config import client as openai_client, DEFAULT_MODEL


class MeetingSummarizer:
    """Feature 3: Converts meeting notes into structured summaries with action items."""

    def __init__(self):
        self.client = openai_client

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

        system_prompt = (
            "You are an expert meeting facilitator and business analyst.\n\n"
            "Convert raw meeting notes into a clean, structured summary.\n\n"
            "Always respond in EXACTLY this format (keep the separator lines):\n\n"
            "===========================================\n"
            "MEETING SUMMARY\n"
            "===========================================\n"
            "Date: [date]\n"
            "[Attendees line]\n\n"
            "SUMMARY\n"
            "[2-3 sentence overview of the meeting]\n\n"
            "KEY POINTS\n"
            "[Bullet list of main discussion topics, one per line starting with •]\n\n"
            "DECISIONS\n"
            "[Numbered list of decisions made]\n\n"
            "ACTION ITEMS\n"
            "[Bullet list of action items with owners where mentioned, e.g. • Name: task]\n\n"
            "NEXT MEETING: [date if mentioned, otherwise 'Not scheduled']\n"
            "===========================================\n\n"
            "If a section has no content, write 'None noted' under it."
        )

        user_prompt = (
            f"Date: {date}\n"
            f"{attendees_line}\n\n"
            f"Meeting Notes:\n{notes}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
        )

        return response.choices[0].message.content.strip()
