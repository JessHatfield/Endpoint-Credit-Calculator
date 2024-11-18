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

        cleaned_word = remove_non_supported_characters(text)
        cleaned_word = cleaned_word.split(' ')

        for word in cleaned_word:
            length=len(word)

            if len(word) >= 1 and len(word) <= 3:
                credit_cost += Decimal('0.1')
            elif len(word) >= 4 and len(word) <= 7:
                credit_cost += Decimal('0.2')
            elif len(word) >= 8:
                credit_cost += Decimal('0.3')

        return credit_cost


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
