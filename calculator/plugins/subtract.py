from calculator import Calculator
from decimal import Decimal
import logging

logger = logging.getLogger('calculator_app')

class SubtractCommand:
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def execute(self, operand1: Decimal, operand2: Decimal) -> Decimal:
        """Execute the subtraction operation and record it in history."""
        result = operand1 - operand2
        self.calculator.add_to_history("subtract", [operand1, operand2], result)
        logger.info(f"Executed Subtract: {operand1} - {operand2} = {result}")
        return result

    def show_help(self) -> None:
        """Provide help for the Subtract command."""
        print("\nUsage: subtract <value1> <value2>")
        print("Description: Subtracts the second number from the first.")
