"""
Configuration for Llama API
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Llama API Configuration
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
LLAMA_BASE_URL = "https://api.llama-api.com"
LLAMA_MODEL = "llama-4-maverick-17b-128e-instruct-fp8"

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