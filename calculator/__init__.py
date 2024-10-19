import pandas as pd 
from decimal import Decimal
import logging
import os
import shutil  # for copying files

logger = logging.getLogger('calculator_app')

class Calculator:
    def __init__(self, history_file: str = "history.csv"):
        self.history_file = history_file
        self.active_history_file = self.history_file  # Track the currently active file
        self.history = self.load_history()  # Load history on initialization
        logger.info(f"Initial history loaded from {self.active_history_file}")

    def add_to_history(self, operation: str, operands: list, result: Decimal) -> None:
        """Add a calculation to the history and save it to the active history file."""
        new_entry = pd.DataFrame({
            "operation": [operation],
            "operands": [str(operands)],  # Store as string for easier CSV handling
            "result": [result]
        })
        self.history = pd.concat([self.history, new_entry], ignore_index=True)  # Allow duplicates
        logger.info(f"Added to history: {operation} with operands {operands} = {result}")
        self.save_history()  # Save immediately after adding

    def save_history(self) -> None:
        """Save the current history DataFrame to the active CSV file."""
        if not self.history.empty:
            history_to_save = self.history[['operation', 'operands', 'result']]  # Only save these columns
            if not os.path.isfile(self.active_history_file):
                history_to_save.to_csv(self.active_history_file, mode='w', index=False)
                logger.info(f"History saved to new file: {self.active_history_file}")
            else:
                # Append new entries to the active history file instead of overwriting
                history_to_save.to_csv(self.active_history_file, mode='a', index=False, header=False)
                logger.info(f"New history appended to {self.active_history_file}")

    def load_history(self, new_filename: str = None) -> pd.DataFrame:
        """Load history from a new file or the active file."""
        if new_filename:
            if os.path.isfile(new_filename):
                self.active_history_file = new_filename  # Switch to the new file
                logger.info(f"Switched to history file: {self.active_history_file}")
                # Load new history and reset current history
                loaded_history = pd.read_csv(new_filename)
                self.history = loaded_history
                return loaded_history
            else:
                logger.error(f"History file '{new_filename}' does not exist.")
                return pd.DataFrame(columns=["operation", "operands", "result"])
        
        if os.path.isfile(self.active_history_file):
            try:
                loaded_history = pd.read_csv(self.active_history_file)
                logger.info(f"History loaded from {self.active_history_file}")
                self.history = loaded_history  # Update current history
                return loaded_history
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
        else:
            logger.warning(f"No history file found: {self.active_history_file}. Starting with empty history.")
            return pd.DataFrame(columns=["operation", "operands", "result"])

    def clear_history(self) -> None:
        """Clear the calculation history by deleting the active file."""
        if os.path.isfile(self.active_history_file):
            os.remove(self.active_history_file)
            logger.info(f"Cleared history by deleting file: {self.active_history_file}")
            self.history = pd.DataFrame(columns=["operation", "operands", "result"])  # Reset history DataFrame
        else:
            logger.warning(f"Attempted to clear non-existent history file: {self.active_history_file}")

    def delete_last_calculation(self) -> None:
        """Delete the last calculation from history and save the updated history to the active file."""
        if not self.history.empty:
            last_entry = self.history.iloc[-1]
            self.history = self.history.iloc[:-1]  # Drop last row using iloc
            logger.info(f"Deleted last calculation: {last_entry['operation']} with operands {last_entry['operands']} = {last_entry['result']}")
            self.save_history()  # Save updated history to active file
        else:
            logger.warning("Attempted to delete from empty history.")

    def show_history(self) -> None:
        """Print the current history in a user-friendly format."""
        # Load history from the active file
        self.history = self.load_history(self.active_history_file)  # Always read from the active history file
        if self.history.empty:
            print("No history recorded.")
            return

        # Split operands into operand1 and operand2 columns for display purposes
        display_history = self.history.copy()
        display_history[['operand1', 'operand2']] = pd.DataFrame(
            display_history['operands'].apply(lambda op: eval(op) if isinstance(op, str) else op).tolist(),
            index=display_history.index
        )

        # Display the formatted history
        print("\nCurrent History:")
        print(f"{'Index':<5} {'Operation':<15} {'Operand1':<10} {'Operand2':<10} {'Result':<10}")
        print("=" * 60)
        for index, row in display_history.iterrows():
            print(f"{index + 1:<5} {row['operation']:<15} {row['operand1']:<10} {row['operand2']:<10} {row['result']:<10}")
        print("")

    def save_as_new_file(self, new_filename: str) -> None:
        """Save a copy of the current history to a new file."""
        history_to_save = self.history[['operation', 'operands', 'result']]  # Ensure only these columns are saved
        history_to_save.to_csv(new_filename, mode='w', index=False)
        logger.info(f"History saved as a copy to {new_filename}")
