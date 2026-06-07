import unittest
import tempfile
import os
from parser.parser import Parser


def make_vm_file(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".vm", delete=False)
    f.write(content)
    f.close()
    return f.name


class TestParserFiltering(unittest.TestCase):
    def test_inline_comment_stripped(self):
        path = make_vm_file("push constant 5 // empilha 5\n")
        p = Parser(path)
        p.advance()
        self.assertEqual(p.arg2(), 5)
        os.unlink(path)

    def test_blank_lines_ignored(self):
        path = make_vm_file("\n\n\npush constant 1\n")
        p = Parser(path)
        p.advance()
        self.assertEqual(p.commandType(), "C_PUSH")
        os.unlink(path)

    def test_comment_only_lines_ignored(self):
        path = make_vm_file("// isto é um comentário\npush constant 2\n")
        p = Parser(path)
        p.advance()
        self.assertEqual(p.commandType(), "C_PUSH")
        os.unlink(path)


class TestParserCommandType(unittest.TestCase):
    def _parse_single(self, line: str) -> Parser:
        path = make_vm_file(line + "\n")
        p = Parser(path)
        p.advance()
        os.unlink(path)
        return p

    def test_arithmetic_commands(self):
        for cmd in ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"):
            with self.subTest(cmd=cmd):
                p = self._parse_single(cmd)
                self.assertEqual(p.commandType(), "C_ARITHMETIC")

    def test_push_command_type(self):
        p = self._parse_single("push constant 0")
        self.assertEqual(p.commandType(), "C_PUSH")

    def test_pop_command_type(self):
        p = self._parse_single("pop local 1")
        self.assertEqual(p.commandType(), "C_POP")


class TestParserArgs(unittest.TestCase):
    def _parse_single(self, line: str) -> Parser:
        path = make_vm_file(line + "\n")
        p = Parser(path)
        p.advance()
        os.unlink(path)
        return p

    def test_arg1_arithmetic_returns_command(self):
        p = self._parse_single("add")
        self.assertEqual(p.arg1(), "add")

    def test_arg1_push_returns_segment(self):
        p = self._parse_single("push local 3")
        self.assertEqual(p.arg1(), "local")

    def test_arg1_pop_returns_segment(self):
        p = self._parse_single("pop argument 2")
        self.assertEqual(p.arg1(), "argument")

    def test_arg2_push_returns_index(self):
        p = self._parse_single("push constant 42")
        self.assertEqual(p.arg2(), 42)

    def test_arg2_pop_returns_index(self):
        p = self._parse_single("pop temp 6")
        self.assertEqual(p.arg2(), 6)


class TestParserHasMoreCommands(unittest.TestCase):
    def test_returns_false_when_exhausted(self):
        path = make_vm_file("push constant 1\nadd\n")
        p = Parser(path)
        self.assertTrue(p.hasMoreCommands())
        p.advance()
        self.assertTrue(p.hasMoreCommands())
        p.advance()
        self.assertFalse(p.hasMoreCommands())
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()
