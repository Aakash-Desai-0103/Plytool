import ply.lex as lex
import config  # <-- import config to set syntax_error flag

# List of token names
tokens = (
    'TYPE',
    'VOID',
    'ID',
    'INT',
    'SEMICOLON',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'IF',
    'ELSE'
)

# Reserved words
reserved = {
    'int': 'TYPE',
    'char': 'TYPE',
    'float': 'TYPE',
    'double': 'TYPE',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE'
}

# Regular expression rules for simple tokens
t_SEMICOLON = r';'
t_COMMA     = r','
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'

# Identifier
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Integer literal
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignore spaces and tabs
t_ignore = ' \t'

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")
    config.syntax_error = True  # <-- set syntax_error flag
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
