from .base import BaseFeature

COMMUNICATION_TYPES = {
    "project proposal": "project proposal",
    "status update": "status update",
    "response to inquiry": "response to inquiry",
    "follow-up message": "follow-up message",
}


class ClientCommunicationDrafter(BaseFeature):
    """Feature 5: Drafts professional client communications."""


    def get_inputs(self) -> dict:
        """Collect all required inputs interactively from the user."""
        print("\n--- Client Communication Drafter ---")
        print("Available communication types:")
        for i, ct in enumerate(COMMUNICATION_TYPES, 1):
            print(f"  {i}. {ct.title()}")

        comm_type  = input("\nEnter communication type: ").strip()
        client_name = input("Enter client name / company: ").strip()
        context    = input("Enter context / details: ").strip()
        tone       = input("Enter tone preference (e.g. professional, friendly, formal) [professional]: ").strip()

        if not tone:
            tone = "professional"

        return {
            "comm_type": comm_type,
            "client_name": client_name,
            "context": context,
            "tone": tone,
        }

    def run(self) -> str:
        """Collect inputs interactively, draft the communication, and print it."""
        inputs = self.get_inputs()
        result = self.draft(**inputs)
        print("\n--- Generated Communication ---\n")
        print(result)
        return result

    def draft(self, comm_type: str, client_name: str, context: str, tone: str) -> str:
        """
        Draft a professional client communication.

        Args:
            comm_type:   One of 'project proposal', 'status update',
                         'response to inquiry', 'follow-up message'.
            client_name: Client name or company.
            context:     Relevant details (project info, budget, timeline, etc.).
            tone:        Desired tone, e.g. 'professional', 'friendly', 'formal'.

        Returns:
            A fully formatted communication string with greeting, body,
            call-to-action, and professional closing.
        """
        comm_type_normalised = comm_type.strip().lower()

        system_prompt = (
            "You are an expert business communication writer who creates "
            "polished, professional client-facing documents.\n\n"
            "Always structure your output with ALL four of these sections:\n"
            "1. Professional greeting addressed to the client.\n"
            "2. Context-appropriate body (2-3 paragraphs).\n"
            "3. Clear call-to-action.\n"
            "4. Professional closing with '[Your Name]' as the sender placeholder.\n\n"
            f"Tone: {tone}."
        )

        user_prompt = (
            f"Write a {comm_type_normalised} for the following:\n"
            f"Client / Company: {client_name}\n"
            f"Details / Context: {context}\n\n"
            "Return the complete communication ready to send — do not add any "
            "explanatory text outside the communication itself."
        )

        return self._complete(system_prompt, user_prompt)

    # ------------------------------------------------------------------
    # Convenience wrappers for each communication type
    # ------------------------------------------------------------------

    def draft_project_proposal(self, client_name: str, context: str, tone: str = "professional but friendly") -> str:
        """Draft a project proposal."""
        return self.draft("project proposal", client_name, context, tone)

    def draft_status_update(self, client_name: str, context: str, tone: str = "professional") -> str:
        """Draft a project status update."""
        return self.draft("status update", client_name, context, tone)

    def draft_inquiry_response(self, client_name: str, context: str, tone: str = "professional") -> str:
        """Draft a response to a client inquiry."""
        return self.draft("response to inquiry", client_name, context, tone)

    def draft_followup(self, client_name: str, context: str, tone: str = "friendly") -> str:
        """Draft a follow-up message."""
        return self.draft("follow-up message", client_name, context, tone)