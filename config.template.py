"""
SignSafe Configuration Template
Copy this file to config.py and update with your actual API keys
"""

# API Keys - Update these with your actual keys
GEMINI_API_KEY = "your_gemini_api_key_here"
OMNIDIMENSION_API_KEY = "your_omnidimension_api_key_here"

# Application Settings
DEBUG = False
LOG_LEVEL = "INFO"

# File Processing Settings
MAX_FILE_SIZE_MB = 200
SUPPORTED_FILE_TYPES = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']

# AI Processing Settings
AI_REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 5  # seconds between API calls