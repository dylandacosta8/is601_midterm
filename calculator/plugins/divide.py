from decimal import Decimal
from calculator import Calculator, Calculation
from . import Command

class DivideCommand(Command):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self._validate_inputs(a, b)
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        
        result = a / b
        
        # Create and store the Calculation instance
        calculation = Calculation("divide", [a, b], result)
        Calculator.history.append(calculation)

        return result

    def help(self) -> str:
        return "Usage: divide <value1> <value2> - Divides first number by the second."

    @staticmethod
    def _validate_inputs(a, b) -> None:
        if not isinstance(a, (int, float, Decimal)) or not isinstance(b, (int, float, Decimal)):
            raise ValueError("Operands must be numeric.")
