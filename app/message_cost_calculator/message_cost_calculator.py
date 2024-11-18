from abc import ABC
from decimal import Decimal
from typing import List


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
        return

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
