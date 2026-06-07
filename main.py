import sys
import os
from parser.parser import Parser
from codewriter.code_writer import CodeWriter


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.vm")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + ".asm"

    parser = Parser(input_file)
    writer = CodeWriter(output_file)

    while parser.hasMoreCommands():
        parser.advance()
        cmd_type = parser.commandType()

        if cmd_type == "C_ARITHMETIC":
            writer.writeArithmetic(parser.arg1())
        elif cmd_type == "C_PUSH":
            writer.writePush(parser.arg1(), parser.arg2())
        elif cmd_type == "C_POP":
            writer.writePop(parser.arg1(), parser.arg2())

    writer.close()
    print(f"Gerado: {output_file}")


if __name__ == "__main__":
    main()

