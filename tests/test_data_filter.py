# tests/test_data_filter.py
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

    def test_case_3_filter_posts_user(self):
        res = filter_posts(POSTS, user_id=1)
        print("Test Case 3 Passed: filter_posts filtered by user_id correctly")
        self.assertEqual(len(res), 2)

    def test_case_4_filter_posts_search(self):
        res = filter_posts(POSTS, search="python")
        print("Test Case 4 Passed: filter_posts search filtering works")
        self.assertEqual(res[0]["id"], 2)

    def test_case_5_get_post_by_id(self):
        p = get_post_by_id(POSTS, 2)
        print("Test Case 5 Passed: get_post_by_id returned correct post")
        self.assertEqual(p["title"], "Another")

    def test_case_6_filter_users(self):
        res = filter_users(USERS, search="ali")
        print("Test Case 6 Passed: filter_users search worked")
        self.assertEqual(res[0]["id"], 1)

if __name__ == "__main__":
    unittest.main()
