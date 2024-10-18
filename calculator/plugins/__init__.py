import importlib
import pkgutil
import os
import logging

logger = logging.getLogger('calculator_app')

class PluginManager:
    def __init__(self, calculator):
        self.plugins = {}
        self.calculator = calculator

    def load_plugins(self):
        plugins_dir = "calculator.plugins"
        for module_name in self.list_command_modules(plugins_dir):
            try:
                logger.debug(f"Attempting to import module: {module_name}")
                module = importlib.import_module(f"{plugins_dir}.{module_name}")
                command_class = getattr(module, f"{module_name.capitalize()}Command")
                command_instance = command_class(self.calculator)
                self.plugins[module_name] = command_instance
                logger.info(f"Successfully loaded plugin: {module_name}")
            except Exception as e:
                logger.error(f"Failed to load command '{module_name}': {e}")

    def list_command_modules(self, package):
        try:
            command_modules = [name for _, name, _ in pkgutil.iter_modules([package.replace('.', os.sep)])]
            logger.debug(f"Found command modules: {command_modules}")
            return command_modules
        except Exception as e:
            logger.exception(f"Error listing command modules in package '{package}': {e}")
            return []

    def get_command(self, command_name):
        command = self.plugins.get(command_name)
        if command:
            logger.debug(f"Retrieved command: {command_name}")
        else:
            logger.warning(f"Command not found: {command_name}")
        return command

    def list_plugins(self):
        plugin_keys = list(self.plugins.keys())
        logger.debug(f"Listing loaded plugins: {plugin_keys}")
        return plugin_keys
