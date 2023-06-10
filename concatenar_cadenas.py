def concatenar_cadenas(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        
    resultado = []
    cadena_actual = ""
    
    for linea in lineas:
        if linea.startswith("fo ") or linea.startswith("Si ") or linea.startswith("para "):
            if cadena_actual:
                resultado.append(cadena_actual.strip())
            cadena_actual = linea.strip()
        else:
            cadena_actual += linea.strip()
    
    if cadena_actual:
        resultado.append(cadena_actual.strip())
    
    with open("concatenado.txt", 'w') as archivo:
        archivo.write('\n'.join(resultado))
    # return '\n'.join(resultado)
    