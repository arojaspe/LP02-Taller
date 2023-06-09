def extract_code_blocks(text):
    start_index = text.find("{")
    end_index = text.find("}")
    while start_index != -1 and end_index != -1:
        code_block = text[start_index+1:end_index]  # Excluir las llaves
        print(code_block)
        text = text[end_index+1:]
        start_index = text.find("{")
        end_index = text.find("}")


# Ejemplo de texto
text = """
if condition {
    statement1;
    statement2;
}

for i in range(5) {
    statement3;
    statement4;
}

while condition {
    statement5;
    statement6;
}
"""

# Extraer bloques de código
extract_code_blocks(text)
