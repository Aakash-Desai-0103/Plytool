import ply.yacc as yacc
from lexer import tokens
import config
def p_program(p):
    '''program : declarations'''
    p[0] = p[1]
def p_declarations_multiple(p):
    '''declarations : declarations declaration'''
    p[0] = p[1] + [p[2]]
def p_declarations_single(p):
    '''declarations : declaration'''
    p[0] = [p[1]]
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
        p[0] = p[1] + [p[3]]  # append next dimension
def p_error(p):
    config.syntax_error = True
    if not p:
        print("Syntax error: unexpected end of input — perhaps missing ';' or ']'?")
        return
    msg = f"Syntax error at token {p.type}, value '{p.value}'"
    if p.type == 'SEMICOLON':
        msg += " → Possible cause: misplaced or missing ';' after declaration."
    elif p.type == 'COMMA':
        msg += " → Possible cause: extra or missing comma between variables."
    elif p.type == 'LBRACKET':
        msg += " → Possible cause: invalid array syntax (missing size or ']')."
    elif p.type == 'RBRACKET':
        msg += " → Possible cause: unmatched ']' or missing '['."
    elif p.type == 'INT':
        msg += " → Possible cause: invalid array size or misplaced number."
    elif p.type == 'ID':
        msg += " → Possible cause: unexpected identifier — maybe missing a comma or semicolon?"
    elif p.type == 'TYPE':
        msg += " → Possible cause: misplaced type keyword or missing ';' before this line."
    print(msg)
parser = yacc.yacc(errorlog=yacc.NullLogger())
