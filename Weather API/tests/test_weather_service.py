import unittest
from unittest.mock import patch, MagicMock
from src.weather_service import get_weather, redis_client


class TestWeatherService(unittest.TestCase):
    @patch("src.weather_service.redis_client.get")
    def test_get_weather_from_cache(self, mock_redis_get):
        mock_redis_get.return_value = '{"temp":25}'
        result = get_weather("Paris")
        self.assertEqual(result["source"], "cache")
        self.assertIn("25", result["data"])

    @patch("src.weather_service.redis_client.get", return_value=None)
    @patch("src.weather_service.requests.get")
    @patch("src.weather_service.redis_client.setex")
    def test_get_weather_from_api(
        self, mock_redis_setex, mock_requests_get, mock_redis_get
    ):
        mock_redis_get.return_value = None

        mock_response = MagicMock()
        mock_response.json.return_value = {"temp": 30}
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        result = get_weather("Tokyo")
        self.assertEqual(result["source"], "api")
        self.assertIn("30", result["data"])
        mock_redis_setex.assert_called_once()

    @patch("src.weather_service.redis_client.get", return_value=None)
    @patch("src.weather_service.requests.get")
    def test_get_weather_api_error(self, mock_requests_get, mock_redis_get):
        mock_requests_get.side_effect = Exception("Network error")
        with self.assertRaises(Exception) as context:
            get_weather("InvalidCity")
        self.assertIn("Network error", str(context.exception))


if __name__ == "__main__":
    unittest.main()
