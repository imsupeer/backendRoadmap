import unittest
import json
from unittest.mock import patch, MagicMock
from src import github_activity


class TestGitHubActivity(unittest.TestCase):
    def test_process_event_push(self):
        event = {
            "type": "PushEvent",
            "repo": {"name": "imsupeer/backendRoadmap"},
            "payload": {"size": 3},
        }
        result = github_activity.process_event(event)
        self.assertEqual(result, "Pushed 3 commits to imsupeer/backendRoadmap")

    def test_process_event_issues(self):
        event = {
            "type": "IssuesEvent",
            "repo": {"name": "imsupeer/backendRoadmap"},
            "payload": {"action": "opened"},
        }
        result = github_activity.process_event(event)
        self.assertEqual(result, "Opened a new issue in imsupeer/backendRoadmap")

    def test_process_event_watch(self):
        event = {
            "type": "WatchEvent",
            "repo": {"name": "imsupeer/backendRoadmap"},
        }
        result = github_activity.process_event(event)
        self.assertEqual(result, "Starred imsupeer/backendRoadmap")

    @patch("src.github_activity.urllib.request.urlopen")
    def test_fetch_user_activity_success(self, mock_urlopen):
        fake_events = [
            {"type": "PushEvent", "repo": {"name": "test/repo"}, "payload": {"size": 2}}
        ]
        fake_response = MagicMock()
        fake_response.read.return_value = json.dumps(fake_events).encode("utf-8")
        fake_response.__enter__.return_value = fake_response
        mock_urlopen.return_value = fake_response

        events = github_activity.fetch_user_activity("someuser")
        self.assertEqual(events, fake_events)

    @patch(
        "src.github_activity.urllib.request.urlopen",
        side_effect=Exception("API failure"),
    )
    @patch("builtins.print")
    def test_fetch_user_activity_error(self, mock_print, mock_urlopen):
        events = github_activity.fetch_user_activity("invaliduser")
        self.assertEqual(events, [])
        mock_print.assert_any_call(
            "Error fetching activity for user invaliduser: API failure"
        )


if __name__ == "__main__":
    unittest.main()
