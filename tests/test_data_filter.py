
import unittest
from src.data_filter import filter_posts, get_post_by_id, filter_users

POSTS = [
    {"id": 1, "userId": 1, "title": "Hello World", "body": "First post"},
    {"id": 2, "userId": 2, "title": "Another", "body": "Second post about Python"},
    {"id": 3, "userId": 1, "title": "Search Me", "body": "Contains keyword"},
]

USERS = [
    {"id": 1, "name": "Alice", "username": "alice"},
    {"id": 2, "name": "Bob", "username": "bobby"},
]

class TestDataFilter(unittest.TestCase):
    def test_filter_posts_user(self):
        res = filter_posts(POSTS, user_id=1)
        self.assertEqual(len(res), 2)

    def test_filter_posts_search(self):
        res = filter_posts(POSTS, search="python")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["id"], 2)

    def test_get_post_by_id(self):
        p = get_post_by_id(POSTS, 2)
        self.assertIsNotNone(p)
        self.assertEqual(p["title"], "Another")

    def test_filter_users(self):
        res = filter_users(USERS, search="ali")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["id"], 1)

if __name__ == "__main__":
    unittest.main()
