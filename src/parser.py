import shlex
from typing import List

class ParsedCommand:
	"""Class representing a parsed command.

    Attributes:
        command_name (str): The name of the command.
        args (List[str]): List of command arguments.
    """
	def __init__(self, command_name: str, args: List[str]):
		self.command_name = command_name
		self.args = args

class ParsedInput:
	"""Class representing parsed user input.

    Attributes:
        commands (List[ParsedCommand]): List of parsed commands.
    """
	def __init__(self, commands: List[ParsedCommand]):
		self.commands = commands

class ParseError(Exception):
    """Custom exception for command parsing errors"""
    pass

class Parser:
	"""Class for parsing user input into a structured format."""

	def _parse_command(self, input: str) ->	ParsedCommand:
		"""Internal method to parse a string into a command and arguments.

        Uses shlex.split to properly handle quotes and spaces.

        Args:
            input (str): User input string (e.g., "cmd 'arg 1' arg2").

        Returns:
            ParsedCommand: Object containing the command and its arguments.
        """
		# Split input while respecting quotes and escaping
		args: List[str] = shlex.split(input)

		if len(args) == 0:
			raise ParseError("Empty command")

		# Extract command name (first element)
		command_name: str = args.pop(0)
		return ParsedCommand(command_name=command_name, args=args)

	def parse(self, input: str) -> ParsedInput:	
		"""Main method to parse user input.

        Args:
            input (str): Input string to parse.

        Returns:
            ParsedInput: Object containing parsed commands.
            
        Note:
            Current implementation assumes single-command input.
        """
		return ParsedInput(commands=[self._parse_command(input=input)])
