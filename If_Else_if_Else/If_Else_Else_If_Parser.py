import ply.yacc as yacc
from lexer import tokens
import config
def p_program(p):
    '''program : if_stmts'''
    p[0] = p[1]
def p_if_stmts_single(p):
    '''if_stmts : if_stmt'''
    p[0] = [p[1]]
def p_if_stmts_multiple(p):
    '''if_stmts : if_stmts if_stmt'''
    p[0] = p[1] + [p[2]]
def p_if_stmt(p):
    '''if_stmt : IF LPAREN ID RPAREN LBRACE statements_opt RBRACE else_opt'''
    p[0] = ('if', p[3], p[6], p[8])
def p_statements_opt(p):
    '''statements_opt : statements_opt declaration
                      | declaration
                      | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2 and p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []
def p_else_opt(p):
    '''else_opt : ELSE IF LPAREN ID RPAREN LBRACE statements_opt RBRACE else_opt
                | ELSE LBRACE statements_opt RBRACE
                | empty'''
    if len(p) == 10:
        p[0] = ('else_if', p[3], p[6], p[8])
    elif len(p) == 5:
        p[0] = ('else', p[3])
    else:
        p[0] = None
def p_declaration(p):
    '''declaration : TYPE ID SEMICOLON'''
    p[0] = ('declaration', p[1], p[2])
def p_empty(p):
    'empty :'
    p[0] = None
def p_error(p):
    config.syntax_error = True
    if not p:
        print("Syntax error: unexpected end of input — perhaps missing '}' or ';' in if/else block.")
        return
    msg = f"Syntax error at token {p.type}, value '{p.value}'"
    if p.type == 'IF':
        msg += " → Unexpected 'if'. Maybe missing 'else' block closure?"
    elif p.type == 'ELSE':
        msg += " → 'else' without matching 'if', or misplaced braces."
    elif p.type == 'LBRACE':
        msg += " → Unexpected '{'. Maybe missing ')' after condition?"
    elif p.type == 'RBRACE':
        msg += " → Unmatched '}'. Missing '{' before this?"
    elif p.type == 'LPAREN':
        msg += " → Missing ')' or incorrect condition syntax."
    elif p.type == 'RPAREN':
        msg += " → Missing '(' before condition."
    elif p.type == 'ID':
        msg += " → Unexpected identifier. Did you forget parentheses or braces?"
    elif p.type == 'TYPE':
        msg += " → Unexpected type inside if/else block."
    print(msg)
parser = yacc.yacc(errorlog=yacc.NullLogger())
