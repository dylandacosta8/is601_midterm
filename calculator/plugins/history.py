import os
from calculator.command import Command

class HistoryCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self, subcommand: str, filename: str = None) -> None:
        """Execute a history command based on the subcommand."""
        # Check if subcommand is 'help' and display relevant help
        if subcommand == "help":
            self.show_help()  # Show general help for the history command
            return
        
        # Execute based on subcommand
        if subcommand == "load":
            if filename is None:
                filename = input("Enter the filename to load history: ")
            self.calculator.load_history(filename)
        elif subcommand == "save":
            if filename is None:
                filename = input("Enter the filename to save history: ")
            self.calculator.save_as_new_file(filename)
        elif subcommand == "clear":
            self.calculator.clear_history()
        elif subcommand == "delete":
            self.calculator.delete_last_calculation()
        elif subcommand == "show":
            if filename is not None:
                if os.path.exists(filename):
                    self.calculator.load_history(filename)
                    self.calculator.show_history()
                else:
                    print(f"History file '{filename}' does not exist.")
            else:
                self.calculator.show_history()
        else:
            print("Invalid subcommand. Use load, save, clear, delete, or show.")

    def show_help(self) -> None:
        """Provide help information for history commands."""
        print(
            "\nHistory command help: \n"
            "Usage: history <subcommand> [<filename>]\n"
            " - load <filename>: Load history from a specified file and set it as the active file.\n"
            " - save <filename>: Save a copy of the current history to a new file.\n"
            " - clear: Clear the current history in the active file.\n"
            " - delete: Delete the last entry from the active history.\n"
            " - show [filename]: Show the current history or load history from the specified file first."
        )
