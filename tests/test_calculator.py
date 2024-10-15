"""Tests for the Calculator application.

This module contains test cases for verifying the functionality of the
Calculator class, its operations, and the integration of command plugins.
"""

import pytest
from calculator import Calculator, Calculation
from calculator.plugins import PluginManager
from calculator.plugins.divide import DivideCommand
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.multiply import MultiplyCommand

@pytest.fixture
def plugin_manager():
    """Fixture to create a PluginManager instance and load plugins."""
    manager = PluginManager()
    manager.load_plugins()
    return manager

@pytest.fixture
def calc_with_fake_data(plugin_manager, fake_data):
    """Fixture to create a Calculator instance and execute fake operations using plugins."""
    calculator = Calculator()
    Calculator.clear_history()  # Clear previous history

    for record in fake_data:
        command_instance = plugin_manager.get_command(record["operation"])
        if command_instance is None:
            raise ValueError(f"Invalid operation: {record['operation']}") #TODO

        if record["operation"] == "divide" and record["operand2"] == 0:
            with pytest.raises(ZeroDivisionError):
                command_instance.execute(record["operand1"], record["operand2"])
        else:
            command_instance.execute(record["operand1"], record["operand2"])

    return calculator

# Tests for Calculator operations
def test_add(calc_with_fake_data):
    """Test the add function using fake data."""
    for record in calc_with_fake_data.get_history():
        if record.operation == "add":
            assert record.result == record.operands[0] + record.operands[1]

def test_subtract(calc_with_fake_data):
    """Test the subtract function using fake data."""
    for record in calc_with_fake_data.get_history():
        if record.operation == "subtract":
            assert record.result == record.operands[0] - record.operands[1]

def test_multiply(calc_with_fake_data):
    """Test the multiply function using fake data."""
    for record in calc_with_fake_data.get_history():
        if record.operation == "multiply":
            assert record.result == record.operands[0] * record.operands[1]

def test_divide(calc_with_fake_data):
    """Test the divide function using fake data."""
    for record in calc_with_fake_data.get_history():
        if record.operation == "divide":
            if record.operands[1] == 0:
                continue  # Skip zero division check as it's handled in calc_with_fake_data #TODO
            assert record.result == record.operands[0] / record.operands[1]

def test_history(calc_with_fake_data):
    """Test that calculation history stores calculation instances correctly."""
    history = calc_with_fake_data.get_history()
    assert len(history) > 0  # Ensuring history is populated
    for record in history:
        assert isinstance(record, Calculation)

def test_clear_history(calc_with_fake_data):
    """Test that the clear_history method empties the calculation history."""
    calc_with_fake_data.clear_history()
    assert len(calc_with_fake_data.get_history()) == 0

def test_get_last_calculation(calc_with_fake_data):
    """Test that get_last_calculation retrieves the most recent calculation."""
    last_calc = calc_with_fake_data.get_last_calculation()
    assert last_calc is not None  # Ensuring last calculation is available
    assert isinstance(last_calc, Calculation)

def test_get_calculations_by_type(calc_with_fake_data):
    """Test that get_calculations_by_type filters history by operation type."""
    addition_calcs = calc_with_fake_data.get_calculations_by_type("add")
    assert len(addition_calcs) > 0  # Check if there are addition calculations

def test_get_last_calculation_empty_history():
    """Test that get_last_calculation raises IndexError when history is empty."""
    calculator = Calculator()
    calculator.clear_history()  # Ensuring history is cleared
    with pytest.raises(IndexError, match="No calculations in history."):
        calculator.get_last_calculation()

# New tests for Calculation methods
def test_calculation_str():
    """Test the __str__ method of the Calculation class."""
    calc = Calculation("add", [1, 2], 3)
    assert str(calc) == "Add: [1, 2] = 3"

def test_calculation_get_operands():
    """Test the get_operands method of the Calculation class."""
    calc = Calculation("subtract", [5, 3], 2)
    assert calc.get_operands() == [5, 3]

def test_calculation_get_result():
    """Test the get_result method of the Calculation class."""
    calc = Calculation("multiply", [2, 3], 6)
    assert calc.get_result() == 6

# Updated invalid input tests
@pytest.mark.parametrize("operation", ["add", "subtract", "multiply", "divide"])
def test_invalid_operand_types(plugin_manager, operation):
    """Test that invalid operand types raise ValueError."""
    with pytest.raises(ValueError, match="Operands must be numeric."):
        command_instance = plugin_manager.get_command(operation)
        if operation == "add":
            command_instance.execute("string", 2)
        elif operation == "subtract":
            command_instance.execute("string", 2)
        elif operation == "multiply":
            command_instance.execute("string", 2)
        elif operation == "divide":
            command_instance.execute("string", 2)

    with pytest.raises(ValueError, match="Operands must be numeric."):
        command_instance = plugin_manager.get_command(operation)
        if operation == "add":
            command_instance.execute(2, None)
        elif operation == "subtract":
            command_instance.execute(2, None)
        elif operation == "multiply":
            command_instance.execute(2, None)
        elif operation == "divide":
            command_instance.execute(2, None)

def test_add_help():
    """Test the help function of the AddCommand plugin."""
    command = AddCommand()
    assert command.help() == "Usage: add <value1> <value2> - Adds two numbers."

def test_subtract_help():
    """Test the help function of the SubtractCommand plugin."""
    command = SubtractCommand()
    assert command.help() == "Usage: subtract <value1> <value2> - Subtracts second number from the first."

def test_multiply_help():
    """Test the help function of the MultiplyCommand plugin."""
    command = MultiplyCommand()
    assert command.help() == "Usage: multiply <value1> <value2> - Multiplies two numbers."

def test_divide_help():
    """Test the help function of the DivideCommand plugin."""
    command = DivideCommand()
    assert command.help() == "Usage: divide <value1> <value2> - Divides first number by the second."
