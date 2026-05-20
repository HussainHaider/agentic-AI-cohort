from ...config import client, DEFAULT_MODEL


class SmartSummarizer:
    """
    Summarizer with detailed analytics.
    Returns a formatted report string including statistics and the summary.
    """

    STYLE_DESCRIPTIONS = {
        "short":    "1-2 concise sentences capturing only the core idea",
        "medium":   "a well-structured paragraph of 3-4 sentences covering the main points",
        "detailed": "multiple paragraphs that cover all key points, supporting details, and conclusions",
    }

    _STYLE_ALIASES = {
        "short":    "short",
        "brief":    "short",
        "quick":    "short",
        "medium":   "medium",
        "moderate": "medium",
        "standard": "medium",
        "detailed": "detailed",
        "long":     "detailed",
        "full":     "detailed",
        "thorough": "detailed",
        "complete": "detailed",
    }

    def _extract_style(self, text: str) -> str:
        """Return the summary style found in the text, defaulting to 'short'."""
        text_lower = text.lower()
        for keyword, style in self._STYLE_ALIASES.items():
            if keyword in text_lower:
                return style
        return "short"

    def summarize(self, text: str, style: str = "short") -> str:
        """Summarize text and return a formatted report string."""
        style = style.lower()
        if style not in self.STYLE_DESCRIPTIONS:
            supported = ", ".join(self.STYLE_DESCRIPTIONS)
            raise ValueError(f"Unsupported style '{style}'. Choose from: {supported}")

        print(f"\n📝 Summarizing ({style} style)...\n")

        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')

        style_guidance = self.STYLE_DESCRIPTIONS[style]
        system_prompt = (
            "You are an expert summarizer. Your task is to produce accurate, faithful summaries "
            "that preserve the original meaning without adding opinions or outside information.\n"
            f"Write the summary as {style_guidance}.\n"
            "Use clear, plain language. Do not include phrases like 'This text discusses' or 'The author says'."
        )

        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Summarize the following:\n\n{text}"},
            ],
            temperature=0.3,
        )

        summary = response.choices[0].message.content
        summary_words = len(summary.split())
        reduction = (word_count - summary_words) / word_count * 100

        lines = [
            "=" * 70,
            "📊 SUMMARY ANALYSIS",
            "=" * 70,
            f"Original: {word_count} words, ~{sentence_count} sentences",
            f"Summary:  {summary_words} words",
            f"Reduction: {reduction:.1f}%",
            f"Style: {style.title()}",
            "",
            "-" * 70,
            "SUMMARY",
            "-" * 70,
            summary,
            "-" * 70,
        ]
        return "\n".join(lines)
