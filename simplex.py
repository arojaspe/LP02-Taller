from pulp import *


def fo(text):
    variables = 0  # Inicializar el número de variables
    coeficientes = []  # Lista para almacenar los coeficientes de la función objetivo
    restricciones_list = []  # Lista para almacenar las restricciones
    restriccions = []
    variablesfo = []  # Lista para almacenar los coeficientes de la función objetivo
    lines = text.split(";")
    print("Solucion para: ")
    for line in lines:
        line = line.strip()  # Eliminar espacios en blanco al inicio y final de la línea
        print(line)
        if line.startswith("sa"):
            line = line.replace("sa ", "")

        if line.startswith("fo"):
            # Línea de la función objetivo
            # Extraer los coeficientes de la función objetivo
            line = line.split()[0:]
            variable = line[2]
            objetivo = line[1]
            variablesfo = line[4:]
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
        elif line == "":
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
            restriccions.append(res[1][1:])
            restricciones_list.append(restriccions)

    fo = ' '.join(str(elemento) for elemento in coeficientes)
    content = objetivo+"\n"+str(variables)+"\n"+fo+"\n"
    # Imprimir las restricciones
    for restriccion in restricciones_list:
        restricciones = ' '.join(str(elemento) for elemento in restriccion)
        content += restricciones+"\n"
    with open("datos.txt", 'w') as file:
        file.write(content)
    solve()


def solve():
    variables = []
    fo = None
    variable = 0
    restriction = None
    foOk = False
    with open('datos.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("max"):
                prob = LpProblem("Problema", LpMaximize)
            elif line.startswith("min"):
                prob = LpProblem("Problema", LpMinimize)
            elif line == "":
                continue
            elif variable == 0:
                try:
                    variable = int(line)
                    for i in range(0, variable):
                        variables.append(LpVariable("x"+str(i+1), lowBound=0))
                except:
                    pass
            elif not foOk:
                numbers = line.split(" ")
                for i in range(len(numbers)):
                    fo += float(numbers[i])*variables[i]
                prob += fo
                foOk = True
            elif restriction == None:
                numbers = line.split(" ")
                # Resolver el problema
                if numbers[len(numbers)-2] == ">=":
                    prob += lpSum((float(numbers[i]) * variables[i])
                                  for i in range(len(variables))) >= float(numbers[len(numbers)-1])

                elif numbers[len(numbers)-2] == "<=":
                    prob += lpSum((float(numbers[i]) * variables[i])
                                  for i in range(len(variables))) <= float(numbers[len(numbers)-1])

    # Resolver el problema
    prob.solve(PULP_CBC_CMD(msg=False))

    # Imprimir el estado de la solución
    print("Estado de la solución:", LpStatus[prob.status])

    # Imprimir la solución óptima y el valor óptimo
    print("Valor óptimo:", value(prob.objective))
    print("Solución:")
    for variable in prob.variables():
        print(variable.name, "=", value(variable))
