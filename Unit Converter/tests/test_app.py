import unittest
from src.app import unitConversorApp


class TestAppServer(unittest.TestCase):
    def setUp(self):
        unitConversorApp.testing = True
        self.client = unitConversorApp.test_client()

    def test_length_page(self):
        response = self.client.get("/length")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Length Converter", response.data)
        self.assertIn(b'<link rel="stylesheet"', response.data)
        self.assertIn(b"style.css", response.data)

    def test_weight_page(self):
        response = self.client.get("/weight")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Weight Converter", response.data)
        self.assertIn(b'<link rel="stylesheet"', response.data)
        self.assertIn(b"style.css", response.data)

    def test_temperature_page(self):
        response = self.client.get("/temperature")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Temperature Converter", response.data)
        self.assertIn(b'<link rel="stylesheet"', response.data)
        self.assertIn(b"style.css", response.data)

    def test_static_css_served(self):
        response = self.client.get("/static/style.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"body {", response.data)


if __name__ == "__main__":
    unittest.main()
