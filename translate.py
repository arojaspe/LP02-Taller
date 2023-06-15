def execute_code(archivo):
    # Abrir el archivo y leer su contenido línea por línea
    with open(archivo, 'r') as file:
        lineas = file.readlines()
    with open("simplex.py", "r") as fo:
        codigo = fo.read()
        exec(codigo)

    codigo_python = ''
    indentacion = 0
    definicion_fo = ""
    inicio_fo = False
    # Procesar cada línea del archivo
    for linea in lineas:
        linea = linea.strip()
        if not inicio_fo:
            if linea.startswith("fo"):
                linea = linea.replace('{', ';')
                line = ""
                lineas = ""
                varss = linea.split(" ")
                for i in range(4, len(varss)):
                    var = varss[i]
                    if len(varss[i]) > 1:
                        number = varss[i].split("*")[0]
                        var = (f'"+str('+number+')+"*' +
                               varss[i].split("*")[1])
                    line += var+" "
                for i in range(4):
                    lineas += varss[i]+" "
                lineas += line
                linea = lineas
                codigo_python += "\t" * indentacion
                inicio_fo = True
                definicion_fo += linea
                continue
            # Reemplazar palabras clave y caracteres especiales
            linea = linea.replace('para', 'for')
            linea = linea.replace('si_no', 'else')
            linea = linea.replace('Si', 'if')
            linea = linea.replace('imprimir', 'print')
            linea = linea.replace('{', ':')
            linea = linea.replace('entonces', '')
            if linea.startswith("for"):
                loop = linea.split(";")
                variable = loop[0].split("=")[0].split()[1]
                inicio = loop[0].split("=")[1]
                signo = loop[1].split()[1]
                final = loop[1].split()[2]
                paso = loop[2].split()[4]
                if signo == '<=' or signo == '<':
                    linea = ("for "+variable+" in range("+str(inicio) +
                             ","+str(final)+","+str(paso)+"):")
                else:
                    linea = ("for "+variable+" in range("+str(final) +
                             ","+str(inicio)+",-"+str(paso)+"):")
            if '}' in linea:
                indentacion -= 1
                codigo_python += '\n'
                continue

            # Agregar indentación
            codigo_python += "\t" * indentacion

            # Agregar la línea procesada al código Python
            linea = linea.replace(';', '')
            codigo_python += linea

            # Agregar una nueva línea después de cada línea de código
            codigo_python += '\n'

            # Aumentar la indentación después de abrir un bloque de código
            if ':' in linea:
                indentacion += 1
        else:
            line = ""
            lineas = ""
            varss = linea.split(" ")
            for i in range(1, len(varss)):
                var = varss[i]
                if len(varss[i]) > 2 and not varss[i].__contains__(";"):
                    number = varss[i].split("*")[0]
                    var = (f'"+str('+number+')+"*' +
                           varss[i].split("*")[1])
                if varss[i].__contains__(";"):
                    var = (f'"+str('+varss[i][:-1]+')+";')
                line += var+" "
            lineas = varss[0]+" "
            lineas += line
            definicion_fo += lineas

            if "}" in linea:
                inicio_fo = False
                variable_fo = definicion_fo.split(" ")[2]
                object_creation = variable_fo+"=Simplex()"
                codigo_python += object_creation+"\n" + \
                    variable_fo+'.fo("'+definicion_fo+'")\n'
                continue
    # Ejecutar el código Python resultante
    exec("from Simplex import Simplex\n"+codigo_python)


# Ejemplo de uso
# archivo_codigo = 'fo.txt'
# ejecutar_codigo_personalizado(archivo_codigo)
