import json
from ...config import client as openai_client, DEFAULT_MODEL


class BaseFeature:
    """Base class for all business assistant features.

    Provides a shared OpenAI client and a ``_complete`` helper that handles
    the repetitive message-building and API-call pattern used by every feature.
    """

    def __init__(self):
        self.client = openai_client

    def _complete(
        self,
        system_prompt: str,
        user_prompt: str,
        functions: dict = None,
        **kwargs,
    ) -> str:
        """Call the chat completions API and return the response text.

        Handles the tool-call loop automatically: if the model returns tool
        calls and a ``functions`` mapping is provided, each tool is executed
        and its result is fed back to the model for a final response.

        Args:
            system_prompt: The system-role message content.
            user_prompt:   The user-role message content.
            functions:     Mapping of tool name to callable.  Required when
                           ``tools=`` is passed so the loop can execute calls.
            **kwargs:      Any extra keyword arguments forwarded to
                           ``chat.completions.create`` (e.g. ``tools=``).

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
        response_message = response.choices[0].message

        if functions and response_message.tool_calls:
            messages.append(response_message)
            for tool_call in response_message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                result = functions[fn_name](**fn_args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
            final = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages,
            )
            return final.choices[0].message.content.strip()

        return response_message.content.strip()
