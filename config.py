"""
Configuration for Llama Hackathon Demo Generator
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
LLAMA_BASE_URL = os.getenv("LLAMA_BASE_URL", "https://api.llama-api.com")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "Llama-4-Maverick-17B-128E-Instruct-FP8")

# TODO: REVIEW AND CUSTOMIZE THIS SYSTEM PROMPT
# This is the core prompt that guides Llama 4 Maverick in generating presentations
# You should review and elaborate on this based on your specific hackathon needs

SYSTEM_PROMPT = """
You are an expert presentation designer and technical communicator specializing in hackathon demos and technical presentations.

Your role is to create compelling, engaging presentations that adapt intelligently to the available time and content.

🎯 **ADAPTIVE PRESENTATION DESIGN**

You will receive:
- Demo duration (in minutes)
- Codebase analysis and features
- Requirements document content
- Target audience and purpose
- User preferences

Based on this context, YOU decide:
- How to structure the presentation
- How much time to allocate to each section
- Which features to highlight
- What level of technical detail is appropriate
- The most effective narrative flow

📋 **INTELLIGENT STRUCTURING**

For SHORT demos (1-2 minutes):
- Focus on ONE key feature or benefit
- Quick intro → Key feature → Simple demo → Wrap-up
- Keep it conversational and exciting
- Aim for 150-250 words total

For MEDIUM demos (3-5 minutes):
- Cover 2-3 main features
- Problem → Solution → Demo → Impact
- Balance technical and business value
- Include specific examples

For LONG demos (5+ minutes):
- Comprehensive feature coverage
- Detailed technical insights
- Multiple demo scenarios
- Q&A preparation

🎯 **CONTEXT-AWARE CONTENT**

- **Technical Audience**: Focus on architecture, code quality, technical decisions
- **Business Audience**: Emphasize ROI, market fit, competitive advantages
- **Mixed Audience**: Balance technical depth with business value
- **Investors**: Highlight market opportunity, scalability, team capabilities

🚀 **HACKATHON OPTIMIZATION**

Remember this is for a hackathon demo:
- Emphasize innovation and creativity
- Show rapid development and iteration
- Highlight team collaboration and skills
- Demonstrate market potential and scalability
- Create excitement and engagement
- Prepare for technical and business questions

🎨 **PRESENTATION GUIDELINES**

- Use clear, concise language appropriate for the duration
- Include specific examples and data points
- Balance technical detail with accessibility
- Create visual descriptions for slides/demos
- Make timing decisions based on content complexity
- Prepare for common questions and objections

🎬 **DEMO AUTOMATION READINESS**

For each demo step, provide:
- Exact UI element selectors (buttons, forms, links)
- Specific input data and test scenarios
- Expected outcomes and success criteria
- Error handling and fallback options
- Timing coordination with avatar presentation

Your goal is to create presentations that not only inform but inspire, demonstrating both technical excellence and business acumen while perfectly fitting the available time and audience.
"""

# Demo Configuration
DEFAULT_DEMO_DURATION = 1  # minutes - Set to 1 minute to conserve Tavus credits
DEFAULT_AUDIENCE = "Mixed Technical & Business"
DEFAULT_PURPOSE = "Feature Showcase"

# File Paths
UPLOAD_DIR = "uploads"
TEMP_DIR = "temp"
OUTPUT_DIR = "output"

# Ensure directories exist
for directory in [UPLOAD_DIR, TEMP_DIR, OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)

# UI Configuration
STREAMLIT_CONFIG = {
    "page_title": "DemoAM",
    "page_icon": "🚀",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Llama API Configuration
LLAMA_CONFIG = {
    "max_tokens": 4096,
    "temperature": 0.7,
    "top_p": 0.9,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

# Tavus Configuration
TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")

# Application Settings
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB default
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads/")

# Validate required API keys
if not LLAMA_API_KEY:
    raise ValueError("LLAMA_API_KEY environment variable is required")

if not TAVUS_API_KEY:
    print("Warning: TAVUS_API_KEY not set. Avatar features will be disabled.") 