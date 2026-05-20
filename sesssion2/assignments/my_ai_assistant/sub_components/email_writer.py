import json

from ...config import client, DEFAULT_MODEL
from ..tools.web_search import web_search, web_search_tool


class EnhancedEmailWriter:
    """
    Enhanced email writer that can research topics before writing.
    Supports formal, friendly, and casual tones.
    Returns a complete email with subject line.
    """

    TONE_DESCRIPTIONS = {
        "formal": "very formal and professional, using proper titles, structured paragraphs, and polite language suitable for business or official correspondence",
        "friendly": "warm and friendly yet professional, using approachable language, a conversational style, and a positive tone",
        "casual": "casual and relaxed, using informal language, contractions, and a conversational tone as if writing to a close colleague or friend",
    }

    _TONE_ALIASES = {
        "formal":       "formal",
        "professional": "formal",
        "official":     "formal",
        "friendly":     "friendly",
        "warm":         "friendly",
        "casual":       "casual",
        "informal":     "casual",
        "relaxed":      "casual",
    }

    def __init__(self):
        self.tools = [web_search_tool]
        self.functions = {"web_search": web_search}

    def _extract_tone(self, text):
        """Return the tone keyword found in the text, defaulting to 'formal'."""
        text_lower = text.lower()
        for keyword, tone in self._TONE_ALIASES.items():
            if keyword in text_lower:
                return tone
        return "formal"

    def write(self, description, tone="formal"):
        tone = tone.lower()
        if tone not in self.TONE_DESCRIPTIONS:
            supported = ", ".join(self.TONE_DESCRIPTIONS)
            raise ValueError(f"Unsupported tone '{tone}'. Choose from: {supported}")

        print(f"\n📧 Writing email: {description}")
        print(f"   Tone: {tone}\n")

        tone_guidance = self.TONE_DESCRIPTIONS[tone]
        system_prompt = (
            f"You are an expert email writer.\n"
            f"Write in a {tone} tone: {tone_guidance}.\n"
            "If you need current information to write the email accurately, use web_search first.\n"
            "Always return the complete email in this exact format:\n"
            "Subject: <subject line>\n\n"
            "<greeting>,\n\n"
            "<body paragraphs>\n\n"
            "<closing>,\n"
            "<sender name placeholder>"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write email: {description}"},
        ]

        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=self.tools,
        )

        response_message = response.choices[0].message

        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"🔍 Researching: {function_args.get('query', 'N/A')}")

                result = self.functions[function_name](**function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

            final_response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages,
            )
            return final_response.choices[0].message.content

        return response_message.content
