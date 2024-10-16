from calculator import Calculator
from . import Command  # Ensure you import Command

class HistoryCommand(Command):
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def execute(self, subcommand: str, filename: str = None):
        if subcommand == "load":
            if filename is None:
                filename = input("Enter the filename to load history: ")
            self.calculator.load_history(filename)
        elif subcommand == "save":
            if filename is None:
                filename = input("Enter the filename to save history: ")
            self.calculator.save_history(filename)
        elif subcommand == "clear":
            self.calculator.clear_history()
        elif subcommand == "delete":
            self.calculator.delete_last_calculation()
        elif subcommand == "show":
            self.show_history()  # Call the show_history method
        else:
            print("Invalid subcommand. Use load, save, clear, delete, or show.")

    def show_history(self):
        """Print the current history in a user-friendly format."""
        '''if self.calculator.history.empty:
            print("No history recorded.")
        else:
            print("\nCurrent History:")
            for index, row in self.calculator.history.iterrows():
                print(f"{index + 1}: {row['operation']} with operands {row['operands']} = {row['result']}")
            print("")  # Add a new line for better formatting'''
        print(self.calculator.history)

    def help(self):
        return "History command: load, save, clear, delete, show"
