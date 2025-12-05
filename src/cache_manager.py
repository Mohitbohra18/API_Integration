# src/cache_manager.py
"""Cache manager: in-memory + file-based JSON caching with TTL."""

from typing import Any, Dict, Optional
import json
import os
import time
import logging
from contextlib import contextmanager

from .utils import safe_get

LOGGER = logging.getLogger(__name__)


class CacheIOError(Exception):
    """Cache related IO errors."""


class CacheManager:
    """File + in-memory cache manager."""

    def __init__(self, cache_dir: str = "cache", ttl_seconds: int = 300) -> None:
        """
        :param cache_dir: Directory to store cache files.
        :param ttl_seconds: Time-to-live for cache entries in seconds.
        """
        self.cache_dir = cache_dir
        self.ttl = ttl_seconds
        os.makedirs(self.cache_dir, exist_ok=True)
        # in-memory store: {key: (timestamp, data)}
        self._mem_cache: Dict[str, Dict[str, Any]] = {}
        LOGGER.debug("CacheManager initialized at %s with TTL=%s", cache_dir, ttl_seconds)

    def _file_path(self, key: str) -> str:
        safe_name = key.replace("/", "_").strip("_")
        return os.path.join(self.cache_dir, f"{safe_name}.json")

    def save(self, key: str, data: Any) -> None:
        """Save data to file cache and memory."""
        ts = int(time.time())
        self._mem_cache[key] = {"ts": ts, "data": data}
        path = self._file_path(key)
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"ts": ts, "data": data}, fh, ensure_ascii=False, indent=2)
            LOGGER.debug("Saved cache to %s", path)
        except OSError as e:
            LOGGER.exception("Failed to write cache file %s", path)
            raise CacheIOError(f"Failed to write cache file {path}") from e

    def load(self, key: str, allow_stale: bool = False) -> Optional[Any]:
        """Load data from memory or file if TTL not expired. Returns None if no valid cache."""
        # check memory first
        mem = self._mem_cache.get(key)
        now = int(time.time())
        if mem:
            age = now - mem["ts"]
            if allow_stale or age <= self.ttl:
                LOGGER.debug("Returning in-memory cache for %s (age=%ds)", key, age)
                return mem["data"]
            LOGGER.debug("In-memory cache expired for %s (age=%ds)", key, age)
        # then file
        path = self._file_path(key)
        if not os.path.exists(path):
            LOGGER.debug("Cache file missing %s", path)
            return None
        try:
            with open(path, "r", encoding="utf-8") as fh:
                obj = json.load(fh)
            ts = safe_get(obj, "ts", 0)
            data = safe_get(obj, "data", None)
            if data is None:
                LOGGER.warning("Cache file %s contained no data", path)
                return None
            age = now - int(ts)
            if allow_stale or age <= self.ttl:
                # refresh memory cache
                self._mem_cache[key] = {"ts": int(ts), "data": data}
                LOGGER.debug("Loaded cache from file %s (age=%ds)", path, age)
                return data
            LOGGER.debug("Cache file expired %s (age=%ds)", path, age)
            return None
        except (OSError, ValueError) as e:
            LOGGER.exception("Failed to read/parse cache file %s", path)
            raise CacheIOError(f"Failed to read cache file {path}") from e

    def clear(self, key: Optional[str] = None) -> None:
        """Clear a single key or all caches."""
        if key:
            self._mem_cache.pop(key, None)
            try:
                os.remove(self._file_path(key))
            except Exception:
                pass
            LOGGER.info("Cleared cache for %s", key)
        else:
            self._mem_cache.clear()
            # remove files
            for fname in os.listdir(self.cache_dir):
                path = os.path.join(self.cache_dir, fname)
                try:
                    os.remove(path)
                except Exception:
                    pass
            LOGGER.info("Cleared all cache files")

    def stats(self) -> Dict[str, Any]:
        """Return simple cache stats."""
        return {
            "in_memory_keys": list(self._mem_cache.keys()),
            "file_count": len([f for f in os.listdir(self.cache_dir) if f.endswith(".json")]),
            "ttl_seconds": self.ttl,
        }
