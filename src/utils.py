# src/utils.py
"""Utility helpers: timing context manager, validation and colored printing helpers."""

from contextlib import contextmanager
import time
import logging
from typing import Iterator, Tuple, Any, Dict
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)


LOGGER = logging.getLogger(__name__)


@contextmanager
def timer(name: str) -> Iterator[float]:
    """Context manager to time a block of code.

    Usage:
        with timer("fetch"):
            ...
    """
    start = time.time()
    try:
        yield start
    finally:
        elapsed = time.time() - start
        LOGGER.debug("%s finished in %.3fs", name, elapsed)


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get a value from a dict; returns default when missing."""
    try:
        return data.get(key, default)
    except Exception:
        return default


def colored(text: str, color: str = "green") -> str:
    """Return colored text for terminals."""
    colors = {
        "green": Fore.GREEN,
        "red": Fore.RED,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
    }
    return f"{colors.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}"


def format_timing(ms: float) -> str:
    """Return a human readable timing string in ms with 3 decimals."""
    return f"{ms*1000:.3f} ms"
