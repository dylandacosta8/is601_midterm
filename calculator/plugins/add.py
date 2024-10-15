from decimal import Decimal
from calculator import Calculator, Calculation
from . import Command

class AddCommand(Command):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self._validate_inputs(a, b)
        result = a + b
        
        # Create a Calculation instance and store it in the history
        calculation = Calculation("add", [a, b], result)
        Calculator.history.append(calculation)  # Assuming Calculator.history is accessible

        return result

    def help(self) -> str:
        return "Usage: add <value1> <value2> - Adds two numbers."

    @staticmethod
    def _validate_inputs(a, b) -> None:
        if not isinstance(a, (int, float, Decimal)) or not isinstance(b, (int, float, Decimal)):
            raise ValueError("Operands must be numeric.")
