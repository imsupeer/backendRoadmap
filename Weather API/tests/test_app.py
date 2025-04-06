import unittest
from src.app import app


class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_weather_endpoint(self):
        response = self.client.get("/weather/Petrolina")
        self.assertIn(response.status_code, [200, 502])


if __name__ == "__main__":
    unittest.main()
