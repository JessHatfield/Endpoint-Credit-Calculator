from decimal import Decimal

import pytest

from app.message_cost_calculator.message_cost_calculator import MessageCostCalculator, BaseCostRule, CharacterCountRule, \
    WordLengthMultiplierRule, AnyThirdCharacterIsVowelRule, LengthPenaltyRule, UniqueWordRule


def test_message_cost_calculator_applies_rules():
    text = ('This is an example string which is definitely longer than 100 characters. Octopus Octopus Octopus Octopus '
            'Octopus')
    # We get a cost of 5 from the length rule and then 1 from the base cost rule
    calculator = MessageCostCalculator(calculators=[BaseCostRule(), LengthPenaltyRule()])
    assert calculator.calculate_cost(text=text) == Decimal(6)


@pytest.mark.parametrize('text,expected_cost', [
    ('Jeffrey Bezos', Decimal('1')),  # Not a palindrome so no multiplier is applied
    ('Warsaw@ Was Raw', Decimal('2')),  # After processing this is a palindrome

]
                         )
def test_message_cost_calculator_doubles_score_when_text_is_palindrome(text, expected_cost):
    calculator = MessageCostCalculator(calculators=[BaseCostRule()])
    assert calculator.calculate_cost(text=text) == expected_cost


def test_character_count_rule():
    text = 'my hovercraft is full of eels'  #29 characters long 0.05 credits per character
    assert CharacterCountRule().calculate(text=text) == Decimal('1.45')


@pytest.mark.parametrize('text,expected_cost', [
    ('cat bat', Decimal('0.2')),
    ('jeff steve jeremy jessica', Decimal('0.8')),
    ('Frenzied phlebotomist', Decimal('0.6')),
    ('cat@ stev- phlebotomist', Decimal('0.6'))]
                         )
def test_word_length_multipler_rule(text, expected_cost):
    assert WordLengthMultiplierRule().calculate(text=text) == expected_cost


@pytest.mark.parametrize('text,expected_cost', [
    ('cba cEb', Decimal('0.6')),
    #Third character is vowel and sixth character is vowel, We count all characters including spaces
    ('12345E', Decimal('0.3')),  #Sixth character is vowel, we count all characters
    ('ahg', Decimal('0'))  # No chracters are vowels
]
                         )
def test_third_vowel_rule(text, expected_cost):
    assert AnyThirdCharacterIsVowelRule().calculate(text=text) == expected_cost


@pytest.mark.parametrize('text,expected_cost', [(
        'This is an example string which is definitely longer than 100 characters. Octopus Octopus Octopus Octopus Octopus',
        Decimal(5)),
    ('I am a tiny little string', Decimal(0))])
def test_length_penalty_rule(text, expected_cost):
    assert LengthPenaltyRule().calculate(text=text) == expected_cost


@pytest.mark.parametrize('text,existing_cost,expected_cost', [
    ('Jeffrey Bezos', Decimal(5), Decimal('-2')),  # All words are unique
    ('Jeffrey jeffrey', Decimal(5), Decimal('-2')),  # All words are unique taking into case
    ('Bezo Bezo eggplant', Decimal(5), Decimal(0)),  # The words are not unique
    ('Jeffrey Bezos', Decimal(2), Decimal(1)),  # All words are unique and expected_cost is capped
]
                         )
def test_unique_word_rule(text, existing_cost, expected_cost):
    assert UniqueWordRule().calculate(text=text, current_cost=existing_cost) == expected_cost
