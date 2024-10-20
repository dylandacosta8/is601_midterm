import os
from calculator.command import Command  # Ensure you import Command

class HistoryCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self, subcommand: str, filename: str = None) -> None:
        """Execute a history command based on the subcommand."""
        if subcommand == "load":
            # Load new history file as the active file
            if filename is None:
                filename = input("Enter the filename to load history: ")
            self.calculator.load_history(filename)  # Switch to new file
        elif subcommand == "save":
            if filename is None:
                filename = input("Enter the filename to save history: ")
            self.calculator.save_as_new_file(filename)
        elif subcommand == "clear":
            # Clear history in the active file
            self.calculator.clear_history()
        elif subcommand == "delete":
            # Delete the last calculation from history
            self.calculator.delete_last_calculation()
        elif subcommand == "show":
            # Show the current or specified history
            if filename is not None:
                if os.path.exists(filename):
                    self.calculator.load_history(filename)  # Load new history file
                    self.calculator.show_history()  # Display loaded history
                else:
                    print(f"History file '{filename}' does not exist.")
            else:
                self.calculator.show_history()  # Display the current active history
        else:
            print("Invalid subcommand. Use load, save, clear, delete, or show.")

    def help(self) -> str:
        """Provide help information for history commands."""
        return (
            "History command: \n"
            " - load <filename>: Load history from a specified file and set it as the active file.\n"
            " - save <filename>: Save a copy of the current history to a new file.\n"
            " - clear: Clear the current history in the active file.\n"
            " - delete: Delete the last entry from the active history.\n"
            " - show [filename]: Show the current history; if a filename is provided, load history from it first."
        )
