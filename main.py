"""Entry point for the API Integration project."""

import os
import logging
from src.api_client import APIClient
from src.cache_manager import CacheManager
from src.cli import CLI

# load simple env config if present
from dotenv import load_dotenv
load_dotenv()  # reads .env or config.env if present

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CACHE_DIR = os.getenv("CACHE_DIR", "cache")
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
API_BASE = os.getenv("API_BASE", "https://jsonplaceholder.typicode.com")

logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO), format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)

def main():
    api_client = APIClient(base_url=API_BASE, timeout=10, max_retries=3)
    cache_manager = CacheManager(cache_dir=CACHE_DIR, ttl_seconds=CACHE_TTL)
    cli = CLI(api_client=api_client, cache_manager=cache_manager)
    exit_code = cli.run()
    return exit_code

if __name__ == "__main__":
    raise SystemExit(main())
