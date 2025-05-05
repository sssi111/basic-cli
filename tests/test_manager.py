import unittest
from unittest.mock import patch
from io import StringIO
import sys
from src.manager import CLIManager


class TestCLIManager(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input')
    def test_session_flow(self, mock_input):
        mock_input.side_effect = ["echo test", "exit"]
        manager = CLIManager()
        manager.start()
        output = self.held_output.getvalue()
        self.assertIn("test", output)
        self.assertIn("Exit code: 0", output)
        self.assertIn("`exit` received, closing...", output)

    @patch('builtins.input')
    def test_exit_command(self, mock_input):
        mock_input.side_effect = ["exit"]
        manager = CLIManager()
        manager.start()
        output = self.held_output.getvalue()
        self.assertIn("`exit` received, closing...", output)

    @patch('builtins.input')
    def test_unknown_command(self, mock_input):
        mock_input.side_effect = ["unknown_command", "exit"]
        manager = CLIManager()
        manager.start()
        output = self.held_output.getvalue()
        self.assertIn("unknown_command: command not found", output)
        self.assertIn("Exit code: 1", output)
