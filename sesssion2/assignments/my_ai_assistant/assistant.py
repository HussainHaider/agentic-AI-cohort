import json
import re

# Import the shared client from the assignments-level config.py.
# This allows both assignments to share the same provider configuration.
from ..config import client, DEFAULT_MODEL

from .tools.calculator import calculate, calculator_tool
from .tools.web_search import web_search, web_search_tool
from .tools.data_analyzer import analyze_data, data_analyzer_tool
from .tools.time_tools import time_converter, time_converter_tool
from .tools.unit_converter import unit_converter, unit_converter_tool
from .tools.file_reader import file_reader, file_reader_tool


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

    # Maps natural-language aliases to a supported tone.
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
        system_prompt = f"""You are an expert email writer.
        Write in a {tone} tone: {tone_guidance}.
        If you need current information to write the email accurately, use web_search first.
        Always return the complete email in this exact format:
        Subject: <subject line>

        <greeting>,

        <body paragraphs>

        <closing>,
        <sender name placeholder>"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write email: {description}"}
        ]
        
        # First API call
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=self.tools
        )
        
        response_message = response.choices[0].message
        
        # Check if AI wants to research
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
                    "content": result
                })
            
            # Get final email with research
            final_response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages
            )
            
            return final_response.choices[0].message.content
        
        return response_message.content


class SmartSummarizer:
    """
    COMPLETE summarizer with detailed analytics.
    """
    
    def summarize(self, text, style="short"):
        print(f"\n📝 Summarizing ({style} style)...\n")
        
        # Analytics
        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        # Style instructions
        styles = {
            "short": "1-2 sentences",
            "medium": "A paragraph (3-4 sentences)",
            "detailed": "Multiple paragraphs"
        }
        
        # Get summary
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": f"Summarize as {styles.get(style, styles['short'])}"},
                {"role": "user", "content": f"Summarize:\n{text}"}
            ],
            temperature=0.3
        )
        
        summary = response.choices[0].message.content
        summary_words = len(summary.split())
        reduction = ((word_count - summary_words) / word_count * 100)
        
        # Display
        print("=" * 70)
        print("📊 SUMMARY ANALYSIS")
        print("=" * 70)
        print(f"Original: {word_count} words, ~{sentence_count} sentences")
        print(f"Summary: {summary_words} words")
        print(f"Reduction: {reduction:.1f}%")
        print(f"Style: {style.title()}")
        print()
        print("-" * 70)
        print("SUMMARY")
        print("-" * 70)
        print(summary)
        print("-" * 70)

class DataAnalyzer:
    """
    COMPLETE data analyzer that can handle various data formats and provide insights.
    """
    
    def analyze(self, data):
        print(f"\n📊 Analyzing data...\n")
        
        # For simplicity, we just return basic stats here.
        # In a real implementation, this could be much more complex.
        if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
            count = len(data)
            mean = sum(data) / count if count > 0 else 0
            minimum = min(data) if count > 0 else None
            maximum = max(data) if count > 0 else None
            
            analysis = f"Count: {count}\nMean: {mean:.2f}\nMin: {minimum}\nMax: {maximum}"
            print(analysis)
            return analysis
        else:
            print("Unsupported data format. Please provide a list of numbers.")
            return "Unsupported data format."
class MultiCapabilityAssistant:
    """
    COMPLETE multi-capability assistant.
    
    Features:
    - Enhanced email writer (with research, supports formal/friendly/casual tones)
    - Smart summarizer (with analytics)
    - Calculator, web search, data analysis tools, time conversion, unit conversion, file reading
    
    """
    
    def __init__(self):
        # All tools
        self.tools = [calculator_tool, web_search_tool, data_analyzer_tool, time_converter_tool, unit_converter_tool, file_reader_tool]
        self.functions = {
            "calculate": calculate,
            "web_search": web_search,
            "analyze_data": analyze_data,
            "time_converter": time_converter,
            "unit_converter": unit_converter,
            "file_reader": file_reader
        }
        
        # Sub-components
        self.email_writer = EnhancedEmailWriter()
        self.summarizer = SmartSummarizer()
        
        print("✅ Multi-Capability Assistant initialized!")
        print("   Capabilities: Chat, Email, Summarize, Calculate, Search, Analyze\n")
    
    def route_request(self, request):
        """Decide which capability to use"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['email', 'write to', 'compose']):
            return 'email'
        elif any(word in request_lower for word in ['summarize', 'summary']):
            return 'summarize'
        elif any(word in request_lower for word in ['calculate', 'math', 'average', 'sum', 'convert', 'time in', 'search']) or re.search(r'read\s+(the\s+)?(file|content|contents)', request_lower):
            return 'tools'
        else:
            return 'general'
    
    def process(self, request):
        """Process any request intelligently"""
        print(f"\n{'=' * 70}")
        print(f"📥 Request: {request}")
        print("=" * 70)
        
        capability = self.route_request(request)
        print(f"🎯 Using: {capability.upper()}\n")
        
        if capability == 'email':
            tone = self.email_writer._extract_tone(request)
            return self.email_writer.write(request, tone=tone)
        elif capability == 'summarize':
            return "Please provide text to summarize."
        elif capability == 'tools':
            return self.use_tools(request)
        else:
            return self.general_assistant(request)
    
    def use_tools(self, query):
        """Use tools to answer query"""
        messages = [{"role": "user", "content": query}]
        
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=self.tools
        )
        
        response_message = response.choices[0].message
        
        if not response_message.tool_calls:
            return response_message.content
        
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Using {function_name}...")
            
            try:
                result = self.functions[function_name](**function_args)
            except Exception as e:
                result = f"Search failed: {e}"
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        final_response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages
        )
        
        return final_response.choices[0].message.content
    
    def general_assistant(self, query):
        """General purpose assistant"""
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": query}],
            tools=self.tools
        )
        return response.choices[0].message.content

# Create the assistant
assistant = MultiCapabilityAssistant()

tests = [
## sub-component tests
# "Write a friendly email to a client named Sarah, updating her on the project status and next steps.",
#    "Summarize the following text: Artificial intelligence is transforming how businesses operate. Companies are using AI for customer service, data analysis, and automation. Machine learning models identify patterns in large datasets. Natural language processing enables computers to understand human language. AI adoption is accelerating across all industries and business sizes. Challenges include data privacy, ethics, and finding skilled professionals.",

## tools tests
#    "Calculate what is 15% of 250?",
#    "Search for the latest news on AI advancements.",
#    "Analyze the data [10, 20, 30, 40] to find the average.",
#    "Convert 3 PM EST to JST.",
#    "What is the current time in Tokyo?",
#    "Convert 100 meters to feet.",
#    "Read the contents of 'assignments/my_ai_assistant/sales.json'."
]

for test in tests:
    result = assistant.process(test)
    print(f"\n💬 Response:\n{result}\n")
    print("=" * 70)