from decimal import Decimal
from calculator import Calculator, Calculation
from . import Command

class SubtractCommand(Command):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self._validate_inputs(a, b)
        result = a - b
        
        # Create and store the Calculation instance
        calculation = Calculation("subtract", [a, b], result)
        Calculator.history.append(calculation)

        return result

    def help(self) -> str:
        return "Usage: subtract <value1> <value2> - Subtracts second number from the first."

    @staticmethod
    def _validate_inputs(a, b) -> None:
        if not isinstance(a, (int, float, Decimal)) or not isinstance(b, (int, float, Decimal)):
            raise ValueError("Operands must be numeric.")
