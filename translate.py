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
            linea = linea.replace('si', 'if')
            linea = linea.replace('imprimir', 'print')
            linea = linea.replace('{', ':')
            linea = linea.replace(';', '')

            if linea.startswith("for"):
                loop = linea.split(" ")
                variable = loop[1].split("=")[0]
                inicio = loop[1].split("=")[1]
                signo = ""
                final = 0
                signo_paso = ""
                for i in range(len(loop[3])):
                    try:
                        final = int(loop[3][i:])
                        break
                    except:
                        if loop[3][i] == "<" or loop[3][i] == ">" or loop[3][i] == "=":
                            signo += loop[3][i]
                for i in range(len(loop[5])):
                    try:
                        paso = abs(int(loop[5][i:]))
                        break
                    except:
                        pass
                if int(inicio) < final and signo_paso == "+" and (signo == '<=' or signo == '<'):
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
                codigo_python += 'fo("'+definicion_fo+'")\n'
                continue
    # Ejecutar el código Python resultante
    exec("from simplex import fo\n"+codigo_python)


# Ejemplo de uso
# archivo_codigo = 'fo.txt'
# ejecutar_codigo_personalizado(archivo_codigo)
