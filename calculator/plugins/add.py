from calculator import Calculator
from decimal import Decimal
import logging

logger = logging.getLogger('calculator_app')

class AddCommand:
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def execute(self, operand1: Decimal, operand2: Decimal) -> Decimal:
        """Execute the addition operation and record it in history."""
        result = operand1 + operand2
        self.calculator.add_to_history("add", [operand1, operand2], result)
        logger.info(f"Executed Add: {operand1} + {operand2} = {result}")
        return result

    def show_help(self) -> None:
        """Provide help for the Add command."""
        print("\nUsage: add <value1> <value2>")
        print("Description: Adds two numbers.")
