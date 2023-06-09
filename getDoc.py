import re
openedFor = [False, 0]
openedIf = [False, False, 0]
openedElse = [False, 0]
latestOpened = []
finishedConditional = True


def translate(filename):
    with open(filename, 'r') as lines:
        for line in lines:
            if line.startswith("para"):
                pattern = r'(\d+)'  # Expresión regular para encontrar números
                numbers = re.findall(pattern, line)
                openedFor[0] = True
                openedFor[1] += 1
                latestOpened.append("for")
                continue
            if line.startswith("si "):
                # Extrae la condición sin los caracteres "si " y "{"
                condition = line[3:-2]
                if eval(condition):
                    # Si la condición es verdadera, ejecuta el bloque de código dentro del if
                    # Extrae el siguiente bloque de código
                    code_block = lines[lines.index(line)+1:lines.index(line)+2]
                    assignment = code_block[0].split("=")
                    variable = assignment[0].strip()
                    value = assignment[1].strip()
                    # Actualiza el valor de la variable
                    locals()[variable] = eval(value)
                elif line.startswith("si_no"):
                    # Si no se cumple la condición anterior, ejecuta el bloque de código dentro del else
                    # Extrae el siguiente bloque de código
                    code_block = lines[lines.index(line)+1:lines.index(line)+2]
                    assignment = code_block[0].split("=")
                    variable = assignment[0].strip()
                    value = assignment[1].strip()
                    # Actualiza el valor de la variable
                    locals()[variable] = eval(value)

            if line.startswith("}"):
                latest = latestOpened.pop()
                if latest == "for":
                    openedFor[1] -= 1
                elif latest == "if":
                    openedIf[2] -= 1
                    finishedConditional = openedIf[1].pop()
                elif latest == "else":
                    pass


def extract_code_blocks(text):
    start_index = text.find("{")
    end_index = text.find("}")
    while start_index != -1 and end_index != -1:
        code_block = text[start_index+1:end_index]  # Excluir las llaves
        print(code_block)
        text = text[end_index+1:]
        start_index = text.find("{")
        end_index = text.find("}")
