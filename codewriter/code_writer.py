import os


class CodeWriter:
    def __init__(self, filename: str):
        self._file = open(filename, "w")
        self._base_name = os.path.splitext(os.path.basename(filename))[0]
        self._label_counter = 0
        self._current_function = ""

    def _write(self, *lines: str) -> None:
        for line in lines:
            self._file.write(line + "\n")

    def _scoped(self, label: str) -> str:
        # Escopa o label pela função atual para garantir unicidade global:
        # "funcao$label". Fora de função, vira apenas "$label".
        return f"{self._current_function}${label}"

    _SEGMENT_POINTER = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
    }

    def writePush(self, segment: str, index: int) -> None:
        if segment == "constant":
            self._write(
                f"@{index}",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            )
        elif segment in self._SEGMENT_POINTER:
            ptr = self._SEGMENT_POINTER[segment]
            self._write(
                f"@{ptr}",
                "D=M",
                f"@{index}",
                "A=D+A",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            )
        elif segment == "temp":
            self._write(
                f"@{5 + index}",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            )
        elif segment == "pointer":
            addr = 3 + index
            self._write(
                f"@{addr}",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            )
        elif segment == "static":
            self._write(
                f"@{self._base_name}.{index}",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            )

    def writeArithmetic(self, command: str) -> None:
        if command == "add":
            self._write("@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M")
        elif command == "sub":
            self._write("@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D")
        elif command == "neg":
            self._write("@SP", "A=M-1", "M=-M")
        elif command in ("eq", "gt", "lt"):
            jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
            label = command.upper()
            n = self._label_counter
            self._label_counter += 1
            self._write(
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@{label}_TRUE_{n}",
                f"D;{jump}",
                "@SP",
                "A=M-1",
                "M=0",
                f"@{label}_END_{n}",
                "0;JMP",
                f"({label}_TRUE_{n})",
                "@SP",
                "A=M-1",
                "M=-1",
                f"({label}_END_{n})",
            )
        elif command == "and":
            self._write("@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M")
        elif command == "or":
            self._write("@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M")
        elif command == "not":
            self._write("@SP", "A=M-1", "M=!M")

    def writePop(self, segment: str, index: int) -> None:
        if segment in self._SEGMENT_POINTER:
            ptr = self._SEGMENT_POINTER[segment]
            self._write(
                f"@{ptr}",
                "D=M",
                f"@{index}",
                "D=D+A",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D",
            )
        elif segment == "temp":
            self._write(
                "@SP",
                "AM=M-1",
                "D=M",
                f"@{5 + index}",
                "M=D",
            )
        elif segment == "pointer":
            self._write(
                "@SP",
                "AM=M-1",
                "D=M",
                f"@{3 + index}",
                "M=D",
            )
        elif segment == "static":
            self._write(
                "@SP",
                "AM=M-1",
                "D=M",
                f"@{self._base_name}.{index}",
                "M=D",
            )

    def writeLabel(self, label: str) -> None:
        self._write(f"({self._scoped(label)})")

    def writeGoto(self, label: str) -> None:
        self._write(f"@{self._scoped(label)}", "0;JMP")

    def writeIf(self, label: str) -> None:
        # Desempilha o topo; salta se for diferente de zero (verdadeiro).
        self._write(
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{self._scoped(label)}",
            "D;JNE",
        )

    def writeFunction(self, name: str, nLocals: int) -> None:
        # Define o escopo atual (usado pelos labels) e inicializa as
        # variaveis locais com 0, empilhando-as uma a uma.
        self._current_function = name
        self._write(f"({name})")
        for _ in range(nLocals):
            self._write("@SP", "A=M", "M=0", "@SP", "M=M+1")

    def writeReturn(self) -> None:
        # endFrame = LCL (R13); retAddr = *(endFrame - 5) (R14)
        self._write(
            "@LCL", "D=M", "@R13", "M=D",
            "@5", "A=D-A", "D=M", "@R14", "M=D",
            # *ARG = pop() -> valor de retorno no lugar do arg0
            "@SP", "AM=M-1", "D=M", "@ARG", "A=M", "M=D",
            # SP = ARG + 1
            "@ARG", "D=M+1", "@SP", "M=D",
            # restaura THAT, THIS, ARG, LCL a partir de endFrame
            "@R13", "AM=M-1", "D=M", "@THAT", "M=D",
            "@R13", "AM=M-1", "D=M", "@THIS", "M=D",
            "@R13", "AM=M-1", "D=M", "@ARG", "M=D",
            "@R13", "AM=M-1", "D=M", "@LCL", "M=D",
            # goto retAddr
            "@R14", "A=M", "0;JMP",
        )

    def close(self) -> None:
        self._file.close()
