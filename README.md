# VMTranslator

Tradutor de bytecode VM para linguagem de montagem Hack (Nand2Tetris — Projeto 7).

## Integrantes

- Amanda Maia Soares Silva — Matrícula: 20240065517
- Marcos Antonio Branco Pereira Junior — Matrícula: 20240065393

## Linguagem

Python 3.11+. Sem dependências externas (apenas stdlib).

## Como executar

**Arquivo único:**
```bash
python main.py caminho/para/arquivo.vm
```
Gera `arquivo.asm` no mesmo diretório do arquivo de entrada.

**Pasta com múltiplos arquivos `.vm`:**
```bash
python main.py caminho/para/pasta/
```
Gera `NomeDaPasta.asm` dentro da pasta, combinando todos os `.vm` encontrados.

## Exemplos

```bash
# arquivo único
python main.py input/Main.vm
# Saída: input/Main.asm

# pasta
python main.py input/Average/
# Saída: input/Average/Average.asm
```

## Testes unitários

```bash
python -m pytest tests/

# ou diretamente
python tests/test_parser.py
```
