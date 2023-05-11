from ply import lex
from ply import yacc

# Lista de tokens
tokens = [
    'MIN',      # Token para "min"
    'MAX',      # Token para "max"
    'FO',       # Token para función
    'R',        # Token para restricción
    'VAR',      # Token para nombres de variables
    'NUMBER',   # Token para números
    'PLUS',     # Token para el operador "+"
    'MINUS',    # Token para el operador "-"
    'TIMES',    # Token para el operador "*"
    'DIVIDE',   # Token para el operador "/"
    'EQUAL',     # Token para el operador "="
    'LT',        # Token para el operador "<"
    'LE',        # Token para el operador "<="
    'GT',        # Token para el operador ">"
    'GE'        # Token para el operador ">="
]

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_EQUAL = r'\='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_ignore = ' \t'

# Expresiones regulares para tokens complejos
def t_MIN(t):
    r'min'
    return t

def t_MAX(t):
    r'max'
    return t

def t_FO(t):
    r'fo'
    return t

def t_R(t):
    r'r'
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
def p_problema(p):
    '''problema : funcionobjetivo
                | restriccion'''
    p[0] = p[1]

def p_funcionobjetivo(p):
    '''funcionobjetivo : FO MIN expresion
                       | FO MAX expresion'''
    p[0] = ('funcionobjetivo', ('Palabra reservada', p[2]), p[3])

def p_restriccion(p):
    '''restriccion : R expresion
                   | R expresion LT expresion   
                   | R expresion LE expresion
                   | R expresion GT expresion
                   | R expresion GE expresion
                   | R expresion EQUAL expresion'''
    if len(p) == 2:
        p[0] = ('restriccion', p[2])
    else:
        p[0] = ('restriccion', p[2], ('operador de comparacion', p[3]), p[4])

def p_expresion(p):
    '''expresion : termino
                 | expresion PLUS termino
                 | expresion MINUS termino
                 | expresion EQUAL termino
                 | expresion DIVIDE termino'''
    if len(p) == 2:
        p[0] = ('expresion', p[1])
    else:
        p[0] = ('expresion', p[1], ('operador', p[2]), p[3])

def p_termino(p):
    '''termino : factor
               | termino TIMES factor'''
    if len(p) == 2:
        p[0] = ('termino', p[1])
    else:
        p[0] = ('termino', p[1], ('operador', p[2]), ('factor', p[3]))

def p_factor(p):
    '''factor : NUMBER
              | VAR'''
    p[0] = ('numero', p[1])

def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)
    
# Construcción del parser
parser = yacc.yacc()

# Función principal
def imprimir(text):
    try:
        s = text
    except EOFError:
        exit()
    result = parser.parse(s)
    print(result, "\n")
    contador = 0
    for elem in (str(result).split('(')):
        elem = elem.strip().replace(')', "")
        elem = elem.strip().replace("'", "")
        elem = elem.strip().replace(",", "")
        if elem != "":
            print("\t"*contador+elem)
        else:
            contador+=1
                
def main():
    nombre_archivo = "archivo.txt"
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            imprimir(linea)

if __name__ == '__main__':
    main()