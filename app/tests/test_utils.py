from decimal import Decimal

import pytest

from app.models import HydratedCopilotMessage
from app.utils import calculate_message_cost


def test_calculate_message_cost_works_with_real_message():
    """
    Following rules applied

    Base cost of 1
	3.9 after character count
	5.4 after third vowel count
	7.2 after length penalty
	-2 from unique word rule
	final result is 5.2
    """

    message = HydratedCopilotMessage(text='Are there any restrictions on alterations or improvements?',
                                     timestamp='2024-04-29T03:25:03.613Z',
                                     id=1001,
                                     report_id=None,
                                     cost=None,
                                     report_name=None)

    assert calculate_message_cost(message=message) == Decimal('5.20')


def test_calculate_message_cost_works_with_empty_string():
    """
        Following rules applied

        Base cost of 1

        """

    message = HydratedCopilotMessage(text='',
                                     timestamp='2024-04-29T03:25:03.613Z',
                                     id=1001,
                                     report_id=None,
                                     cost=None,
                                     report_name=None)

    assert calculate_message_cost(message=message) == Decimal('1')
