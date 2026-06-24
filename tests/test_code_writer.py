import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from codewriter.code_writer import CodeWriter


def run(action) -> list:
    """Cria um CodeWriter em arquivo temporario, executa `action(cw)`,
    fecha e devolve as linhas do .asm gerado."""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".asm", delete=False)
    f.close()
    cw = CodeWriter(f.name)
    action(cw)
    cw.close()
    with open(f.name) as out:
        lines = out.read().splitlines()
    os.unlink(f.name)
    return lines


class TestControlFlow(unittest.TestCase):
    def test_label_uses_scoped_name(self):
        def act(cw):
            cw._current_function = "Main.main"
            cw.writeLabel("LOOP")
        self.assertEqual(run(act), ["(Main.main$LOOP)"])

    def test_goto_uses_scoped_name(self):
        def act(cw):
            cw._current_function = "Main.main"
            cw.writeGoto("LOOP")
        self.assertEqual(run(act), ["@Main.main$LOOP", "0;JMP"])

    def test_if_goto_pops_and_jumps_not_equal(self):
        def act(cw):
            cw._current_function = "Main.main"
            cw.writeIf("LOOP")
        self.assertEqual(
            run(act),
            ["@SP", "AM=M-1", "D=M", "@Main.main$LOOP", "D;JNE"],
        )


class TestFunction(unittest.TestCase):
    def test_function_label_and_sets_current_function(self):
        captured = {}

        def act(cw):
            cw.writeFunction("Sys.init", 0)
            captured["fn"] = cw._current_function

        lines = run(act)
        self.assertEqual(lines[0], "(Sys.init)")
        self.assertEqual(captured["fn"], "Sys.init")

    def test_function_initializes_locals_with_zero(self):
        def act(cw):
            cw.writeFunction("Foo.bar", 2)
        lines = run(act)
        # label + 2 blocos de 5 linhas para inicializar locais com 0
        self.assertEqual(lines[0], "(Foo.bar)")
        self.assertEqual(lines[1:], ["@SP", "A=M", "M=0", "@SP", "M=M+1"] * 2)

    def test_function_without_locals_only_label(self):
        def act(cw):
            cw.writeFunction("Sys.init", 0)
        self.assertEqual(run(act), ["(Sys.init)"])


class TestCall(unittest.TestCase):
    def test_call_generates_unique_return_labels(self):
        def act(cw):
            cw.writeCall("Math.mult", 2)
            cw.writeCall("Math.mult", 2)
        lines = run(act)
        self.assertIn("@Math.mult$ret.0", lines)
        self.assertIn("(Math.mult$ret.0)", lines)
        self.assertIn("@Math.mult$ret.1", lines)
        self.assertIn("(Math.mult$ret.1)", lines)

    def test_call_repositions_arg(self):
        def act(cw):
            cw.writeCall("Math.mult", 2)
        lines = run(act)
        # ARG = SP - 5 - nArgs -> com nArgs=2, usa @7
        self.assertIn("@7", lines)

    def test_call_saves_frame_and_jumps(self):
        def act(cw):
            cw.writeCall("Foo.bar", 0)
        lines = run(act)
        for ptr in ("@LCL", "@ARG", "@THIS", "@THAT"):
            self.assertIn(ptr, lines)
        self.assertIn("@Foo.bar", lines)
        self.assertIn("0;JMP", lines)


class TestReturn(unittest.TestCase):
    def test_return_contains_key_steps(self):
        lines = run(lambda cw: cw.writeReturn())
        self.assertIn("@LCL", lines)   # endFrame = LCL
        self.assertIn("@R13", lines)   # endFrame temp
        self.assertIn("@R14", lines)   # retAddr temp
        self.assertEqual(lines[-1], "0;JMP")  # goto retAddr


class TestBootstrap(unittest.TestCase):
    def test_init_sets_sp_and_calls_sys_init(self):
        lines = run(lambda cw: cw.writeInit())
        self.assertEqual(lines[:4], ["@256", "D=A", "@SP", "M=D"])
        self.assertIn("@Sys.init", lines)
        self.assertIn("(Sys.init$ret.0)", lines)


class TestStaticFileName(unittest.TestCase):
    def test_set_filename_changes_static_prefix(self):
        def act(cw):
            cw.setFileName("Foo")
            cw.writePush("static", 3)
        self.assertEqual(run(act)[0], "@Foo.3")


if __name__ == "__main__":
    unittest.main()
