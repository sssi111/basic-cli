import unittest
from src.parser import ParseError, Parser, ParsedInput

class TestParser(unittest.TestCase):
    def test_parse_simple_command(self):
        parser = Parser()
        result = parser.parse("echo hello world")
        self.assertEqual(len(result.commands), 1)
        self.assertEqual(result.commands[0].command_name, "echo")
        self.assertEqual(result.commands[0].args, ["hello", "world"])

    def test_parse_empty_input(self):
        parser = Parser()
        with self.assertRaises(expected_exception=ParseError):
            parser.parse("")

    def test_parse_quoted_arguments(self):
        parser = Parser()
        result = parser.parse("echo 'hello world'")
        self.assertEqual(result.commands[0].args, ["hello world"])
        
    def test_parse_double_quoted_arguments(self):
        parser = Parser()
        result = parser.parse('echo "hello world"')
        self.assertEqual(result.commands[0].args, ["hello world"])
    
    def test_parse_exit_command(self):
        parser = Parser()
        result = parser.parse('exit')
        self.assertEqual(len(result.commands), 1)
        self.assertEqual(result.commands[0].command_name, "exit")
        self.assertEqual(result.commands[0].args, [])
        
    def test_parse_wc_command(self):
        parser = Parser()
        result = parser.parse('wc abc.txt')
        self.assertEqual(len(result.commands), 1)
        self.assertEqual(result.commands[0].command_name, "wc")
        self.assertEqual(result.commands[0].args, ["abc.txt"])
    
    def test_parse_unknown_command(self):
        parser = Parser()
        result = parser.parse('unknown_command with unknown arguments')
        self.assertEqual(len(result.commands), 1)
        self.assertEqual(result.commands[0].command_name, "unknown_command")
        self.assertEqual(result.commands[0].args, ["with", "unknown", "arguments"])