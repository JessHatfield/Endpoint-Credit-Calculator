from abc import ABC
from decimal import Decimal
from typing import List

from app.message_cost_calculator.text_utils import remove_non_supported_characters


class CalculatorRule(ABC):

    def calculate(self, text: str) -> Decimal:
        pass


class BaseCostRule(CalculatorRule):
    def calculate(self, text: str) -> Decimal:
        return Decimal(1)


class CharacterCountRule(CalculatorRule):
    def calculate(self, text: str) -> Decimal:
        return Decimal(f'{len(text)}') * Decimal('0.05')


class WordLengthMultiplierRule(CalculatorRule):
    def calculate(self, text: str) -> Decimal:
        credit_cost = Decimal(0)
        # Refactored this logic to its own function, I suspect we will be reusing it
        cleaned_word = remove_non_supported_characters(text)
        cleaned_word = cleaned_word.split(' ')

        for word in cleaned_word:

            if 1 <= len(word) <= 3:
                credit_cost += Decimal('0.1')
            elif 4 <= len(word) <= 7:
                credit_cost += Decimal('0.2')
            elif len(word) >= 8:
                credit_cost += Decimal('0.3')

        return credit_cost


class AnyThirdCharacterIsVowelRule(CalculatorRule):
    def calculate(self, text: str) -> Decimal:
        """
        The task specification does not provide a definition of Character
        I've just taken this to mean any character including spaces
        If we just wanted to limit this to alphabetical characters we could do via the remove_non_supported_characters util
        """
        vowels = ['a', 'e', 'i', 'o', 'u']

        credit_cost = Decimal(0)

        cleaned_text = text.lower()

        count = 1
        for character in cleaned_text:

            if count % 3 == 0 and character in vowels:
                credit_cost += Decimal('0.3')

            count += 1

        return credit_cost


class LengthPenaltyRule(CalculatorRule):
    def calculate(self, text: str) -> Decimal:
        if len(text) > 100:
            return Decimal(5)
        return Decimal(0)


class MessageCostCalculator:
    """
    We use a strategy pattern here to keep cost calculation
        -Extendable
        -Easier to understand
        -Easier to test
    """

    def __init__(self, calculators: List[CalculatorRule]):
        self.__calculator_rules = calculators

    def calculate_cost(self, text):
        cost = Decimal(0)

        for rule in self.__calculator_rules:
            cost += rule.calculate(text)

        return cost
