import unittest
import os
import tempfile
import io
from unittest.mock import patch
from src.commands import *

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"line1\nline2\nline3")
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_echo_command(self, mock_stdout):
        cmd = EchoCommand()
        exit_code = cmd.execute(ParsedCommand("echo", ["test"]))
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_stdout.getvalue().strip(), "test")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cat_command(self, mock_stdout):
        cmd = CatCommand()
        exit_code = cmd.execute(ParsedCommand("cat", [self.temp_file.name]))
        self.assertEqual(exit_code, 0)
        self.assertIn("line1", mock_stdout.getvalue())
        self.assertIn("line2", mock_stdout.getvalue())
        self.assertIn("line3", mock_stdout.getvalue())
        self.assertNotIn("line4", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_wc_command(self, mock_stdout):
        cmd = WcCommand()
        exit_code = cmd.execute(ParsedCommand("wc", [self.temp_file.name]))
        self.assertEqual(exit_code, 0)
        expected_lines = 3
        expected_words = 3
        expected_bytes = 3 * 5 + 2
        expected = f"{expected_lines} {expected_words} {expected_bytes}"
        self.assertEqual(mock_stdout.getvalue().strip(), expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pwd_command(self, mock_stdout):
        cmd = PwdCommand()
        exit_code = cmd.execute(ParsedCommand("pwd", []))
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_stdout.getvalue().strip(), os.getcwd())

    def test_exit_command(self):
        cmd = ExitCommand()
        with self.assertRaises(ExitCommandException):
            cmd.execute(ParsedCommand("exit", []))
            
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_default_command(self, mock_stdout):
        cmd = DefaultCommand()
        exit_code = cmd.execute(ParsedCommand("head", [self.temp_file.name, "-n", "1"]))
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_stdout.getvalue().strip(), "line1")  
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_other_default_command(self, mock_stdout):
        cmd = DefaultCommand()
        exit_code = cmd.execute(ParsedCommand("tail", [self.temp_file.name, "-n", "1"]))
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_stdout.getvalue().strip(), "line3")  
