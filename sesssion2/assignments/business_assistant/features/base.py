from ...config import client as openai_client, DEFAULT_MODEL


class BaseFeature:
    """Base class for all business assistant features.

    Provides a shared OpenAI client and a ``_complete`` helper that handles
    the repetitive message-building and API-call pattern used by every feature.
    """

    def __init__(self):
        self.client = openai_client

    def _complete(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Call the chat completions API and return the response text.

        Args:
            system_prompt: The system-role message content.
            user_prompt:   The user-role message content.
            **kwargs:      Any extra keyword arguments forwarded to
                           ``chat.completions.create`` (e.g. ``tools=``,
                           ``tool_choice=``).

        Returns:
            The assistant's reply as a stripped string.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = self.client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content.strip()
