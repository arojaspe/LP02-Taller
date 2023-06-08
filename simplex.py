from pulp import *


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
                    fo += int(numbers[i])*variables[i]
                prob += fo
                foOk = True
            elif restriction == None:
                numbers = line.split(" ")
                # Resolver el problema
                if numbers[len(numbers)-2] == ">":
                    prob += lpSum((int(numbers[i]) * variables[i])
                                  for i in range(len(variables))) > int(numbers[len(numbers)-1])

                elif numbers[len(numbers)-2] == "<":
                    prob += lpSum((int(numbers[i]) * variables[i])
                                  for i in range(len(variables))) < int(numbers[len(numbers)-1])

                elif numbers[len(numbers)-2] == ">=":
                    prob += lpSum((int(numbers[i]) * variables[i])
                                  for i in range(len(variables))) >= int(numbers[len(numbers)-1])

                elif numbers[len(numbers)-2] == "<=":
                    prob += lpSum((int(numbers[i]) * variables[i])
                                  for i in range(len(variables))) <= int(numbers[len(numbers)-1])

    # Resolver el problema
    prob.solve()

    # Imprimir el estado de la solución
    # print("Estado de la solución:", LpStatus[prob.status])

    # Imprimir la solución óptima y el valor óptimo
    # print("Valor óptimo:", value(prob.objective))
    # print("Solución:")
    # for variable in prob.variables():
    #    print(variable.name, "=", value(variable))

    return prob
