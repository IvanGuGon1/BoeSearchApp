import sys
def transform_unidecode_string(string):
    from unidecode import unidecode
    return unidecode(string).upper()

def procesar_nombre_apellidos(apellido1, apellido2, nombre):
    
    apellido1 = transform_unidecode_string(apellido1)
    apellido2 = transform_unidecode_string(apellido2)
    nombre = transform_unidecode_string(nombre)
    # Realiza cualquier operación que desees con los argumentos
    nombre_completo = f"{nombre} {apellido1} {apellido2}"
    
    return nombre_completo

if __name__ == "__main__":
    # Verifica si se proporcionaron los tres argumentos esperados
    if len(sys.argv) != 4:
        print("Uso: python script.py <Apellido1> <Apellido2> <Nombre>")
        sys.exit(1)

    # Lee los argumentos de la línea de comandos
    apellido1 = sys.argv[1]
    apellido2 = sys.argv[2]
    nombre = sys.argv[3]

    # Llama a la función para procesar los argumentos
    nombre_completo = procesar_nombre_apellidos(apellido1, apellido2, nombre)

    # Imprime el resultado
    print("Nombre completo:", nombre_completo)