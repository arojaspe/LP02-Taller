
variables = 0  # Inicializar el número de variables
restricciones = 0  # Inicializar el número de restricciones
coeficientes = []  # Lista para almacenar los coeficientes de la función objetivo
restricciones_list = []  # Lista para almacenar las restricciones
restriccions=[]
variablesfo = []  # Lista para almacenar los coeficientes de la función objetivo

with open('fo.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()  # Eliminar espacios en blanco al inicio y final de la línea
    if line.startswith("fo"):
        # Línea de la función objetivo
        variablesfo = line.split()[2:-1]  # Extraer los coeficientes de la función objetivo
        variables = len(variablesfo)
        for i in range(0, len(variablesfo)):
            try:
                c=int(variablesfo[i].split("*")[0])
            except:
                c=1
            coeficientes.append(c)
    elif line.startswith("}") or line == "" or line.startswith("sa"):
        # Línea de cierre o línea vacía, ignorar
        continue
    else:
        # Línea de restricción
        res=line
        restriccion = res.split()[1:-2]  # Extraer los coeficientes de la restricción
        restriccions=[]
        for i in range(0,len(restriccion),2):
            try:
                r=int(restriccion[i].split("*")[0])
            except:
                r=1
            restriccions.append(r)
        res = line.split(restriccion[len(restriccion)-1])
        restriccions.append(res[1][1:-1])
        restricciones_list.append(restriccions)
        restricciones += 1
# Imprimir el número de variables
print(variables)
# Imprimir el número de restricciones
print(restricciones)
# Imprimir los coeficientes de la función objetivo
cadena = ' '.join(str(elemento) for elemento in coeficientes)
print(cadena)

# Imprimir las restricciones
for restriccion in restricciones_list:
    cadena = ' '.join(str(elemento) for elemento in restriccion)
    print(cadena)
