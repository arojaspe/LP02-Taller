import numpy as np
from scipy.optimize import linprog


def solve_simplex(filename):
    # Leer la función objetivo y las restricciones del archivo
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Obtener el número de variables y restricciones
    num_vars = int(lines[0])
    num_constraints = int(lines[1])

    # Obtener los coeficientes de la función objetivo
    c = np.array([float(x) for x in lines[2].split()])

    # Crear la matriz de restricciones (coeficientes)
    A = np.zeros((num_constraints, num_vars))
    b = np.zeros(num_constraints)

    for i in range(num_constraints):
        line = lines[i + 3].split()
        constraint = line[:-2]
        operator = line[-2]
        rhs = float(line[-1])

        A[i] = [float(x) for x in constraint]
        b[i] = rhs if operator == '<=' else -rhs

    # Resolver el problema utilizando el método Simplex
    res = linprog(c, A_ub=A, b_ub=b, method='simplex')

    # Mostrar la solución obtenida
    print('Solución:')
    print('Valor óptimo:', res.fun)
    print('Variables de decisión:', res.x)


# Llamar a la función con el nombre del archivo de entrada
solve_simplex('datos.txt')
