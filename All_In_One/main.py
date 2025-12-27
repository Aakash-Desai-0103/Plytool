from lexer import lexer
from parser import parser
import config  # <-- use config for syntax_error flag
print("--- C++ Language 5-Construct Parser ---")
print("--- (Declarations, Arrays, If/Else, Func-Decl, Func-Def) ---")
print("Type 'exit' to quit.")
def multiline_input(prompt='C++-Code > '):
    """Allow multi-line C code input until a blank line or 'exit'."""
    lines = []
    while True:
        line = input(prompt if not lines else '... > ')
        if line.strip().lower() == 'exit':
            return 'exit'
        if line.strip() == '':  # blank line ends input
            break
        lines.append(line)
    return '\n'.join(lines)
while True:
    try:
        data = multiline_input()
        if data == 'exit':
            break
    except EOFError:
        break

    if not data.strip():
        continue

    # Reset syntax error flag
    config.syntax_error = False

    # Print tokens for debug
    lexer.input(data)
    print("Tokens:", end=" ")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"({tok.type}, {tok.value})", end=" ")
    print()

    # Parse input
    result = parser.parse(data, lexer=lexer)
    if not config.syntax_error:
        print("--- Parsing Successful ---")
