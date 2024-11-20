import httpx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_all_messages_in_current_period_are_in_our_response():
    response = httpx.get("https://owpublic.blob.core.windows.net/tech-task/messages/current-period")
    initial_messages = response.json()

    response = client.get("/tech-task/usage/")
    useage_data = response.json()

    # We can't the accuracy of our message cost calculation here without first manually calculating the cost per message
    # We instead try to ensure our message cost calculator is accurate via extensive unit testing
    for count, message in enumerate(initial_messages['messages']):
        assert message['id'] == useage_data['usage'][count]['message_id']
        assert message['timestamp'] == useage_data['usage'][count]['timestamp']
