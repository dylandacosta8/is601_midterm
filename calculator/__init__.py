from typing import List
from decimal import Decimal
import logging
import pandas as pd

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
    def __init__(self):
        # Initialize a DataFrame to hold history
        self.history = pd.DataFrame(columns=["operation", "operands", "result"])

    def add_to_history(self, operation: str, operands: list, result: Decimal) -> None:
        """Add a calculation to the history."""
        self.history = self.history.append({"operation": operation, "operands": operands, "result": result}, ignore_index=True)

    def save_history(self, filename: str) -> None:
        """Save history to a CSV file."""
        self.history.to_csv(filename, index=False)

    def load_history(self, filename: str) -> None:
        """Load history from a CSV file."""
        try:
            self.history = pd.read_csv(filename)
        except FileNotFoundError:
            print(f"No such file: {filename}")

    def clear_history(self) -> None:
        """Clear the calculation history."""
        self.history = pd.DataFrame(columns=["operation", "operands", "result"])

    def delete_last_calculation(self) -> None:
        """Delete the last calculation from history."""
        if not self.history.empty:
            self.history = self.history[:-1]
