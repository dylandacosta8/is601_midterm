from calculator import Calculator
from decimal import Decimal
import logging

logger = logging.getLogger('calculator_app')

class DivideCommand:
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def execute(self, operand1: Decimal, operand2: Decimal) -> Decimal:
        """Execute the division operation and record it in history."""
        if operand2 == 0:
            logger.error("Division by zero attempted.")
            raise ZeroDivisionError("Cannot divide by zero.")
        result = operand1 / operand2
        self.calculator.add_to_history("divide", [operand1, operand2], result)
        logger.info(f"Executed Divide: {operand1} / {operand2} = {result}")
        return result

    def help(self) -> str:
        """Provide help for the Divide command."""
        return "Usage: divide <value1> <value2> - Divides first number by the second."
