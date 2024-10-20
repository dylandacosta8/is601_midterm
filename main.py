import os
import logging
import concurrent.futures
from calculator.plugins import PluginManager
from calculator import Calculator
from decimal import Decimal
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the environment variable (now ENV instead of ENVIRONMENT)
environment = os.getenv('ENV', 'prod').lower()

# Set the logging format with a timestamp
log_format = "%(asctime)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Configure logging to write to a file called calc.log in the same directory
log_file = 'calc.log'

# Configure logging based on environment, writing to a file
if environment == 'dev':
    logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format, filename=log_file, filemode='a')
elif environment == 'uat':
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format, filename=log_file, filemode='a')
else:  # 'prod'
    logging.basicConfig(level=logging.WARNING, format=log_format, datefmt=date_format, filename=log_file, filemode='a')

# REPL function
def repl():
    # Prompt the user to load a history file or use the default 'history.csv'
    user_history_file = input("Enter the history file to load (press Enter for 'history.csv'): ").strip()

    if not user_history_file:
        user_history_file = "history.csv"  # Default to 'history.csv'

    # Initialize the Calculator with the specified or default history file
    calculator = Calculator(history_file=user_history_file)
    
    # Initialize the PluginManager and load plugins
    plugin_manager = PluginManager(calculator)
    plugin_manager.load_plugins()

    # Display menu function
    def display_menu():
        logging.debug("Displaying available plugins")
        print("\nAvailable plugins:")
        for command in plugin_manager.list_plugins():
            print(f" - {command}")
        print("\nExample input: add 5 3 or history load history.csv")

    # Display the menu when the application starts
    display_menu()

    while True:
        # Print the currently active history file
        print(f"\n[Active history file: {calculator.active_history_file}]")

        user_input = input("\nEnter command (e.g., add 5 3) or 'menu' to see options or 'exit' to quit: ").strip().lower()

        if user_input == "exit":
            logging.info("User exited the application.")
            print("Exiting the calculator. Goodbye!")
            break
        elif user_input == "menu":
            display_menu()
            continue

        try:
            parts = user_input.split()
            operation = parts[0]

            # Handle history subcommands
            if operation == "history" and len(parts) > 1:
                history_command = parts[1]
                command_instance = plugin_manager.get_command("history")
                if command_instance:
                    if history_command == "load" and len(parts) == 3:
                        filename = parts[2]
                        command_instance.execute("load", filename)  # Call history.load
                    elif history_command == "save" and len(parts) == 3:
                        filename = parts[2]
                        command_instance.execute("save", filename)  # Call history.save
                    elif history_command == "clear":
                        command_instance.execute("clear")  # Call history.clear
                    elif history_command == "delete":
                        command_instance.execute("delete")  # Call history.delete
                    elif history_command == "show":
                        command_instance.execute("show")  # Call history.show
                    else:
                        print("Invalid history command. Type 'menu' to see available options.")
                else:
                    print("History command not found.")
                continue

            # Convert values to Decimal for arithmetic operations
            values = [Decimal(value) for value in parts[1:]] if len(parts) > 1 else []

            # Check if the operation is valid
            command_instance = plugin_manager.get_command(operation)
            if command_instance is None:
                logging.warning(f"Invalid operation attempted: {operation}")
                print("Invalid operation. Type 'menu' to see available plugins.")
                continue

            # Execute the command in a separate process
            with concurrent.futures.ProcessPoolExecutor() as executor:
                future = executor.submit(command_instance.execute, *values)
                result = future.result()  # This will block until the result is available

            logging.debug(f"Operation '{operation}' executed with result: {result}")
            print(f"Result: {result}")

        except ValueError:
            logging.error("Invalid input provided.")
            print("Invalid input. Please enter valid numbers and an operation.")
        except ZeroDivisionError:
            logging.error("Division by zero attempted.")
            print("Error: Division by zero.")
        except Exception as e:
            logging.exception(f"An error occurred during command execution: {e}")
            print(f"An error occurred: {e}")

# Starting the REPL
if __name__ == "__main__":
    repl()

