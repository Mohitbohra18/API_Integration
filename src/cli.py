"""Command-line interface wiring for the application."""

from typing import List, Optional
import argparse
import logging
import sys
import time

from .api_client import APIClient, APIClientError
from .cache_manager import CacheManager, CacheIOError
from .data_filter import (
    filter_posts,
    get_post_by_id,
    filter_users,
    get_user_by_id,
)
from .utils import colored, format_timing

LOGGER = logging.getLogger(__name__)


class CLI:
    """CLI wrapper to parse args and call appropriate components."""

    def __init__(self, api_client: APIClient, cache_manager: CacheManager) -> None:
        self.api = api_client
        self.cache = cache_manager

    def run(self, argv: Optional[List[str]] = None) -> int:
        parser = argparse.ArgumentParser(prog="api-integration", description="Global Trend - API Integration CLI")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
        parser.add_argument("--force", action="store_true", help="Force refresh from API (ignore cache)")
        parser.add_argument("--version", action="version", version="api-integration 1.0.0")
        subparsers = parser.add_subparsers(dest="command")

        # list posts
        lp = subparsers.add_parser("list", help="List resources")
        lp_sub = lp.add_subparsers(dest="resource")

        list_posts = lp_sub.add_parser("posts", help="List posts")
        list_posts.add_argument("--user-id", type=int, help="Filter by user id")
        list_posts.add_argument("--limit", type=int, help="Limit results")
        list_posts.add_argument("--search", type=str, help="Search keyword in title/body")

        list_users = lp_sub.add_parser("users", help="List users")
        list_users.add_argument("--limit", type=int, help="Limit users")
        list_users.add_argument("--search", type=str, help="Search in name/username")

        # get
        get_p = subparsers.add_parser("get", help="Get single resource")
        get_sub = get_p.add_subparsers(dest="resource")
        get_post = get_sub.add_parser("post", help="Get post by id")
        get_post.add_argument("id", type=int, help="Post id")
        get_user = get_sub.add_parser("user", help="Get user by id")
        get_user.add_argument("id", type=int, help="User id")

        args = parser.parse_args(argv)

        # configure logging
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
        else:
            logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

        try:
            if args.command == "list" and args.resource == "posts":
                return self._handle_list_posts(args, force=args.force)
            if args.command == "list" and args.resource == "users":
                return self._handle_list_users(args, force=args.force)
            if args.command == "get" and args.resource == "post":
                return self._handle_get_post(args.id, force=args.force)
            if args.command == "get" and args.resource == "user":
                return self._handle_get_user(args.id, force=args.force)
            parser.print_help()
            return 0
        except (APIClientError, CacheIOError) as e:
            LOGGER.error("Operation failed: %s", e)
            print(colored(f"Error: {str(e)}", "red"))
            return 2
        except Exception as e:
            LOGGER.exception("Unhandled exception")
            print(colored("An unexpected error occurred. See logs for details.", "red"))
            return 3

    def _fetch_with_cache(self, key: str, fetcher):
        """Helper to get data with cache and TTL. Returns (data, ms_elapsed, from_cache:bool)."""
        start = time.time()
        cached = self.cache.load(key)
        if cached is not None:
            ms = time.time() - start
            return cached, ms, True
        # fetch from API
        data = fetcher()
        self.cache.save(key, data)
        ms = time.time() - start
        return data, ms, False

    def _handle_list_posts(self, args, force: bool = False) -> int:
        """List posts with filters."""
        if force:
            self.cache.clear("posts")
        if force:
            # forced load from API (bypass file-based cache)
            posts = self.api.fetch_posts()
            self.cache.save("posts", posts)
            ms = 0.0
            from_cache = False
        else:
            posts, ms, from_cache = self._fetch_with_cache("posts", self.api.fetch_posts)
        # apply filters
        filtered = filter_posts(posts, user_id=getattr(args, "user_id", None), limit=getattr(args, "limit", None), search=getattr(args, "search", None))
        # print header
        source = "cache" if from_cache else "api"
        print(colored(f"Showing {len(filtered)} posts (source: {source}, time: {format_timing(ms)})", "cyan"))
        for p in filtered:
            title = p.get("title", "<no title>")
            pid = p.get("id", "<no id>")
            uid = p.get("userId", "<no userId>")
            print(f"[{pid}] (user {uid}) {title}")
        return 0

    def _handle_list_users(self, args, force: bool = False) -> int:
        """List users."""
        if force:
            self.cache.clear("users")
        users, ms, from_cache = self._fetch_with_cache("users", self.api.fetch_users)
        filtered = filter_users(users, limit=getattr(args, "limit", None), search=getattr(args, "search", None))
        source = "cache" if from_cache else "api"
        print(colored(f"Showing {len(filtered)} users (source: {source}, time: {format_timing(ms)})", "cyan"))
        for u in filtered:
            uid = u.get("id", "<no id>")
            name = u.get("name", "<no name>")
            username = u.get("username", "")
            print(f"[{uid}] {name} (@{username})")
        return 0

    def _handle_get_post(self, post_id: int, force: bool = False) -> int:
        """Get single post and show associated user info."""
        if force:
            self.cache.clear("posts")
        posts, ms_posts, from_cache_posts = self._fetch_with_cache("posts", self.api.fetch_posts)
        post = get_post_by_id(posts, post_id)
        if not post:
            print(colored(f"Post with id {post_id} not found.", "yellow"))
            return 1
        # get user for this post
        user_id = post.get("userId")
        users, ms_users, from_cache_users = self._fetch_with_cache("users", self.api.fetch_users)
        user = get_user_by_id(users, user_id)
        print(colored(f"Post [{post_id}] - {post.get('title')}", "green"))
        print(post.get("body", ""))
        if user:
            print(colored(f"\nAuthor: {user.get('name')} (@{user.get('username')})", "blue"))
            print(f"Email: {user.get('email')}")
            # posts count
            count = len([p for p in posts if p.get("userId") == user.get("id")])
            print(colored(f"Author posts: {count}", "magenta"))
        else:
            print(colored("Author info not available.", "yellow"))
        return 0

    def _handle_get_user(self, user_id: int, force: bool = False) -> int:
        """Get single user with their post count."""
        if force:
            self.cache.clear("users")
            self.cache.clear("posts")
        users, ms_users, from_cache_users = self._fetch_with_cache("users", self.api.fetch_users)
        user = get_user_by_id(users, user_id)
        if not user:
            print(colored(f"User with id {user_id} not found.", "yellow"))
            return 1
        posts, ms_posts, from_cache_posts = self._fetch_with_cache("posts", self.api.fetch_posts)
        post_count = len([p for p in posts if p.get("userId") == user_id])
        print(colored(f"User [{user_id}] {user.get('name')} (@{user.get('username')})", "green"))
        print(f"Email: {user.get('email')}")
        print(f"Company: {user.get('company', {}).get('name')}")
        print(colored(f"Posts count: {post_count}", "magenta"))
        return 0
