# VMTranslator

Tradutor de bytecode VM para linguagem de montagem Hack (Nand2Tetris — Projeto 7).

## Integrantes

- Amanda Maia Soares Silva — Matrícula: 20240065517
- Marcos Antonio Branco Pereira Junior — Matrícula: 20240065393

## Linguagem

Python 3.11+. Sem dependências externas (apenas stdlib).

## Como executar

```bash
python main.py caminho/para/arquivo.vm
```

Gera: `caminho/para/arquivo.asm`

## Exemplo

```bash
python main.py projects/07/MemoryAccess/BasicTest/BasicTest.vm
# Saída: projects/07/MemoryAccess/BasicTest/BasicTest.asm
```

## Validação no CPUEmulator

1. Abrir o CPUEmulator do Nand2Tetris
2. Carregar o script `.tst` correspondente ao teste
3. Executar — resultado esperado: `Comparison ended successfully.`

Testes obrigatórios:
- `StackArithmetic/SimpleAdd/SimpleAdd.vm`
- `MemoryAccess/BasicTest/BasicTest.vm`

## Testes unitários

```bash
python -m pytest tests/
```
