from ply import lex
from ply import yacc

# Lista de tokens
tokens = [
    'MIN',      # Token para "min"
    'MAX',      # Token para "max"
    'VAR',      # Token para nombres de variables
    'NUMBER',   # Token para números
    'PLUS',     # Token para el operador "+"
    'MINUS',    # Token para el operador "-"
    'TIMES',    # Token para el operador "*"
    'DIVIDE',   # Token para el operador "/"
    'EQUAL'     # Token para el operador "="
]

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_EQUAL = r'\='
t_ignore = ' \t'

# Expresiones regulares para tokens complejos
def t_MIN(t):
    r'min'
    return t

def t_MAX(t):
    r'max'
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# Manejo de errores
def t_error(t):
    print("Error: Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()


# Definición de la gramática
def p_expression(p):
    '''expression : MIN expr
                  | MAX expr'''
    p[0] = (p[1], p[2])

def p_expr(p):
    '''expr : term
            | term PLUS expr
            | term MINUS expr
            | term EQUAL expr
            | term DIVIDE expr'''
    
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])

def p_term(p):
    '''term : factor
            | factor TIMES term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])

def p_factor(p):
    '''factor : NUMBER
              | VAR'''
    p[0] = p[1]

def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)
    
# Construcción del parser
parser = yacc.yacc()

# Función principal
def main():
    while True:
        try:
            s = input('Ingrese una expresión: ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result, "\n")
        print(type(result))

if __name__ == '__main__':
    main()