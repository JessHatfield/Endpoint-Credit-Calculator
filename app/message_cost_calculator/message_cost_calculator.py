from abc import ABC
from decimal import Decimal
from typing import List




class CalculatorRule(ABC):

    def calculate(self, message: str) -> Decimal:
        pass


class BaseCostRule(CalculatorRule):
    def calculate(self, message: str) -> Decimal:
        return Decimal(1)


class MessageCostCalculator:

    def __init__(self, calculators: List[CalculatorRule]):
        self.__calculator_rules = calculators

    def calculate_cost(self, text):
        cost = Decimal(0)

        for rule in self.__calculator_rules:
            cost += rule.calculate(text)

        return cost
