from setuptools import setup, find_packages

setup(
    name='calculator',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'calculator.plugins': [
            'add = calculator.plugins.add:AddCommand',
            'subtract = calculator.plugins.subtract:SubtractCommand',
            'multiply = calculator.plugins.multiply:MultiplyCommand',
            'divide = calculator.plugins.divide:DivideCommand',
        ],
    },
)
