import pandas as pd
from decimal import Decimal
import logging
import os
import csv

logger = logging.getLogger('calculator_app')

class Calculator:
    def __init__(self, history_file: str = "history.csv"):
        self.history_file = history_file
        self.history = self.load_history()  # Load history on initialization
        logger.info(f"Initial history loaded: {self.history}")  # Log the loaded history for debugging

    def add_to_history(self, operation: str, operands: list, result: Decimal) -> None:
        """Add a calculation to the history and save it to the file."""
        new_entry = pd.DataFrame({
            "operation": [operation],
            "operands": [str(operands)],  # Store as string for easier CSV handling
            "result": [result]
        })
        # Append the new entry to the CSV file directly
        new_entry.to_csv(self.history_file, mode='a', index=False, header=not os.path.isfile(self.history_file))
        self.history = self.load_history()  # Refresh the in-memory history
        logger.info(f"Added to history: {operation} with operands {operands} = {result}")

    def load_history(self) -> pd.DataFrame:
        """Load history from a CSV file."""
        if os.path.isfile(self.history_file):
            try:
                loaded_history = pd.read_csv(self.history_file)
                if {'operation', 'operands', 'result'}.issubset(loaded_history.columns):
                    loaded_history['operands'] = loaded_history['operands'].apply(eval)  # Convert strings back to lists
                    logger.info(f"History loaded from {self.history_file}")
                    return loaded_history
                else:
                    logger.error(f"Invalid history file format: {self.history_file}")
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
        else:
            logger.warning(f"No history file found: {self.history_file}. Starting with empty history.")
        
        return pd.DataFrame(columns=["operation", "operands", "result"])  # Return empty DataFrame if loading fails

    def clear_history(self) -> None:
        """Clear the calculation history by deleting the history file."""
        if os.path.isfile(self.history_file):
            os.remove(self.history_file)
            logger.info(f"Cleared history by deleting file: {self.history_file}")
            self.history = pd.DataFrame(columns=["operation", "operands", "result"])  # Reset history DataFrame
        else:
            logger.warning(f"Attempted to clear non-existent history file: {self.history_file}")

    def delete_last_calculation(self) -> None:
        """Delete the last calculation from history in the CSV file."""
        if os.path.isfile(self.history_file):
            with open(self.history_file, 'r') as file:
                lines = file.readlines()
            if len(lines) > 1:  # Ensure there's something to delete (skip header)
                # Remove the last line (the last calculation)
                with open(self.history_file, 'w') as file:
                    file.writelines(lines[:-1])  # Write back all lines except the last one
                logger.info(f"Deleted the last calculation from {self.history_file}")
            else:
                logger.warning("Attempted to delete from a history file with only header.")
        else:
            logger.warning(f"Attempted to delete from non-existent history file: {self.history_file}")

    def show_history(self) -> None:
        """Print the current history in a user-friendly format."""
        if not os.path.isfile(self.history_file) or os.stat(self.history_file).st_size == 0:
            print("No history recorded.")
            return

        print("\nCurrent History:")
        print(f"{'Index':<6} {'Operation':<15} {'Operand 1':<15} {'Operand 2':<15} {'Result':<10}")  # Header
        print("=" * 80)  # Separator line

        try:
            with open(self.history_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row

                for index, row in enumerate(reader, start=1):
                    operation, operands, result = row
                    operand_list = eval(operands)  # Convert string back to list
                    operand1 = operand_list[0] if len(operand_list) > 0 else ''
                    operand2 = operand_list[1] if len(operand_list) > 1 else ''
                    
                    # Print formatted output without the Decimal type
                    print(f"{index:<6} {operation:<15} {operand1:<15} {operand2:<15} {result:<10}")  # Formatted output

        except Exception as e:
            logger.error(f"Failed to read history: {e}")
            print("Error reading history.")
        
        print("")

    def load_new_history(self, new_filename: str) -> None:
        """Load a new history from a specified CSV file."""
        if os.path.isfile(new_filename):
            loaded_history = pd.read_csv(new_filename)
            if {'operation', 'operands', 'result'}.issubset(loaded_history.columns):
                loaded_history['operands'] = loaded_history['operands'].apply(eval)  # Convert strings back to lists
                loaded_history.to_csv(self.history_file, index=False)  # Save the loaded history to the default history file
                self.history = loaded_history
                logger.info(f"New history loaded from {new_filename}")
            else:
                logger.error(f"Invalid history file format: {new_filename}")
        else:
            logger.error(f"No such file: {new_filename}")
