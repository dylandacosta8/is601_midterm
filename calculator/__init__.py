from typing import List
from decimal import Decimal
import logging

logger = logging.getLogger('calculator_app')

class Calculation:
    def __init__(self, operation: str, operands: List[Decimal], result: Decimal):
        self.operation = operation
        self.operands = operands
        self.result = result
        logger.debug(f"Calculation created: {self.operation} with operands {self.operands} = {self.result}")

    def __str__(self) -> str:
        return f"{self.operation.capitalize()}: {self.operands} = {self.result}"

    def get_operands(self) -> List[Decimal]:
        return self.operands

    def get_result(self) -> Decimal:
        return self.result

class Calculator:
    history: List[Calculation] = []

    def __init__(self) -> None:
        pass

    def _add_to_history(self, operation: str, operands: List[Decimal], result: Decimal) -> None:
        calc = Calculation(operation, operands, result)
        Calculator.history.append(calc)
        logger.info(f"Added to history: {operation} with result {result}")

    @classmethod
    def get_history(cls) -> List[Calculation]:
        logger.debug(f"Fetching history: {cls.history}")
        return cls.history

    @classmethod
    def clear_history(cls) -> None:
        logger.info("Clearing history.")
        cls.history.clear()

    @classmethod
    def get_last_calculation(cls) -> Calculation:
        if cls.history:
            logger.debug("Retrieving last calculation.")
            return cls.history[-1]
        else:
            logger.warning("No calculations in history.")
            raise IndexError("No calculations in history.")

    @classmethod
    def get_calculations_by_type(cls, operation: str) -> List[Calculation]:
        filtered_calculations = [calc for calc in cls.history if calc.operation == operation]
        logger.debug(f"Filtered calculations by type '{operation}': {filtered_calculations}")
        return filtered_calculations
