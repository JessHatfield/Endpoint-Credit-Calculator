from decimal import Decimal

import pytest

from app.message_cost_calculator.message_cost_calculator import MessageCostCalculator, BaseCostRule


def test_message_cost_calculator_applies_rules():
    text = 'my hovercraft is full of eels'

    calculator = MessageCostCalculator(calculators=[BaseCostRule()])
    assert calculator.calculate_cost(text=text) == Decimal(1)
