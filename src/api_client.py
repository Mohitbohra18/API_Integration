# src/api_client.py
"""API client for JSONPlaceholder with robust error handling, retries, and validation."""

from typing import List, Dict, Any, Optional
import requests
import time
import logging

from .utils import timer

LOGGER = logging.getLogger(__name__)


class APIClientError(Exception):
    """Base class for API client exceptions."""


class APIClient:
    """Simple API client for JSONPlaceholder."""

    def __init__(
        self,
        base_url: str = "https://jsonplaceholder.typicode.com",
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        """
        Initialize API client.
        :param base_url: Base API URL
        :param timeout: Request timeout in seconds
        :param max_retries: Number of retry attempts on network errors
        :param backoff_factor: Exponential backoff multiplier
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = requests.Session()
        LOGGER.debug("APIClient initialized with base_url=%s", self.base_url)

    def _request(self, path: str) -> List[Dict[str, Any]]:
        """Internal request with retries and JSON validation."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                LOGGER.debug("Requesting %s (attempt %d)", url, attempt)
                start = time.time()
                resp = self.session.get(url, timeout=self.timeout)
                elapsed = time.time() - start
                LOGGER.info("GET %s -> %s (%s)", url, resp.status_code, f"{elapsed:.3f}s")
                if resp.status_code >= 500:
                    # Server error - may retry
                    raise APIClientError(f"Server error: {resp.status_code}")
                if resp.status_code >= 400:
                    # Client error - do not retry
                    raise APIClientError(f"Client error: {resp.status_code} - {resp.text}")
                try:
                    data = resp.json()
                except ValueError as e:
                    raise APIClientError("Invalid JSON response") from e
                if not isinstance(data, list):
                    # JSONPlaceholder returns list for these endpoints - validate basic shape
                    raise APIClientError("Unexpected JSON shape - expected list")
                # Basic data validation (non-empty list acceptable)
                LOGGER.debug("Received %d items from %s", len(data), url)
                return data
            except (requests.Timeout, requests.ConnectionError) as e:
                last_exc = e
                wait = self.backoff_factor * (2 ** (attempt - 1))
                LOGGER.warning("Network error on attempt %d: %s; retrying after %.2fs", attempt, e, wait)
                time.sleep(wait)
            except APIClientError as e:
                # For client errors (4xx) or parsing issues, don't retry further
                LOGGER.error("API client error: %s", e)
                raise
            except Exception as e:
                last_exc = e
                LOGGER.exception("Unexpected error during request")
                wait = self.backoff_factor * (2 ** (attempt - 1))
                time.sleep(wait)
        # if we get here, all retries failed
        LOGGER.critical("All retries failed for %s", url)
        raise APIClientError(f"Failed to fetch {url}") from last_exc

    def fetch_posts(self) -> List[Dict[str, Any]]:
        """Fetch posts from /posts endpoint."""
        with timer("fetch_posts"):
            return self._request("/posts")

    def fetch_users(self) -> List[Dict[str, Any]]:
        """Fetch users from /users endpoint."""
        with timer("fetch_users"):
            return self._request("/users")
