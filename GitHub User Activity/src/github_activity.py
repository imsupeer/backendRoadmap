import sys
import urllib.request
import json
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

GIT_ACCESS_TOKEN = os.environ.get("GIT_ACCESS_TOKEN")


def fetch_user_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    req = urllib.request.Request(
        url,
        headers={
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {GIT_ACCESS_TOKEN}",
        },
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = response.read().decode("utf-8")
            events = json.loads(data)
            return events
    except Exception as e:
        print(f"Error fetching activity for user {username}: {str(e)}")
        traceback.print_exc()
        return []


def process_event(event):
    event_type = event.get("type", "")
    repo = event.get("repo", {}).get("name", "unknown repository")
    if event_type == "PushEvent":
        commits = event.get("payload", {}).get("size", 0)
        return f"Pushed {commits} commits to {repo}"
    elif event_type == "IssuesEvent":
        action = event.get("payload", {}).get("action", "")
        if action == "opened":
            return f"Opened a new issue in {repo}"
        else:
            return f"Issue {action} in {repo}"
    elif event_type == "WatchEvent":
        return f"Starred {repo}"
    else:
        return f"{event_type} event in {repo}"


def main():
    if len(sys.argv) < 2:
        print("Use command: github-activity <username>")
        sys.exit(1)
    username = sys.argv[1]
    events = fetch_user_activity(username)
    if not events:
        print("No activity found or an error occurred.")
        return
    for event in events:
        output = process_event(event)
        print(output)


if __name__ == "__main__":
    main()
