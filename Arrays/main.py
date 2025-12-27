from lexer import lexer
from parser_array import parser
import config  # use config for syntax_error flag
print("--- C++ Language 5-Construct Parser ---")
print("--- Arrays Construct (Multi-line input enabled) ---")
print("Type 'exit' to quit.")
print("Press Enter on a blank line to parse your code.\n")
while True:
    try:
        first_line = input('C++-Code > ')
        if first_line.strip().lower() == 'exit':
            break
        if not first_line.strip():
            continue
        lines = [first_line]
        while True:
            line = input('...    > ')
            if not line.strip():
                break
            lines.append(line)
        data = "\n".join(lines)
        config.syntax_error = False
        lexer.input(data)
        print("Tokens:", end=" ")
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(f"({tok.type}, {tok.value})", end=" ")
        print()
        result = parser.parse(data, lexer=lexer)
        if not config.syntax_error:
            print("--- Parsing Successful ---")
    except EOFError:
        break
    except Exception as e:
        print(f"Unexpected error: {e}")
