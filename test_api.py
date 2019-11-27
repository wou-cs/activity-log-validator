import json
import os
import requests
from datetime import datetime, timezone
from dateutil.parser import parse


base_url = os.environ.get('BASE_URL', "http://localhost:5001")
log_url = base_url + "/api/activities"


def test_activities_list():
    """Verify that the activity logger returns a list of at least 1 activity."""
    try:
        r = requests.get(log_url)
        assert r.status_code == 200
        activities = json.loads(r.text)
        assert isinstance(activities, dict)
        assert len(activities["activities"]) > 0
    except requests.exceptions.RequestException:
        assert False, f"Could not connect to activity log service at {log_url}"


def test_get_single_activity():
    """Verify that we can traverse from the first entry in the list to a single item."""
    try:
        r = requests.get(log_url)
        assert r.status_code == 200
        activities = json.loads(r.text)
        single_activity = activities["activities"][0]
        assert "location" in single_activity
        item_url = base_url + single_activity["location"]
    except requests.exceptions.RequestException:
        assert False, f"Could not connect to activity log service at {log_url}"

    try:
        r = requests.get(item_url)
        assert r.status_code == 200, f"Loading: {item_url}"
        activity = json.loads(r.text)
        assert isinstance(activity, dict)
        assert "id" in activity
        assert "username" in activity
        assert "user_id" in activity
        assert "details" in activity
        assert "timestamp" in activity
    except requests.exceptions.RequestException:
        assert False, f"Could not connect to activity log service at {item_url}"


def test_add_new_activity():
    """Verify that we can create a new item and that the id and location point to it"""
    timestamp = datetime.now(timezone.utc)
    new_activity = {
        "user_id": 9,
        "username": "Paul",
        "timestamp": timestamp.isoformat(),
        "details": "Paul is alive",
    }
    try:
        r = requests.post(log_url, json=new_activity)
        assert r.status_code == 201
        reply = json.loads(r.text)
        assert "location" in reply
        assert "id" in reply
        assert reply["location"] == "/api/activities/" + reply["id"]

        # Let's check how the timestamp is formatted
        returned_timestamp = parse(reply["timestamp"])
        assert abs((timestamp-returned_timestamp).total_seconds()) < 1
    except requests.exceptions.RequestException:
        assert False, f"Could not connect to activity log service at {log_url}"
