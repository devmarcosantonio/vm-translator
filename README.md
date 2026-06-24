# VMTranslator

Tradutor de bytecode VM para linguagem de montagem Hack (Nand2Tetris — Projetos 7 e 8).

## Integrantes

- Amanda Maia Soares Silva — Matrícula: 20240065517
- Marcos Antonio Branco Pereira Junior — Matrícula: 20240065393

## Linguagem

Python 3.11+. Sem dependências externas (apenas stdlib).

## Funcionalidades

**Parte 1 — Aritmética e acesso à memória**
- Operações aritméticas: `add`, `sub`, `neg`
- Operações lógicas: `and`, `or`, `not`
- Comparações: `eq`, `gt`, `lt` (com labels únicos)
- `push` / `pop` nos segmentos: `constant`, `local`, `argument`, `this`, `that`,
  `temp`, `pointer`, `static`

**Parte 2 — Controle de fluxo e sub-rotinas**
- Controle de fluxo: `label`, `goto`, `if-goto` (labels escopados por `função$label`)
- Sub-rotinas: `function`, `call`, `return` (com salvamento/restauração de frame)
- Código de **bootstrap** (`SP = 256` + chamada a `Sys.init`)
- Suporte a múltiplos arquivos `.vm` concatenados em um único `.asm`

## Como executar

**Arquivo único:**
```bash
python main.py caminho/para/arquivo.vm
```
Gera `arquivo.asm` no mesmo diretório do arquivo de entrada. **Não** inclui o
código de bootstrap (útil para os testes de `ProgramFlow` e `SimpleFunction`,
que rodam sem `Sys.init`).

**Pasta com múltiplos arquivos `.vm`:**
```bash
python main.py caminho/para/pasta/
```
Gera um **único** `.asm` com o nome da pasta (ex.: `NestedCall/` → `NestedCall.asm`),
contendo o **bootstrap** seguido da tradução de todos os `.vm` da pasta. É o modo
exigido pelos testes completos do Projeto 8 (ex.: `NestedCall`).

## Exemplos

```bash
# arquivo único (sem bootstrap)
python main.py input/Seven/Main.vm
# Saída: input/Seven/Main.asm

# pasta (um .asm único com bootstrap)
python main.py input/Square/
# Saída: input/Square/Square.asm
```

### Exemplo de saída (controle de fluxo)

Entrada VM (dentro de `function Main.main`):
```
label LOOP
goto LOOP
if-goto END
```

Assembly Hack gerado:
```asm
(Main.main$LOOP)
@Main.main$LOOP
0;JMP
@SP
AM=M-1
D=M
@Main.main$END
D;JNE
```

## Testes unitários

```bash
python -m unittest discover tests
```

Os testes cobrem o `Parser` (classificação de comandos e extração de argumentos)
e o `CodeWriter` (controle de fluxo, funções, `call`, `return` e bootstrap).

## Validação no CPUEmulator (Projeto 8)

Para validar a corretude funcional, traduza os diretórios de teste do pacote
oficial Nand2Tetris (`projects/08`) e compare a saída no **CPUEmulator** com os
arquivos `.cmp`:

| Teste | Foco |
| --- | --- |
| `ProgramFlow/BasicLoop` | `label`, `goto`, `if-goto` |
| `ProgramFlow/FibonacciSeries` | controle de fluxo com lógica |
| `FunctionCalls/SimpleFunction` | `function` / `return` |
| `FunctionCalls/NestedCall` | bootstrap + call/return aninhados |
