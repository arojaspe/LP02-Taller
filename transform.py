from simplex import solve


def transform(filename):
    variables = 0  # Inicializar el número de variables
    coeficientes = []  # Lista para almacenar los coeficientes de la función objetivo
    restricciones_list = []  # Lista para almacenar las restricciones
    restriccions = []
    variablesfo = []  # Lista para almacenar los coeficientes de la función objetivo
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()  # Eliminar espacios en blanco al inicio y final de la línea
        if line.__contains__("fo"):
            # Línea de la función objetivo
            # Extraer los coeficientes de la función objetivo
            line = line.split()[0:-1]
            variable = line[0]
            variablesfo = line[3:]
            objetivo = variablesfo[0]
            variablesfo = variablesfo[1:]
            aux = []
            for i in range(0, len(variablesfo)):
                if i % 2 == 0:
                    aux.append(variablesfo[i])
                else:
                    if variablesfo[i] == "-":
                        variablesfo[i+1] = "-"+variablesfo[i+1]
            variablesfo = aux
            variables = len(variablesfo)
            for i in range(0, len(variablesfo)):
                try:
                    c = float(variablesfo[i].split("*")[0])
                except:
                    c = 1
                coeficientes.append(c)
        elif line == "" or line.startswith("sa"):
            # Línea de cierre o línea vacía, ignorar
            continue
        elif line.startswith("}"):
            break
        else:
            # Línea de restricción
            res = line
            # Extraer los coeficientes de la restricción
            restriccion = res.split()[1:-2]
            restriccions = []
            for i in range(0, len(restriccion)):
                if i % 2 == 0:
                    try:
                        r = float(restriccion[i].split("*")[0])
                    except:
                        r = 1
                    restriccions.append(r)
                else:
                    if restriccion[i] == "-":
                        restriccion[i+1] = "-"+restriccion[i+1]

            res = line.split(restriccion[len(restriccion)-1])
            restriccions.append(res[1][1:-1])
            restricciones_list.append(restriccions)

    fo = ' '.join(str(elemento) for elemento in coeficientes)
    content = objetivo+"\n"+str(variables)+"\n"+fo+"\n"
    # Imprimir las restricciones
    for restriccion in restricciones_list:
        restricciones = ' '.join(str(elemento) for elemento in restriccion)
        content += restricciones+"\n"
    with open("datos.txt", 'w') as file:
        file.write(content)
    res = [variable]
    res.append(solve())
    return res


transform("fo.txt")
