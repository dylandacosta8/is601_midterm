import pandas as pd
from decimal import Decimal
import logging
import os

logger = logging.getLogger('calculator_app')

class Calculator:
    def __init__(self, history_file: str = None):

        self.history_file = history_file
        self.active_history_file = self.history_file  # Track the currently active file
        if os.path.isfile(self.history_file) and os.path.getsize(self.history_file) > 0:
            # If file exists and is not empty, load history from it
            self.history = self.load_history(self.history_file)
            logger.info(f"History loaded from {self.history_file}")
        else:
            # Otherwise, start with an empty history
            self.history = pd.DataFrame(columns=["operation", "operands", "result"])
            logger.info(f"Starting with empty history, no valid file found at {self.history_file}")
        self.new_entries = []  # Keep track of new entries added during the session

    def add_to_history(self, operation: str, operands: list, result: Decimal) -> None:
        """Add a calculation to the history and save it to the active history file."""
        new_entry = {
            "operation": operation,
            "operands": str(operands),  # Store as string for easier CSV handling
            "result": result
        }
        # Append the new entry to the history DataFrame
        self.history = pd.concat([self.history, pd.DataFrame([new_entry])], ignore_index=True)
        
        # Also append to the new_entries list to track this session's new additions
        self.new_entries.append(new_entry)
        
        logger.info(f"Added to history: {operation} with operands {operands} = {result}")
        self.save_history()  # Save only the new entry

    def save_history(self) -> None:
        """Save only new entries to the active history file."""
        if self.new_entries:  # If there are new entries to save
            new_entries_df = pd.DataFrame(self.new_entries)
            if not os.path.isfile(self.active_history_file):
                new_entries_df.to_csv(self.active_history_file, mode='w', index=False)
                logger.info(f"History saved to new file: {self.active_history_file}")
            else:
                # Append only the new entries to the active history file
                new_entries_df.to_csv(self.active_history_file, mode='a', index=False, header=False)
                logger.info(f"New entries appended to {self.active_history_file}")
            
            # Clear the new entries after saving
            self.new_entries.clear()

    def load_history(self, new_filename: str = None) -> pd.DataFrame:
        """Load history from a new file or the active file."""
        if new_filename:

            if "data" in new_filename:
                full_path = new_filename
            else:
                full_path = os.path.join('data', new_filename)

            if os.path.isfile(full_path):
                self.active_history_file = full_path
                logger.info(f"Switched to history file: {self.active_history_file}")
                # Load new history and reset current history
                loaded_history = pd.read_csv(full_path)
                self.history = loaded_history
                return loaded_history
            else:
                logger.error(f"History file '{full_path}' does not exist.")
                return pd.DataFrame(columns=["operation", "operands", "result"])
        
        # Load from the active history file
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
            self.save_as_new_file(self.active_history_file)  # Save updated history to active file
        else:
            logger.warning("Attempted to delete from empty history.")

    def show_history(self) -> None:
        """Print the current history in a user-friendly format."""
        # Load history from the active file
        self.history = self.load_history(self.active_history_file)
        
        if self.history.empty:
            print("No history recorded.")
            return

        # Split operands into operand1 and operand2 columns for display purposes
        try:
            display_history = self.history.copy()
            display_history[['operand1', 'operand2']] = pd.DataFrame(
                display_history['operands'].apply(lambda op: eval(op) if isinstance(op, str) else op).tolist(),
                index=display_history.index
            )
        except Exception as e:
            logger.error(f"Failed to process operands for display: {e}")
            print("Error processing history data.")
            return

        # Display the formatted history
        print("\nCurrent History:")
        print(f"{'Index':<5} {'Operation':<15} {'Operand1':<10} {'Operand2':<10} {'Result':<10}")
        print("=" * 60)
        for index, row in display_history.iterrows():
            print(f"{index + 1:<5} {row['operation']:<15} {row['operand1']:<10} {row['operand2']:<10} {row['result']:<10}")
        print("")

    def save_as_new_file(self, new_filename: str) -> None:
        """Save a copy of the current history to a new file."""

        self.history = self.load_history(self.active_history_file)
        
        if self.history.empty:
            print("No history to save.")
            return
        else:
            # Ensure the directory exists; if not, create it
            os.makedirs('data', exist_ok=True)
        
            # Combine the directory with the new filename
            full_path = os.path.join('data', new_filename)
        
            # Ensure only the necessary columns are saved
            history_to_save = self.history[['operation', 'operands', 'result']]
            history_to_save.to_csv(full_path, mode='w', index=False)
            logger.info(f"History saved as a copy to {full_path}")
