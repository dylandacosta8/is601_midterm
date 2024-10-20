import pkgutil
import importlib
from calculator.command import Command

class CommandFactory:
    # Class variable to hold command classes
    command_classes = {}

    @classmethod
    def load_command_classes(cls):
        """Load all command classes from the plugins package."""
        for loader, module_name, is_pkg in pkgutil.iter_modules(['calculator/plugins']):
            module = importlib.import_module(f"calculator.plugins.{module_name}")
            for name in dir(module):
                cls_obj = getattr(module, name)
                if isinstance(cls_obj, type) and issubclass(cls_obj, Command):
                    cls.command_classes[module_name] = cls_obj  # Store the command class by module name

    @classmethod
    def create_command(cls, command_name: str, calculator) -> Command:
        """Create an instance of the specified command."""
        if command_name in cls.command_classes:
            return cls.command_classes[command_name](calculator)  # Instantiate command
        else:
            raise ValueError(f"Unknown command: {command_name}")

# Load the command classes when the module is imported
CommandFactory.load_command_classes()
