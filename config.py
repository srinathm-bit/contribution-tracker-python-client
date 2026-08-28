import os
import logging
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

# Backward compatibility for files using BASE_URL
BASE_URL = API_BASE_URL