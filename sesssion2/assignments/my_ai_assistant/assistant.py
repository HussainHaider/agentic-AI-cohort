import json
import re

# Import the shared client from the assignments-level config.py.
# This allows both assignments to share the same provider configuration.
from ..config import client

from .tools.calculator import calculate, calculator_tool
from .tools.web_search import web_search, web_search_tool
from .tools.data_analyzer import analyze_data, data_analyzer_tool
from .tools.time_tools import time_converter, time_converter_tool
from .tools.unit_converter import unit_converter, unit_converter_tool
from .tools.file_reader import file_reader, file_reader_tool


class EnhancedEmailWriter:
    """
    COMPLETE email writer that can research topics.
    """
    
    def __init__(self):
        self.tools = [web_search_tool]
        self.functions = {"web_search": web_search}
    
    def write(self, description, tone="professional"):
        print(f"\n📧 Writing email: {description}")
        print(f"   Tone: {tone}\n")
        
        system_prompt = f"""You are a professional email writer.
        Write in a {tone} tone.
        If you need current information, use web_search.
        Include subject, greeting, body, closing."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write email: {description}"}
        ]
        
        # First API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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
                model="gpt-3.5-turbo",
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
            model="gpt-3.5-turbo",
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


class MultiCapabilityAssistant:
    """
    COMPLETE multi-capability assistant.
    
    Features:
    - Enhanced email writer (with research)
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
            return self.email_writer.write(request)
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
            model="gpt-3.5-turbo",
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
            
            result = self.functions[function_name](**function_args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        return final_response.choices[0].message.content
    
    def general_assistant(self, query):
        """General purpose assistant"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            tools=self.tools
        )
        return response.choices[0].message.content

# Create the assistant
assistant = MultiCapabilityAssistant()

tests = [
## sub-component tests
#    "Write an email to announce new AI features to the team.",
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