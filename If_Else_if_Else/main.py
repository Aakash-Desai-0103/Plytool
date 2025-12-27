from lexer import lexer
from If_Else_Else_If_Parser import parser
import config  # <-- use config for syntax_error flag

print("--- C++ Language 5-Construct Parser ---")
print("--- (If / Else / Else If Parser with Multi-line Input) ---")
print("Type 'exit' to quit.")
print("Enter your code (press Enter on a blank line to parse):")

while True:
    try:
        lines = []
        while True:
            line = input('C++-Code > ' if not lines else '...    > ')
            if line.strip().lower() == 'exit':
                raise KeyboardInterrupt
            if line.strip() == '':
                break
            lines.append(line)
        if not lines:
            continue
        data = '\n'.join(lines)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        break

    # Reset syntax error flag
    config.syntax_error = False

    # Print tokens for debugging
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
