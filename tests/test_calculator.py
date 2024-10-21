"""
Unit tests for the Calculator application.

These tests cover the basic functionalities of the Calculator class, including
addition, subtraction, and history tracking. Each test utilizes fixtures to set
up a testing environment with a temporary history file and generate fake data.
"""

import os
from decimal import Decimal
import pytest
from calculator import Calculator
from calculator.plugins import PluginManager
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand

@pytest.fixture
def calculator():
    """Fixture to create a Calculator instance with a valid history file."""
    history_file = os.path.join('data', 'test_history.csv')  # Provide a test history file
    # Create an empty history file for testing purposes
    with open(history_file, 'a', encoding='utf-8'):
        pass  # Create the file if it doesn't exist

    calc = Calculator(history_file=history_file)
    yield calc
    # Cleanup the test history file after the test
    os.remove(history_file)

@pytest.fixture
def plugin_manager(calculator):
    """Fixture to create a PluginManager instance and load plugins."""
    manager = PluginManager(calculator)
    manager.load_plugins()
    return manager

def test_add(calculator, fake_data):
    """Test the add function using the AddCommand with fake data."""
    for record in fake_data:
        if record['operation'] == 'add':
            command = AddCommand(calculator)
            result = command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            assert result == Decimal(record['operand1'] + record['operand2'])  # Validate the result

def test_subtract(calculator, fake_data):
    """Test the subtract function using the SubtractCommand with fake data."""
    for record in fake_data:
        if record['operation'] == 'subtract':
            command = SubtractCommand(calculator)
            result = command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            assert result == Decimal(record['operand1'] - record['operand2'])  # Validate the result

def test_history(calculator, fake_data):
    """Test that calculation history stores calculations correctly using fake data."""
    add_command = AddCommand(calculator)

    for record in fake_data:
        if record['operation'] == 'add':
            add_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))  # Perform addition with Decimal

    history = calculator.get_history()  # Retrieve the calculation history
    expected_history_length = sum(1 for record in fake_data if record['operation'] == 'add')
    assert len(history) == expected_history_length  # Ensure history has correct entries

    # Check results for only the 'add' operations
    for record in fake_data:
        if record['operation'] == 'add':
            expected_result = Decimal(record['operand1'] + record['operand2'])
            actual_result = history.pop(0)['result']  # Use pop to ensure we get the correct entry
            print(f"Expected: {expected_result}, Actual: {actual_result}, Operand1: {record['operand1']}, Operand2: {record['operand2']}")
            assert actual_result == expected_result  # Check recorded result
