# tests/test_api_client.py
import unittest
from unittest.mock import patch, Mock
from src.api_client import APIClient, APIClientError

class TestAPIClient(unittest.TestCase):

    @patch("src.api_client.requests.Session.get")
    def test_case_1_fetch_posts_success(self, mock_get):
        """Test Case 1: Successful fetch of posts"""

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{"id": 1, "title": "ok"}]
        mock_get.return_value = mock_resp

        client = APIClient(base_url="https://jsonplaceholder.typicode.com", timeout=1, max_retries=1)

        posts = client.fetch_posts()

        print("Test Case 1 Passed: Successfully fetched posts")

        self.assertEqual(posts[0]["id"], 1)

    @patch("src.api_client.requests.Session.get")
    def test_case_2_invalid_json(self, mock_get):
        """Test Case 2: Invalid JSON handling"""

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_resp

        client = APIClient(base_url="https://jsonplaceholder.typicode.com", timeout=1, max_retries=1)

        try:
            client.fetch_posts()
        except APIClientError:
            print("Test Case 2 Passed: Invalid JSON correctly raised APIClientError")
            return

        self.fail("APIClientError was not raised")

if __name__ == "__main__":
    unittest.main()
