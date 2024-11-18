import pytest
from .main import app
from fastapi.testclient import TestClient

from .models import CopilotMessages, CopilotMessage
from .utils import get_copilot_messages

client = TestClient(app)


def mock_get_copilot_messages():
    return CopilotMessages(
        messages=[
            CopilotMessage(text='Are there any rent escalation clauses?',
                           timestamp="2024-05-03T01:04:01.375Z",
                           id=1066),

            CopilotMessage(text='Generate a detailed Environmental Compliance Report',
                           timestamp="2024-05-03T21:17:32.996Z",
                           report_id=7321,
                           id=1082)
        ]

    )


def test_get_useage_report_returns_useage_report():
    """
    Mock the values returned from messages endpoint

    mock the values returned from
    :return:
    """

    app.dependency_overrides.update(
        {get_copilot_messages: mock_get_copilot_messages}
    )

    response = client.get("/tech-task/usage/")
    assert response.status_code == 200
    assert response.json() == {}
