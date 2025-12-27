import ply.yacc as yacc
from lexer import tokens
import config
def p_program(p):
    '''program : function_decls'''
    p[0] = p[1]
def p_function_decls_single(p):
    '''function_decls : function_decl'''
    p[0] = [p[1]]
def p_function_decls_multiple(p):
    '''function_decls : function_decls function_decl'''
    p[0] = p[1] + [p[2]]
def p_function_decl(p):
    '''function_decl : TYPE ID LPAREN param_list_opt RPAREN SEMICOLON
                     | VOID ID LPAREN param_list_opt RPAREN SEMICOLON'''
    p[0] = ('func_decl', p[1], p[2], p[4])
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
def p_empty(p):
    'empty :'
    p[0] = None
def p_error(p):
    config.syntax_error = True
    if not p:
        print("Syntax error: unexpected end of input (missing ';' or ')'?)")
        return
    msg = f"Syntax error at token {p.type}, value '{p.value}'"
    if p.type == 'SEMICOLON':
        msg += " → Possible cause: extra or misplaced ';'."
    elif p.type == 'RPAREN':
        msg += " → Possible cause: missing '('."
    elif p.type == 'LPAREN':
        msg += " → Possible cause: missing ')' or invalid parameters."
    elif p.type == 'ID':
        msg += " → Possible cause: unexpected identifier or missing comma."
    elif p.type in ('TYPE', 'VOID'):
        msg += " → Possible cause: misplaced type keyword or missing identifier."    
    print(msg)
parser = yacc.yacc(errorlog=yacc.NullLogger())
