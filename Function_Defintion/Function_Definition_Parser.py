import ply.yacc as yacc
from lexer import tokens
import config
def p_program(p):
    '''program : function_defs'''
    p[0] = p[1]
def p_function_defs_single(p):
    '''function_defs : function_def'''
    p[0] = [p[1]]
def p_function_defs_multiple(p):
    '''function_defs : function_defs function_def'''
    p[0] = p[1] + [p[2]]
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
def p_statements_opt(p):
    '''statements_opt : statements_opt declaration
                      | declaration
                      | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]   # Add declaration to list
    elif len(p) == 2 and p[1]:
        p[0] = [p[1]]          # Single declaration
    else:
        p[0] = []              # Empty body
def p_declaration(p):
    '''declaration : TYPE ID SEMICOLON'''
    p[0] = ('declaration', p[1], p[2])
def p_empty(p):
    'empty :'
    p[0] = None
def p_error(p):
    config.syntax_error = True
    if not p:
        print("Syntax error: unexpected end of input — maybe a missing '}' or ';' in function definition.")
        return
    msg = f"Syntax error at token {p.type}, value '{p.value}' (line {getattr(p, 'lineno', '?')})"
    if p.type == 'LPAREN':
        msg += " → Missing '(' or misplaced parenthesis in parameter list."
    elif p.type == 'RPAREN':
        msg += " → Missing ')' — possibly incomplete parameter list."
    elif p.type == 'LBRACE':
        msg += " → Unexpected '{' — perhaps a missing ')' or ';'."
    elif p.type == 'RBRACE':
        msg += " → Unmatched '}' — missing '{' in function body?"
    elif p.type == 'TYPE':
        msg += " → Unexpected type keyword — misplaced declaration?"
    elif p.type == 'ID':
        msg += " → Unexpected identifier — maybe missing a comma or semicolon?"
    elif p.type == 'SEMICOLON':
        msg += " → Misplaced ';' — possibly inside parameter list or after a block."
    print(msg)
parser = yacc.yacc(errorlog=yacc.NullLogger())