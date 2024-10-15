''' Conftest file for Faker '''
import random
from faker import Faker
import pytest

# Initialize Faker
fake = Faker()

# Custom command line option for pytest
def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption("--num_records", action="store", default=0, type=int,
                     help="Number of records to generate using Faker.")

# Fixture to generate fake data
@pytest.fixture(scope='session')
def fake_data(request):
    """Generate fake data for calculator operations."""
    num_records = request.config.getoption("--num_records")
    records = []

    for _ in range(num_records):
        # Generate a fake record for calculator operations
        record = {
            "operation": random.choice(['add', 'subtract', 'multiply', 'divide']),
            "operand1": random.choice([fake.random_number(digits=2), 0]),
            "operand2": random.choice([fake.random_number(digits=2), 0])
        }
        records.append(record)

    return records
