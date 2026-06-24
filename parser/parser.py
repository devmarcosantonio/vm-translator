ARITHMETIC_COMMANDS = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}


class Parser:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            lines = f.readlines()

        self._commands = []
        for line in lines:
            line = line.split("//")[0].strip()
            if line:
                self._commands.append(line)

        self._index = -1
        self._current = None

    def hasMoreCommands(self) -> bool:
        return self._index < len(self._commands) - 1

    def advance(self) -> None:
        self._index += 1
        self._current = self._commands[self._index].split()

    def commandType(self) -> str:
        cmd = self._current[0]
        if cmd in ARITHMETIC_COMMANDS:
            return "C_ARITHMETIC"
        elif cmd == "push":
            return "C_PUSH"
        elif cmd == "pop":
            return "C_POP"
        elif cmd == "label":
            return "C_LABEL"
        elif cmd == "goto":
            return "C_GOTO"
        elif cmd == "if-goto":
            return "C_IF"
        elif cmd == "function":
            return "C_FUNCTION"
        elif cmd == "call":
            return "C_CALL"
        elif cmd == "return":
            return "C_RETURN"

    def arg1(self) -> str:
        # Não deve ser chamado para C_RETURN (comando sem argumentos).
        # C_ARITHMETIC retorna o próprio comando; os demais retornam o
        # primeiro argumento (segmento, label ou nome da função).
        if self.commandType() == "C_ARITHMETIC":
            return self._current[0]
        return self._current[1]

    def arg2(self) -> int:
        # Índice (push/pop), nLocals (function) ou nArgs (call).
        return int(self._current[2])
