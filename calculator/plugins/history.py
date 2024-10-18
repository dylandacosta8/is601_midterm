import os
from calculator.command import Command  # Ensure you import Command

class HistoryCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self, subcommand: str, filename: str = None) -> None:
        """Execute a history command based on the subcommand."""
        if subcommand == "load":
            if filename is None:
                filename = input("Enter the filename to load history: ")
            self.calculator.load_new_history(filename)
        elif subcommand == "save":
            if filename is None:
                filename = input("Enter the filename to save history: ")
            # Implement a save method if needed (currently handled in Calculator)
            print("Save functionality needs implementation if not already present in Calculator.")
        elif subcommand == "clear":
            self.calculator.clear_history()
        elif subcommand == "delete":
            self.calculator.delete_last_calculation()
        elif subcommand == "show":
            if filename is not None:
                if os.path.exists(filename):
                    self.calculator.load_new_history(filename)
                    self.calculator.show_history()  # Display loaded history
                else:
                    print(f"History file '{filename}' does not exist.")
            else:
                self.calculator.show_history()  # Display in-memory history
        else:
            print("Invalid subcommand. Use load, save, clear, delete, or show.")

    def help(self) -> str:
        """Provide help information for history commands."""
        return (
            "History command: \n"
            " - load [filename]: Load history from a specified file.\n"
            " - save [filename]: Save current history to a specified file.\n"
            " - clear: Clear the current history.\n"
            " - delete: Delete the last entry from the history.\n"
            " - show [filename]: Show current history; if a filename is provided, load history from it first."
        )
