import unittest
from src.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Personal Blog", response.data)

    def test_article_not_found(self):
        response = self.client.get("/article/99999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Article not found.", response.data)

    def test_admin_requires_login(self):
        response = self.client.get("/admin", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.headers.get("Location").lower())


if __name__ == "__main__":
    unittest.main()
