import os


class CodeWriter:
    def __init__(self, filename: str):
        self._file = open(filename, "w")
        self._base_name = os.path.splitext(os.path.basename(filename))[0]

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

    def writePop(self, segment: str, index: int) -> None:
        pass

    def close(self) -> None:
        self._file.close()
