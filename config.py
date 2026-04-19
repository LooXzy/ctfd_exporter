import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

CTFD_URL = os.getenv("CTFD_URL", "").rstrip("/")
CTFD_TOKEN = os.getenv("CTFD_TOKEN", "")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))
PORT = 8000

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if not CTFD_URL or not CTFD_TOKEN:
    logging.error("CTFD_URL and CTFD_TOKEN environment variables must be set.")
    sys.exit(1)
