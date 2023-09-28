import tabula
import PyPDF2


# Ruta al archivo PDF
archivo_pdf = "boe_tipo_2.pdf"

# Obtén la lista de páginas del PDF
#lista_de_paginas = tabula.read_pdf(archivo_pdf, pages="all", silent=True)

# El número total de páginas es la longitud de la lista
#total_de_paginas = len(lista_de_paginas)

#print("Total de paginas {}".format(total_de_paginas))

#df = tabula.read_pdf(archivo_pdf, pages=6,silent=True)

import PyPDF2

# Ruta al archivo PDF
archivo_pdf = archivo_pdf

# Abre el archivo PDF en modo lectura binaria

def num_paginas(archivo_pdf):
    """
    Esta bien. Con Libreria PyPDf
    """
    
    with open(archivo_pdf, 'rb') as pdf_file:
        # Crea un objeto PdfFileReader para leer el PDF
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        # Obtiene el número total de páginas del PDF
        total_de_paginas = pdf_reader.numPages
        print(f"El numero de paginas es {total_de_paginas}")
        return total_de_paginas
    

#num_paginas = num_paginas(archivo_pdf)


def determine_pages(archivo_pdf):
    """
    Esta bien. Con libreria tabula
    """
    contador_pags = 0
    
    for i in range(1,1000):
        try:
            with open(archivo_pdf, "rb") as f:
                contador_pags = contador_pags + 1
                table = tabula.read_pdf(f, pages=i)
                table_str = str(table)
            
        except Exception as e:
            contador_pags = contador_pags - 1
            break

    return contador_pags



def find_strings_in_order(surname_1,surname_2,name,text):
    
    surname_1_char_position = text.find(surname_1)
    surname_2_char_position = text.find(surname_2)
    name_char_position = text.find(name)
    
    if surname_1_char_position != -1 and surname_2_char_position != -1 and name_char_position != -1:
        print("Encontrados los apellidos y nombres")
        if surname_1_char_position < surname_2_char_position < name_char_position:
            print("Encontrados apellidos y nombre en el orden buscado")
            return True 
        else:
            print("Apellidos y nombres encontrados pero en otro orden")
            return False
    else:
        print("Alguno de los datos no ha sido encontrado, por lo tanto no nos sirve")
        return False

#TODO Crear funcion para leer cada pagina como un string, y entonces buscar los apellidos y nombres en orden. Podemos usar expresiones regulares o simplemente hacer una busqueda como una cadena teniendo en cuenta en que posicion del string estan
#pages = determine_pages(archivo_pdf)
#print(f"El numero de paginas es {pages}")
surname_1 = "MATEO"
surname_2 = "SANZ"
name = "BEATRIZ"

# Vamos a recorrer el pdf
paginas = determine_pages(archivo_pdf)
print(f"El numero de paginas del documento es {paginas}")


finded_pages_counter = 0
for pagina in range(1,paginas + 1):
    try:
        with open(archivo_pdf, "rb") as f:
            finded_pages_counter = finded_pages_counter + 1
            table = tabula.read_pdf(f, pages=pagina)
            table_str = str(table)
            find_strings = find_strings_in_order(surname_1,surname_2,name,table_str)
            if find_strings:
                print(f"Notificacion de que la persona {surname_1} {surname_2} {name} tiene una entrada en el boe en la pagina {pagina}")
                finded_pages_counter = finded_pages_counter + 1
            else:
                print(f" {surname_1} {surname_2} {name} NO ENCONTRADO en la pagina {pagina}")
            
    except Exception as e:
            print(e)
            break
        
print("\n\n\n*******\n\n\n")
if finded_pages_counter == 0:
    print("No se encontraron apellidos y nombres en el boe para el usuario " + surname_1 + " " + surname_2 + " " + name)
else:
    print("Se encontraron apellidos y nombres en el boe para el usuario " + surname_1 + " " + surname_2 + " " + name)




    
    
    
