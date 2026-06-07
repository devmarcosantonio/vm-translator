import os


class CodeWriter:
    def __init__(self, filename: str):
        self._file = open(filename, "w")
        self._base_name = os.path.splitext(os.path.basename(filename))[0]
        self._label_counter = 0

    def _write(self, *lines: str) -> None:
        for line in lines:
            self._file.write(line + "\n")

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

    def writePop(self, segment: str, index: int) -> None:
        pass

    def close(self) -> None:
        self._file.close()
