"""
Unit tests for the Calculator application.

These tests cover the basic functionalities of the Calculator class, including
addition, subtraction, multiplication, division, and history tracking. Each test utilizes fixtures to set
up a testing environment with a temporary history file and generate fake data.
"""

import os
from decimal import Decimal
import pytest
from calculator import Calculator
from calculator.plugins import PluginManager
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.divide import DivideCommand
from calculator.plugins.multiply import MultiplyCommand

@pytest.fixture
def calculator():
    """Fixture to create a Calculator instance with a valid history file."""
    history_file = os.path.join('data', 'test_history.csv')  # Provide a test history file

    # Create the data directory if it does not exist
    os.makedirs('data', exist_ok=True)

    # Create an empty history file for testing purposes if it doesn't exist
    if not os.path.exists(history_file):
        with open(history_file, 'w', encoding='utf-8'):
            pass  # Create the file

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
    add_command = AddCommand(calculator)

    for record in fake_data:
        if record['operation'] == 'add':
            result = add_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            expected_result = Decimal(record['operand1']) + Decimal(record['operand2'])
            assert result == expected_result, f"Expected {expected_result} but got {result}"  # Validate the result

def test_subtract(calculator, fake_data):
    """Test the subtract function using the SubtractCommand with fake data."""
    subtract_command = SubtractCommand(calculator)

    for record in fake_data:
        if record['operation'] == 'subtract':
            result = subtract_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            expected_result = Decimal(record['operand1']) - Decimal(record['operand2'])
            assert result == expected_result, f"Expected {expected_result} but got {result}"  # Validate the result

def test_multiply(calculator, fake_data):
    """Test multiplication using the MultiplyCommand with fake data."""
    multiply_command = MultiplyCommand(calculator)

    for record in fake_data:
        if record['operation'] == 'multiply':
            result = multiply_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            expected_result = Decimal(record['operand1']) * Decimal(record['operand2'])
            assert result == expected_result, f"Expected {expected_result} but got {result}"  # Validate the result

def test_divide(calculator, fake_data):
    """Test division using the DivideCommand with fake data."""
    divide_command = DivideCommand(calculator)

    for record in fake_data:
        if record['operation'] == 'divide' and Decimal(record['operand2']) != 0:
            result = divide_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            expected_result = Decimal(record['operand1']) / Decimal(record['operand2'])
            # Compare with a tolerance for floating point precision issues
            assert abs(result - expected_result) < Decimal('0.0001'), f"Expected {expected_result} but got {result}"

def test_history(calculator, fake_data):
    """Test that calculation history stores calculations correctly using fake data."""
    add_command = AddCommand(calculator)

    for record in fake_data:
        if record['operation'] == 'add':
            add_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))  # Perform addition

    history = calculator.get_history()  # Retrieve the calculation history
    expected_history_length = sum(1 for record in fake_data if record['operation'] == 'add')
    assert len(history) == expected_history_length, f"Expected history length {expected_history_length} but got {len(history)}"

    # Check results for only the 'add' operations
    for record in fake_data:
        if record['operation'] == 'add':
            expected_result = Decimal(record['operand1']) + Decimal(record['operand2'])
            actual_result = history.pop(0)['result']  # Use pop to ensure we get the correct entry
            assert actual_result == expected_result, f"Expected {expected_result} but got {actual_result}"  # Check recorded result
