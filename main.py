import os
import logging
import concurrent.futures
from calculator.plugins import PluginManager
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
    # Initialize the PluginManager and load plugins
    plugin_manager = PluginManager()
    plugin_manager.load_plugins()

    # Display menu function
    def display_menu():
        logging.debug("Displaying available plugins")
        print("\nAvailable plugins:")
        for command in plugin_manager.list_plugins():
            print(f" - {command}")
        print("\nExample input: add 5 3")

    # Display the menu when the application starts
    display_menu()

    while True:
        user_input = input("\nEnter command (e.g., add 5 3) or 'menu' to see options or 'exit' to quit: ").strip().lower()

        if user_input == "exit":
            logging.info("User exited the application.")
            print("Exiting the calculator. Goodbye!")
            break
        elif user_input == "menu":
            display_menu()
            continue

        try:
            operation, value1, value2 = user_input.split()

            # Convert values to Decimal
            value1 = Decimal(value1)
            value2 = Decimal(value2)

            # Check if the operation is valid
            command_instance = plugin_manager.get_command(operation)
            if command_instance is None:
                logging.warning(f"Invalid operation attempted: {operation}")
                print("Invalid operation. Type 'menu' to see available plugins.")
                continue

            # Execute the command in a separate process
            with concurrent.futures.ProcessPoolExecutor() as executor:
                future = executor.submit(command_instance.execute, value1, value2)
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
