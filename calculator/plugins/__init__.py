import importlib
import pkgutil
import os
import logging

from abc import ABC, abstractmethod

logger = logging.getLogger('calculator_app')

class Command(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass #TODO

    @abstractmethod
    def help(self):
        pass #TODO

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self):
        # Path to the plugins directory
        plugins_dir = "calculator.plugins"

        # Automatically discover and load command plugins
        for module_name in self.list_command_modules(plugins_dir):
            try:
                # Import the module
                logger.debug(f"Attempting to import module: {module_name}")
                module = importlib.import_module(f"{plugins_dir}.{module_name}")

                # Get the command class (assumed to be named <ModuleName>Command)
                command_class = getattr(module, f"{module_name.capitalize()}Command")
                command_instance = command_class()

                # Use the module name as the command key
                self.plugins[module_name] = command_instance
                logger.info(f"Successfully loaded plugin: {module_name}")
            except Exception as e: #TODO
                logger.error(f"Failed to load command '{module_name}': {e}") #TODO

    def list_command_modules(self, package):
        # Returns a list of command modules in the specified package
        try:
            command_modules = [name for _, name, _ in pkgutil.iter_modules([package.replace('.', os.sep)])]
            logger.debug(f"Found command modules: {command_modules}")
            return command_modules
        except Exception as e: #TODO
            logger.exception(f"Error listing command modules in package '{package}': {e}") #TODO
            return [] #TODO

    def get_command(self, command_name):
        command = self.plugins.get(command_name)
        if command:
            logger.debug(f"Retrieved command: {command_name}")
        else:
            logger.warning(f"Command not found: {command_name}") #TODO
        return command

    def list_plugins(self): 
        plugin_keys = list(self.plugins.keys()) #TODO
        logger.debug(f"Listing loaded plugins: {plugin_keys}") #TODO
        return plugin_keys #TODO
