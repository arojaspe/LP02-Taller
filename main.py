from ply import lex
from ply import yacc

# Lista de tokens
tokens = [
    'MIN',      # Token para "min"
    'MAX',      # Token para "max"
    'FO',       # Token para función
    'R',        # Token para restricción
    'SA',
    'VAR',      # Token para nombres de variables
    'LBRACKET', # Token para caracter de arreglo o matriz "[" 
    'RBRACKET', # Token para caracter de arreglo o matriz "]"
    'LBRACE',   # Token para caracter "{"
    'RBRACE',   # Token para caracter "}"
    'COMMA',    # Token para caracter de arreglo o matriz ","
    'ARRAY',    # Token para identificar arrays
    'PCOMA',    # Token para caracter ";"
    'SI',       # Token para palabra reservada "SI"
    'SI_NO',    # Token para palabra reservada "SI_NO"
    'ENTONCES', # Token para palabra reservada "ENTONCES"
    'RETORNAR', # Token para palabra reservada "RETORNAR"
    'IMPRIMIR',
    'LPAR',   # Token para caracter "("
    'RPAR',   # Token para caracter ")"
    'NUMBER',   # Token para números
    'PLUS',     # Token para el operador "+"
    'MINUS',    # Token para el operador "-"
    'TIMES',    # Token para el operador "*"
    'DIVIDE',   # Token para el operador "/"
    'EQUAL',     # Token para el operador "="
    'LT',        # Token para el operador "<"
    'LE',        # Token para el operador "<="
    'GT',        # Token para el operador ">"
    'GE',        # Token para el operador ">="
]

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_EQUAL = r'\='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAR = r'\('
t_RPAR = r'\)'
t_COMMA = r','
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_PCOMA = r';'

t_ignore = ' \t \n'

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

def t_SI(t):
    r'SI'
    return t

def t_SI_NO(t):
    r'SI_NO'
    return t

def t_ENTONCES(t):
    r'entonces'
    return t

def t_RETORNAR(t):
    r'retornar'
    return t

def t_IMPRIMIR(t):
    r'imprimir'
    return t

def t_SA(t):
    r'SA'
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    print("Comentario", t.value)

# Manejo de errores
def t_error(t):
    if t.value[0] != None: 
        print("Error: Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Definición de la gramática

# def p_iniciar(p): 
#     ''' iniciar : contenido  
#                 '''
#     p[0] = p[1]

def p_contenido(p):
    ''' contenido : problema
                  | proposicion
                  | IMPRIMIR LPAR expresion RPAR PCOMA'''
    p[0] = p[1]

def p_proposicion(p):
    ''' proposicion : si_senten'''
    
def p_problema(p):
    '''problema : funcionobjetivo restricciones'''
    print(p[0])
    p[0] = (p[1]), (p[2])

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
        p[0] = ('restricción', p[2])
    else:
        p[0] = ('restricción', p[2], ('operador de comparación', p[3]), (p[4]))

def p_restricciones(p):
    '''restricciones : restriccion PCOMA
                     | restriccion PCOMA restricciones'''
    
    if len(p) == 2:
        p[0] = p[1]
    
    else:
        p[0] = [p[1]] + [p[2]]

def p_expresion(p):
    '''expresion : termino
                 | expresion PLUS termino
                 | expresion MINUS termino
                 | expresion EQUAL termino
                 | expresion DIVIDE termino'''
    if len(p) == 2:
        p[0] = (p[1])
    else:
        p[0] = p[1], ('operador', p[2]), p[3]

def p_termino(p):
    '''termino : factor
               | termino TIMES factor'''
    if len(p) == 2:
        p[0] = (p[1])
    else:
        p[0] = (p[1], ('operador', p[2]), p[3])

def p_factor(p):
    '''factor : NUMBER
              | VAR
              | array'''
    if isinstance(p[1], float):
        p[0] = ('número', p[1])
    elif isinstance(p[1], str):
        p[0] = ('variable', p[1])
    else:
        p[0] = (p[1])
def p_array(p):
    '''array : LBRACKET arrayElements RBRACKET
             | matrix'''
    if len(p) == 4:
        p[0] = ('array', p[2])
    else:
        p[0] = p[1]
   
def p_arrayElements(p):
    '''arrayElements : factor
                     | arrayElements COMMA factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif isinstance(p[3], tuple):
        p[0] = p[1] + (p[3],)
    else:
        p[0] = p[1] + (p[3],)

def p_matrix(p):
    '''matrix : LBRACKET array RBRACKET
              | LBRACKET array COMMA matrix_elements RBRACKET'''

    if len(p) == 4:
        p[0] = ('matrix', p[2])
    else:
        p[0] = ('matrix', p[2]) + p[4]

def p_matrix_elements(p):
    '''matrix_elements : array
                       | array COMMA matrix_elements'''
    if len(p) == 2:
        p[0] = (p[1])
    else:
        p[0] = (p[1])+ p[3]

def p_si_senten(p):
    '''si_senten : SI restriccion ENTONCES expresion
                 | SI restriccion ENTONCES expresion SI_NO expresion'''
    if len(p) == 4:
        p[0] = ('Palabra reservada', p[0]), ('Condicion', p[1]), ('Palabra reservada', p[2]), p[3]
    else:
        p[0] = ('Palabra reservada', p[0]), ('Condicion', p[2]), ('Palabra reservada', p[2]), p[3], ('Palabra reservada', p[4]), p[5]


# def p_exp_condicional(p):
#     '''exp_condicional : expresion LT expresion
#                        | expresion LE expresion
#                        | expresion GT expresion
#                        | expresion GE expresion
#                        | expresion EQUAL expresion'''
#     p[0] = ('Operador de comparación', p[2])

# def p_bloque(p):
#     '''bloque : LBRACE sentencias RBRACE'''
#     p[0] = ('bloque', p[2])


# def p_sentencias(p):
#     '''sentencias : sentencia
#                   | sentencias sentencia'''
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[0] = p[1] + [p[2]]

# def p_sentencia(p):
#     '''sentencia : RETORNAR expresion PCOMA
#                  | IMPRIMIR expresion PCOMA'''
#     p[0] = (('Sentencia', p[1]), (p[2]), p[3])

def p_error(p):
    if p!=None:
        print("Error de sintaxis en '%s'" % p)
    
# Construcción del parser
parser = yacc.yacc()

# Función principal
def imprimir(text):
    try:
        s = text
    except EOFError:
        exit()
    result = parser.parse(s)
    if result != None: 
        print(result, "\n")
    contador = 0
    for elem in (str(result).split('(')):
        elem = elem.strip().replace(')', "")
        elem = elem.strip().replace("'", "")
        elem = elem.strip().replace(",", "")
        if elem != "" and elem != "None":
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