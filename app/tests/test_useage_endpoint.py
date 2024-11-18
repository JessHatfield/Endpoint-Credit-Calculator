from decimal import Decimal
from unittest import mock

from .main import app
from fastapi.testclient import TestClient

from .models import CopilotMessages, CopilotMessage, HydratedCopilotMessage, HydratedCopilotMessages

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


def mock_get_report_costs_for_messages():
    return HydratedCopilotMessages(
        messages=[
            HydratedCopilotMessage(text='Are there any rent escalation clauses?',
                                   timestamp="2024-05-03T01:04:01.375Z",
                                   id=1066,
                                   cost=None),

            HydratedCopilotMessage(text='Generate a detailed Environmental Compliance Report',
                                   timestamp="2024-05-03T21:17:32.996Z",
                                   report_id=7321,
                                   id=1082,
                                   report_name='Test Report',
                                   cost=Decimal('0.1'),
                                   )
        ]

    )


def mock_calculate_cost_for_message():
    return Decimal('0.5')


def test_get_useage_report_returns_useage_report_in_correct_format():
    """
    Confirms that we can generate a response with the correct json structure
    Confirms that the useage cost for each message can be populated

    We mock out API calls to reduce execution time + ensure test is repeatable
    We mock out calculating message costs because we want to test implementation details elsewhere

    """

    with mock.patch('app.main.get_copilot_messages', return_value=mock_get_copilot_messages()):
        with mock.patch('app.main.add_report_details_for_messages', return_value=mock_get_report_costs_for_messages()):
            with mock.patch('app.main.calculate_message_cost', return_value=mock_calculate_cost_for_message()):
                response = client.get("/tech-task/usage/")
                assert response.status_code == 200
                assert response.json() == {'usage': [
                    {'credits_used': 0.5, 'message_id': 1066, 'timestamp': '2024-05-03T01:04:01.375Z'},
                    {'credits_used': 0.1, 'message_id': 1082, 'report_name': 'Test Report', 'timestamp': '2024-05-03T21:17:32.996Z'}
                ]}


def test_integration_data_fetched_and_useage_returned():

    """
    I just added this quickly, so I had some way of running the code using live data via pycharms debugger
    Given more time I'd add this to an integrations test folder and then exclude this folder from the commands used to run our test suite
    """

    response = client.get("/tech-task/usage/")
    print(response.json())