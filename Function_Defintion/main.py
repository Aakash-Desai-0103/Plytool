from lexer import lexer
from Function_Definition_Parser import parser
import config  # for syntax_error flag

print("--- C++ Language 5-Construct Parser ---")
print("--- (Multi-line input enabled. Press Enter on a blank line to parse.) ---")
print("Type 'exit' to quit.")

while True:
    try:
        # Read the first line
        first_line = input('C++-Code > ')
        if first_line.strip().lower() == 'exit':
            break
        if not first_line.strip():
            continue

        # Collect further lines until blank line
        lines = [first_line]
        while True:
            line = input('...    > ')
            if not line.strip():
                break
            lines.append(line)

        # Join into a single multi-line string
        data = "\n".join(lines)

        # Reset syntax error flag
        config.syntax_error = False

        # Debug: print tokens
        lexer.input(data)
        print("Tokens:", end=" ")
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(f"({tok.type}, {tok.value})", end=" ")
        print()

        # Parse the code
        result = parser.parse(data, lexer=lexer)
        if not config.syntax_error:
            print("--- Parsing Successful ---")

    except EOFError:
        break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
