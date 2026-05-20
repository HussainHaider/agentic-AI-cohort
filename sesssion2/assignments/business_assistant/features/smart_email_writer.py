import json
from ..tools.web_search import web_search, web_search_tool
from .base import BaseFeature

RECIPIENT_TYPES = ["client", "team", "stakeholder", "supplier"]
TONE_OPTIONS = ["formal", "professional", "friendly"]


class SmartEmailWriter(BaseFeature):
    """Feature 1: Writes professional business emails with optional market research."""


    def get_inputs(self) -> dict:
        """Collect all required inputs interactively from the user."""
        print("\n--- Smart Email Writer ---")

        print("Recipient types: " + ", ".join(RECIPIENT_TYPES))
        purpose = input("\nEnter email purpose: ").strip()
        recipient = input("Enter recipient type (client / team / stakeholder / supplier): ").strip()

        print("Tone options: " + ", ".join(TONE_OPTIONS))
        tone = input("Enter tone (formal / professional / friendly) [professional]: ").strip()
        if not tone:
            tone = "professional"

        research_topic = input("Enter a topic to research (or press Enter to skip): ").strip()

        return {
            "purpose": purpose,
            "recipient": recipient,
            "tone": tone,
            "research_topic": research_topic if research_topic else None,
        }

    def run(self) -> str:
        """Collect inputs interactively, write the email, and print it."""
        inputs = self.get_inputs()
        result = self.write(**inputs)
        print("\n--- Generated Email ---\n")
        print(result)
        return result

    def write(self, purpose: str, recipient: str, tone: str, research_topic: str = None) -> str:
        """
        Write a professional business email.

        Args:
            purpose:        What the email should accomplish.
            recipient:      Type of recipient (client, team, stakeholder, supplier).
            tone:           Desired tone (formal, professional, friendly).
            research_topic: Optional topic to research before writing.

        Returns:
            Formatted email with subject line, greeting, body, and closing.
        """
        research_context = ""
        if research_topic:
            raw = web_search(research_topic)
            result = json.loads(raw).get("results", "")
            research_context = f"\nResearch findings to incorporate:\n{result}\n"

        system_prompt = (
            "You are an expert business email writer.\n\n"
            f"Write emails appropriate for a {recipient} audience using a {tone} tone.\n"
            "Always structure your output in EXACTLY this format:\n\n"
            "Subject: [compelling subject line]\n\n"
            "Dear [appropriate salutation],\n\n"
            "[3-5 body paragraphs]\n\n"
            "[Professional closing],\n"
            "[Your Name]\n"
            "[Title], [Company Name]\n\n"
            "Do not add any text outside this structure."
        )

        user_prompt = (
            f"Email purpose: {purpose}\n"
            f"Recipient type: {recipient}\n"
            f"Tone: {tone}"
            f"{research_context}"
        )

        return self._complete(system_prompt, user_prompt, tools=[web_search_tool], tool_choice="none")
