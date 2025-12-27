import ply.yacc as yacc
from lexer import tokens
import config  # <-- use config for syntax_error flag

# Precedence (not strictly needed here, but can help future expansions)
precedence = ()

# ---------- Grammar rules ----------

def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement(p):
    '''statement : declaration
                 | function_decl
                 | function_def
                 | if_stmt'''
    p[0] = p[1]

# ---------- Declarations ----------

def p_declaration(p):
    '''declaration : TYPE declarator_list SEMICOLON'''
    p[0] = ('declaration', p[1], p[2])

def p_declarator_list_single(p):
    '''declarator_list : declarator'''
    p[0] = [p[1]]

def p_declarator_list_multiple(p):
    '''declarator_list : declarator_list COMMA declarator'''
    p[0] = p[1] + [p[3]]

# ---------- Declarators (variables and arrays, including multi-dimensional) ----------

def p_declarator(p):
    '''declarator : ID
                  | ID array_dims'''
    if len(p) == 2:
        p[0] = ('var', p[1])
    else:
        p[0] = ('array', p[1], p[2])

def p_array_dims(p):
    '''array_dims : LBRACKET INT RBRACKET
                  | array_dims LBRACKET INT RBRACKET'''
    if len(p) == 4:
        p[0] = [p[2]]  # first dimension
    else:
        p[0] = p[1] + [p[3]]  # append additional dimension


# ---------- If/Else statements ----------

def p_if_stmt(p):
    '''if_stmt : IF LPAREN ID RPAREN LBRACE statements_opt RBRACE else_opt'''
    p[0] = ('if', p[3], p[6], p[8])

def p_statements_opt(p):
    '''statements_opt : statements
                      | empty'''
    p[0] = p[1]

def p_else_opt(p):
    '''else_opt : ELSE IF LPAREN ID RPAREN LBRACE statements_opt RBRACE else_opt
                | ELSE LBRACE statements_opt RBRACE
                | empty'''
    if len(p) == 10:  # matched ELSE IF ...
        p[0] = ('else_if', p[3], p[6], p[8])
    elif len(p) == 5:  # matched simple ELSE
        p[0] = p[3]
    else:
        p[0] = None


# ---------- Function Declaration ----------

def p_function_decl(p):
    '''function_decl : TYPE ID LPAREN param_list_opt RPAREN SEMICOLON
                     | VOID ID LPAREN param_list_opt RPAREN SEMICOLON'''
    p[0] = ('func_decl', p[1], p[2], p[4])


# ---------- Function Definition ----------

def p_function_def(p):
    '''function_def : TYPE ID LPAREN param_list_opt RPAREN LBRACE statements_opt RBRACE
                    | VOID ID LPAREN param_list_opt RPAREN LBRACE statements_opt RBRACE'''
    p[0] = ('func_def', p[1], p[2], p[4], p[7])

def p_param_list_opt(p):
    '''param_list_opt : param_list
                      | VOID
                      | empty'''
    if p[1] == 'void':
        p[0] = []
    else:
        p[0] = p[1]

def p_param_list_single(p):
    '''param_list : TYPE ID'''
    p[0] = [(p[1], p[2])]

def p_param_list_multiple(p):
    '''param_list : param_list COMMA TYPE ID'''
    p[0] = p[1] + [(p[3], p[4])]


# ---------- Empty rule ----------

def p_empty(p):
    'empty :'
    p[0] = None


# ---------- Error rule (Enhanced with reserved-word detection) ----------

def p_error(p):
    config.syntax_error = True  # Use shared config flag

    if not p:
        print("Syntax error: unexpected end of input (possibly missing '}' or ';').")
        return

    msg = f"Syntax error at token {p.type}, value '{p.value}', line {p.lineno}"

    if p.type == 'SEMICOLON':
        msg += " -> Possible cause: extra or misplaced ';'."
    elif p.type == 'ID':
        msg += " -> Possible cause: unexpected identifier. Maybe missing a comma, operator, or semicolon?"
    elif p.type == 'RBRACE':
        msg += " -> Possible cause: unmatched '}' (missing a '{'?)."
    elif p.type == 'RPAREN':
        msg += " -> Possible cause: unmatched ')' (missing a '('?)."
    elif p.type == 'RBRACKET':
        msg += " -> Possible cause: unmatched ']' (missing a '[' or array size?)."
    elif p.type == 'ELSE':
        msg += " -> Possible cause: 'else' without a matching 'if'."
    elif p.type == 'LBRACE':
        msg += " -> Possible cause: unexpected '{'. Maybe you forgot a ')' or function/if keyword?"
    elif p.type in ('TYPE', 'VOID', 'IF', 'ELSE'):
        msg += " -> Possible cause: reserved keyword used as an identifier."

    print(msg)


# ---------- Build parser (Suppress PLY Warnings) ----------

parser = yacc.yacc(errorlog=yacc.NullLogger())
