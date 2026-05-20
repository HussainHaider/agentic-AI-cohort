import json
import re

from ..config import client, DEFAULT_MODEL

from .tools.calculator import calculate, calculator_tool
from .tools.web_search import web_search, web_search_tool
from .tools.data_analyzer import analyze_data, data_analyzer_tool
from .tools.time_tools import time_converter, time_converter_tool
from .tools.unit_converter import unit_converter, unit_converter_tool
from .tools.file_reader import file_reader, file_reader_tool

from .sub_components.email_writer import EnhancedEmailWriter
from .sub_components.summarizer import SmartSummarizer
from .sub_components.data_analyzer_agent import DataAnalyzer


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
        self.data_analyzer = DataAnalyzer()
        
        print("\n" + "=" * 70)
        print("🤖  MULTI-CAPABILITY AI ASSISTANT")
        print("=" * 70)
        print("  Capabilities:")
        print("    📧  Email Writer    — formal / friendly / casual tones")
        print("    📝  Summarizer      — short / medium / detailed styles")
        print("    📊  Data Analyzer   — reads files, computes stats")
        print("    🔢  Calculator      — evaluates math expressions")
        print("    🔍  Web Search      — researches topics")
        print("    🕐  Time Converter  — converts across timezones")
        print("    📏  Unit Converter  — length, weight, temperature & more")
        print("    📂  File Reader     — reads file contents")
        print("=" * 70)
        print("  Ready! Type any request and it will be routed automatically.")
        print("=" * 70 + "\n")
    
    def route_request(self, request):
        """Decide which capability to use"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['email', 'write to', 'compose']):
            return 'email'
        elif any(word in request_lower for word in ['summarize', 'summary']):
            return 'summarize'
        elif any(word in request_lower for word in ['analyze', 'analyse']) and re.search(r'\.(json|csv|txt)', request_lower):
            return 'analyze'
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
            style = self.summarizer._extract_style(request)
            text_match = re.search(r'(?:summarize|summary)[^:]*[:\s]+(.+)', request, re.IGNORECASE | re.DOTALL)
            text = text_match.group(1).strip() if text_match else request
            return self.summarizer.summarize(text, style=style)
        elif capability == 'analyze':
            path_match = re.search(r"['\"]([^'\"]+\.(json|csv|txt))['\"]|(\S+\.(json|csv|txt))", request)
            file_path = (path_match.group(1) or path_match.group(3)) if path_match else "assignments/my_ai_assistant/sales.json"
            field = self.data_analyzer._extract_numeric_field(request)
            return self.data_analyzer.analyze(file_path, numeric_field=field)
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


if __name__ == "__main__":
    assistant = MultiCapabilityAssistant()

    tests = [
        ## sub-component tests
        # "Write a friendly email to a client named Sarah, updating her on the project status and next steps.",
        # "Summarize the following text: Artificial intelligence is transforming how businesses operate. Companies are using AI for customer service, data analysis, and automation. Machine learning models identify patterns in large datasets. Natural language processing enables computers to understand human language. AI adoption is accelerating across all industries and business sizes. Challenges include data privacy, ethics, and finding skilled professionals.",
        # "Analyze 'assignments/my_ai_assistant/sales.json' and report the revenue stats.",

        ## tools tests
        # "Calculate what is 15% of 250?",
        # "Search for the latest news on AI advancements.",
        # "Analyze the data [10, 20, 30, 40] to find the average.",
        # "Convert 3 PM EST to JST.",
        # "What is the current time in Tokyo?",
        # "Convert 100 meters to feet.",
        # "Read the contents of 'assignments/my_ai_assistant/sales.json'.",
    ]

    for test in tests:
        result = assistant.process(test)
        print(f"\n💬 Response:\n{result}\n")
        print("=" * 70)