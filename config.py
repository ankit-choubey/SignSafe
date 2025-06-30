"""
SignSafe Configuration
API keys and configuration settings
"""

# API Keys - Update these with your actual keys
GEMINI_API_KEY = "AIzaSyBlLBhvRnucpTd80qEIsropN6J26qigNVY"
OMNIDIMENSION_API_KEY = "mqH3kVdj6lhiUBF19X8D0F93epBvEfGPuu0-GiX4Y3w"

# Application Settings
DEBUG = False
LOG_LEVEL = "INFO"

# File Processing Settings
MAX_FILE_SIZE_MB = 200
SUPPORTED_FILE_TYPES = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']

# AI Processing Settings
AI_REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 5  # seconds between API calls