"""Filtering utilities for posts and users."""

from typing import List, Dict, Any, Optional
import logging

LOGGER = logging.getLogger(__name__)


def filter_posts(
    posts: List[Dict[str, Any]],
    user_id: Optional[int] = None,
    limit: Optional[int] = None,
    search: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter posts by user_id, search keyword in title/body, and limit results."""
    results = posts
    if user_id is not None:
        results = [p for p in results if p.get("userId") == user_id]
        LOGGER.debug("Filtered posts by user_id=%s -> %d results", user_id, len(results))
    if search:
        s = search.lower()
        results = [p for p in results if s in (p.get("title", "").lower() + p.get("body", "").lower())]
        LOGGER.debug("Filtered posts by search='%s' -> %d results", search, len(results))
    if limit is not None:
        results = results[:limit]
    return results


def get_post_by_id(posts: List[Dict[str, Any]], post_id: int) -> Optional[Dict[str, Any]]:
    """Return a post matching id or None."""
    for p in posts:
        if p.get("id") == post_id:
            return p
    return None


def filter_users(users: List[Dict[str, Any]], limit: Optional[int] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Filter users with optional name search and limit."""
    results = users
    if search:
        s = search.lower()
        results = [u for u in results if s in (u.get("name", "").lower() + u.get("username", "").lower())]
    if limit is not None:
        results = results[:limit]
    LOGGER.debug("filter_users -> %d results", len(results))
    return results


def get_user_by_id(users: List[Dict[str, Any]], user_id: int) -> Optional[Dict[str, Any]]:
    """Return a user by id or None."""
    for u in users:
        if u.get("id") == user_id:
            return u
    return None
