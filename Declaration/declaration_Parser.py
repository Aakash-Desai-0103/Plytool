import ply.yacc as yacc
from lexer import tokens
import config
def p_program(p):
    '''program : declarations'''
    p[0] = p[1]
def p_declarations_single(p):
    '''declarations : declaration'''
    p[0] = [p[1]]
def p_declarations_multiple(p):
    '''declarations : declarations declaration'''
    p[0] = p[1] + [p[2]]
def p_declaration(p):
    '''declaration : TYPE declarator_list SEMICOLON'''
    p[0] = ('declaration', p[1], p[2])
def p_declarator_list_single(p):
    '''declarator_list : declarator'''
    p[0] = [p[1]]
def p_declarator_list_multiple(p):
    '''declarator_list : declarator_list COMMA declarator'''
    p[0] = p[1] + [p[3]]
def p_declarator(p):
    '''declarator : ID'''
    p[0] = ('var', p[1])
def p_error(p):
    config.syntax_error = True
    if not p:
        print("Syntax error: unexpected end of input — perhaps missing ';' at end of declaration.")
        return
    msg = f"Syntax error at token {p.type}, value '{p.value}' (line {getattr(p, 'lineno', '?')})"
    if p.type == 'COMMA':
        msg += " → Extra or misplaced comma in variable list."
    elif p.type == 'SEMICOLON':
        msg += " → Misplaced ';' or duplicate semicolon."
    elif p.type == 'TYPE':
        msg += " → Type keyword in unexpected place — missing ';' or wrong declaration order?"
    elif p.type == 'ID':
        msg += " → Unexpected identifier — missing ',' or ';'?"
    elif p.type == 'INT' or p.type == 'FLOAT':
        msg += " → Unexpected constant — declarations should list variable names only."
    elif p.type == 'LBRACKET' or p.type == 'RBRACKET':
        msg += " → Array dimension syntax error — check brackets."
    print(msg)
parser = yacc.yacc(errorlog=yacc.NullLogger())
