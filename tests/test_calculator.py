"""
Unit tests for the Calculator application.

These tests cover the basic functionalities of the Calculator class, including
addition, subtraction, and history tracking. Each test utilizes fixtures to set
up a testing environment with a temporary history file.
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

def test_add(calculator):
    """Test the add function using the AddCommand."""
    command = AddCommand(calculator)
    result = command.execute(Decimal(2), Decimal(3))  # Use Decimal for operands
    assert result == Decimal(5)  # Check if the result is correct

def test_subtract(calculator):
    """Test the subtract function using the SubtractCommand."""
    command = SubtractCommand(calculator)
    result = command.execute(Decimal(5), Decimal(2))  # Use Decimal for operands
    assert result == Decimal(3)  # Check if the result is correct

def test_history(calculator):
    """Test that calculation history stores calculations correctly."""
    add_command = AddCommand(calculator)
    add_command.execute(Decimal(2), Decimal(3))  # Perform addition with Decimal
    history = calculator.get_history()  # Retrieve the calculation history
    assert len(history) == 1  # Ensure history has one entry
    assert history[0]['result'] == Decimal(5)  # Access using list indexing
