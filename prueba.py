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
def p_funcionobjetivo(p):
    '''funcionobjetivo : MIN expresion
                  | MAX expresion'''
    p[0] = (('Palabra reservada',p[1]), ('Expresión ', p[2]))

def p_expresion(p):
    '''expresion : termino
            | termino PLUS expresion
            | termino MINUS expresion
            | termino EQUAL expresion
            | termino DIVIDE expresion'''
    
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (('término ',p[1]), ('operador',p[2]), (p[3]))

def p_termino(p):
    '''termino : factor
                | factor TIMES termino'''
    if len(p) == 2:
        p[0] = ('variable',p[1])
    else:
        p[0] = (('número',p[1]), ('operador',p[2]), p[3])

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
        contador = 0
        for elem in (str(result).split('(')):
            elem = elem.strip().replace(')', "")
            elem = elem.strip().replace("'", "")
            elem = elem.strip().replace(",", "")
            if elem != "":
                print("\t"*contador+elem)
                if "+" in elem:
                    contador-=1 
            else:
                contador+=1
if __name__ == '__main__':
    main()