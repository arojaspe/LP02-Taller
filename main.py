from ply import lex
from ply import yacc
from transform import transform
from pulp import *

# Lista de tokens
tokens = [
    'MIN',      # Token para "min"
    'MAX',      # Token para "max"
    'FO',       # Token para función
    'R',        # Token para restricción
    'VAR',      # Token para nombres de variables
    'LBRACKET',  # Token para caracter de arreglo o matriz "["
    'RBRACKET',  # Token para caracter de arreglo o matriz "]"
    'COMMA',    # Token para caracter de arreglo o matriz ","
    'ARRAY',
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
    'IF',  # Token para la palabra reservada de Python "if"
    'ELSE',  # Token para la palabra reservada de Python "else"
    'FOR',  # Token para la palabra reservada de Python "for"
    'WHILE',  # Token para la palabra reservada de Python "while"
    'DO',  # Token para la palabra reservada de Python "do"
    'SWITCH',  # Token para la palabra reservada de Python "switch"
    'CASE',  # Token para la palabra reservada de Python "case"
    'BREAK',  # Token para la palabra reservada de Python "break"
    'CONTINUE',  # Token para la palabra reservada de Python "continue"
    'RETURN',  # Token para la palabra reservada de Python "return"
    'FUNCTION',  # Token para la palabra reservada de Python "function"
    'CLASS',  # Token para la palabra reservada de Python "class"
    'TRY',  # Token para la palabra reservada de Python "try"
    'CATCH',  # Token para la palabra reservada de Python "catch"
    'THROW',  # Token para la palabra reservada de Python "throw"
    'FINALLY',  # Token para la palabra reservada de Python "finally"
    'IMPORT',  # Token para la palabra reservada de Python "import"
    'EXPORT',  # Token para la palabra reservada de Python "export"
    'CONST',  # Token para la palabra reservada de Python "const"
    'LET',  # Token para la palabra reservada de Python "let"
    'STATIC',  # Token para la palabra reservada de Python "static"
    'PUBLIC',  # Token para la palabra reservada de Python "public"
    'PRIVATE',  # Token para la palabra reservada de Python "private"
    'PROTECTED',  # Token para la palabra reservada de Python "protected"
    'INTERFACE',  # Token para la palabra reservada de Python "interface"
    'EXTENDS',  # Token para la palabra reservada de Python "extends"
    'IMPLEMENTS',  # Token para la palabra reservada de Python "implements"
    'NEW',  # Token para la palabra reservada de Python "new"
    'THIS',  # Token para la palabra reservada de Python "this"
    'SUPER',  # Token para la palabra reservada de Python "super"
    'INSTANCEOF',  # Token para la palabra reservada de Python "instanceof"
    'TRUE',  # Token para la palabra reservada de Python "true"
    'FALSE',  # Token para la palabra reservada de Python "false"
    'NULL'  # Token para la palabra reservada de Python "null"
]

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_EQUAL = r'\='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
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


def p_problema(p):
    '''problema : funcionobjetivo
                | restriccion
                | expresion'''
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
        p[0] = ('restricción', p[2])
    else:
        p[0] = ('restricción', p[2], ('operador de comparación', p[3]), p[4])


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
        p[0] = (p[1]) + p[3]


def p_error(p):
    if p != None:
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
            contador += 1


def main():
    nombre_archivo = "archivo.txt"
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            imprimir(linea)
    res = transform(nombre_archivo)
    print("Estado de la solución:", LpStatus[res.status])

    # Imprimir la solución óptima y el valor óptimo
    print("Valor óptimo:", value(res.objective))
    print("Solución:")
    for variable in res.variables():
        print(variable.name, "=", value(variable))


if __name__ == '__main__':
    main()
