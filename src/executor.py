from typing import List
from src.commands import CommandRegistry
from src.parser import ParsedInput


class Executor:
    """Handles execution of parsed commands using registered command implementations."""
    def __init__(self):
        """Initialize the executor with a command registry."""
        self.registry = CommandRegistry()

    def execute(self, commands: ParsedInput) -> int:
        """
        Execute a sequence of parsed commands and return the final exit code.
        
        Args:
            commands: ParsedInput object containing commands to execute
            
        Returns:
            int: Exit code from the last executed command (0 for success, non-zero for errors)
        """
        exit_code: int = 0
        
		# Execute each command in sequence
        for command in commands.commands:
            # Get appropriate command implementation from registry
            cmd_obj = self.registry.get_command(command.command_name)
            
			# Execute command and store exit code
            exit_code = cmd_obj.execute(command=command)
        return exit_code
