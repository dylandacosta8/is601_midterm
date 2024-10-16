from typing import List
from decimal import Decimal
import logging
import pandas as pd

logger = logging.getLogger('calculator_app')

class Calculator:
    def __init__(self):
        # Initialize a DataFrame to hold history
        self.history = pd.DataFrame(columns=["operation", "operands", "result"])

    def add_to_history(self, operation: str, operands: list, result: Decimal) -> None:
        """Add a calculation to the history."""
        new_entry = pd.DataFrame({"operation": [operation], "operands": [operands], "result": [result]})
        self.history = pd.concat([self.history, new_entry], ignore_index=True)
        logger.info(f"Added to history: {operation} with operands {operands} = {result}")

    def save_history(self, filename: str) -> None:
        """Save history to a CSV file."""
        self.history.to_csv(filename, index=False)
        logger.info(f"History saved to {filename}")

    def load_history(self, filename: str) -> None:
        """Load history from a CSV file."""
        try:
            self.history = pd.read_csv(filename)
            logger.info(f"History loaded from {filename}")
        except FileNotFoundError:
            logger.error(f"No such file: {filename}")

    def clear_history(self) -> None:
        """Clear the calculation history."""
        self.history = pd.DataFrame(columns=["operation", "operands", "result"])
        logger.info("Calculation history cleared")

    def delete_last_calculation(self) -> None:
        """Delete the last calculation from history."""
        if not self.history.empty:
            last_entry = self.history.iloc[-1]
            self.history = self.history[:-1]
            logger.info(f"Deleted last calculation: {last_entry['operation']} with operands {last_entry['operands']} = {last_entry['result']}")
        else:
            logger.warning("Attempted to delete from empty history")
