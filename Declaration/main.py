from lexer import lexer
from declaration_Parser import parser
import config  # for syntax_error flag

print("--- C++ Language 5-Construct Parser ---")
print("--- (Multi-line input enabled. Press Enter on a blank line to parse.) ---")
print("Type 'exit' to quit.")

while True:
    try:
        # First line of code
        first_line = input('C++-Code > ')
        if first_line.strip().lower() == 'exit':
            break
        if not first_line.strip():
            continue

        # Collect subsequent lines until blank line
        lines = [first_line]
        while True:
            line = input('...    > ')
            if not line.strip():
                break
            lines.append(line)

        # Join lines into a single code block
        data = "\n".join(lines)

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
    except EOFError:
        break  # Exit on Ctrl+D
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
