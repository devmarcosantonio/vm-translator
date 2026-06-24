import sys
import os
from parser.parser import Parser
from codewriter.code_writer import CodeWriter


def translate(vm_file: str, writer: CodeWriter) -> None:
    # Define o prefixo das variaveis static a partir do nome do arquivo.
    writer.setFileName(os.path.splitext(os.path.basename(vm_file))[0])
    parser = Parser(vm_file)
    while parser.hasMoreCommands():
        parser.advance()
        cmd_type = parser.commandType()
        if cmd_type == "C_ARITHMETIC":
            writer.writeArithmetic(parser.arg1())
        elif cmd_type == "C_PUSH":
            writer.writePush(parser.arg1(), parser.arg2())
        elif cmd_type == "C_POP":
            writer.writePop(parser.arg1(), parser.arg2())
        elif cmd_type == "C_LABEL":
            writer.writeLabel(parser.arg1())
        elif cmd_type == "C_GOTO":
            writer.writeGoto(parser.arg1())
        elif cmd_type == "C_IF":
            writer.writeIf(parser.arg1())
        elif cmd_type == "C_FUNCTION":
            writer.writeFunction(parser.arg1(), parser.arg2())
        elif cmd_type == "C_CALL":
            writer.writeCall(parser.arg1(), parser.arg2())
        elif cmd_type == "C_RETURN":
            writer.writeReturn()


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.vm")
        print("     python main.py pasta/")
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isdir(path):
        vm_files = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.endswith(".vm")
        ]
        if not vm_files:
            print(f"Nenhum arquivo .vm encontrado em: {path}")
            sys.exit(1)

        # Um unico .asm com o nome da pasta, contendo bootstrap + todos os .vm.
        dir_name = os.path.basename(os.path.normpath(path))
        output_file = os.path.join(path, dir_name + ".asm")
        writer = CodeWriter(output_file)
        writer.writeInit()
        for vm_file in sorted(vm_files):
            translate(vm_file, writer)
        writer.close()
        print(f"Gerado: {output_file}")

    else:
        # Arquivo unico: gera .asm de mesmo nome, sem bootstrap (preserva Parte 1).
        output_file = os.path.splitext(path)[0] + ".asm"
        writer = CodeWriter(output_file)
        translate(path, writer)
        writer.close()
        print(f"Gerado: {output_file}")


if __name__ == "__main__":
    main()
