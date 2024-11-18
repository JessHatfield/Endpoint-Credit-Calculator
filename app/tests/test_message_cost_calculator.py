from decimal import Decimal

import pytest

from app.message_cost_calculator.message_cost_calculator import MessageCostCalculator, BaseCostRule, CharacterCountRule, \
    WordLengthMultiplierRule


def test_message_cost_calculator_applies_rules():
    text = 'my hovercraft is full of eels'

    calculator = MessageCostCalculator(calculators=[BaseCostRule()])
    assert calculator.calculate_cost(text=text) == Decimal(1)


def test_character_count_rule():
    text = 'my hovercraft is full of eels'

    assert CharacterCountRule().calculate(text=text) == Decimal('1.45')


@pytest.mark.parametrize('text,expected_cost', [
    ('cat bat', Decimal('0.2')),
    ('jeff steve jeremy jessica', Decimal('0.8')),
     ('Frenzied phlebotomist', Decimal('0.6')),
     ('cat@ stev- phlebotomist', Decimal('0.6'))]
                         )
def test_word_length_multipler_rule(text, expected_cost):
    assert WordLengthMultiplierRule().calculate(text=text) == expected_cost
