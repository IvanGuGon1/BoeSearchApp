import re
import shutil
import PyPDF2
import tabula
import sys
import os
import datetime
import requests
from unidecode import unidecode
from typing import Tuple

#matchings = re.findall(r"**\d{2}/\d{2}/\d{4}.*df", text)

#print(matchings)



def get_date() -> Tuple[str, str, str]:
    """
    Get the current date and return it as a tuple of strings.

    Returns:
        Tuple[str, str, str]: A tuple containing the day, month, and year as strings.
    """
    fecha_actual = datetime.datetime.now()
    fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
    day = fecha_formateada.split("/")[0]
    month = fecha_formateada.split("/")[1]
    year = fecha_formateada.split("/")[2]
    return day, month, year
    

def get_pdf_url_files(year,month,day):

    boe_url_string = f"https://www.boe.es/boe/dias/{year}/{month}/{day}/"
    page  = requests.get(boe_url_string)
    
    if page.status_code == 200:
        text = page.text 
        pdf_url_files_list = []
        for line in text.splitlines():
            if f"/boe/dias/{year}/{month}/{day}/pdfs" in line:
                patron = re.compile(r"BOE-[A-Z]-\d{4}-\d{5}.pdf")
                if len(patron.findall(line)) > 0:
                    file_str_extract = patron.findall(line)[0]
                    url = f"https://www.boe.es/boe/dias/{year}/{month}/{day}/pdfs/{file_str_extract}"
                    #print(url)
                    pdf_url_files_list.append(url)
        print(f"La url boe_url_string {boe_url_string} da ha sido encontrada: {page.status_code}")
    else:
        print(f"La url boe_url_string {boe_url_string} da error {page.status_code}")
        return None
                
    return pdf_url_files_list

def get_webpage_text(boe_url_string):
    
    page  = requests.get(boe_url_string)
    return page.text


def download_pdf_files(url,path):
    
    destino = path + "/" + url.split("/")[-1]

    response = requests.get(url)
    if response.status_code == 200:
        with open(destino, 'wb') as file:
            file.write(response.content)
        print(f"Archivo descargado como '{destino}'")
    else:
        print(f"No se pudo descargar el archivo. Código de estado: {response.status_code}")
    
    return response.status_code



def add_today_files_path():
    import datetime
    import os 
    import shutil
    # Obtener la fecha actual y la fecha de ayer
    fecha_actual = datetime.date.today()
    fecha_ayer = fecha_actual - datetime.timedelta(days=1)

    # Formatear las fechas como cadenas (por ejemplo, "2023-09-26")
    fecha_actual_formateada = fecha_actual.strftime("%Y-%m-%d")
    fecha_ayer_formateada = fecha_ayer.strftime("%Y-%m-%d")
    full_path_today = os.path.abspath(os.path.join("files",fecha_actual_formateada))
    full_path_yesterday = os.path.abspath(os.path.join("files",fecha_ayer_formateada))
    # Crear el directorio con la fecha de hoy (si no existe)
    if not os.path.exists(full_path_today):
        try:
            os.mkdir(full_path_today)
            print(f"Directorio '{full_path_today}' creado con éxito.")
        except Exception as e:
            print(f"No se pudo crear el directorio '{full_path_today}': {e}")
    # Borrar el directorio con la fecha de ayer (si existe)
    if os.path.exists(full_path_yesterday):
      
        try:
            shutil.rmtree(full_path_yesterday)
            print(f"Directorio '{full_path_yesterday}' eliminado con éxito.")
        except Exception as e:
            print(f"Problema al eliminar directorio {full_path_yesterday} , excepcion {e}")
            
    # Obtener la dirección absoluta del directorio creado
    #directorio_absoluto = os.path.abspath(fecha_actual_formateada)
    # Retornar la dirección absoluta
    return full_path_today


def read_local_pdf_files(path):

    # Directorio que deseas leer
    directorio = path

    # Obtén una lista de todos los archivos en el directorio
    archivos = os.listdir(directorio)
    file_list = []
    # Itera sobre la lista de archivos
    for archivo in archivos:
        # Verifica si el elemento en la lista es un archivo (no es un directorio)
        if os.path.isfile(os.path.join(directorio, archivo)):
            # Procesa el archivo aquí
            print("Nombre del archivo:", archivo)
            file_list.append(os.path.join(directorio, archivo))
    
    return file_list

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

def find_person_in_boe(surname_1,surname_2,name,file_path):
    """
    Lo dejo por si necesitamos esta lógica mas adelante para comprobar cual encontramos primero. Usar findall mejor.
    """
    paginas = num_paginas(file_path)
    print(f"El fichero boe_tipo_1.pdf Tiene este numero de paginas del documento es {paginas}")
    finded_pages_counter = 0
    for pagina in range(1,paginas+1):
        print(f"Acceso a pagina: {pagina}")
        try:
            with open(file_path, "rb") as f:
                finded_pages_counter = finded_pages_counter + 1
                table = tabula.read_pdf(f, pages=pagina)
                table_str = str(table)
                find_strings = find_strings_in_order(surname_1,surname_2,name,table_str)
                if find_strings:
                    print("\n\n******\n\n")
                    print(f"Notificacion de que la persona {surname_1} {surname_2} {name} tiene una entrada en el boe en la pagina {pagina}")
                    finded_pages_counter = finded_pages_counter + 1
                    return True
                else:
                    print(f" {surname_1} {surname_2} {name} NO ENCONTRADO en la pagina {pagina}")
                    return False
                    #print(f" {surname_1} {surname_2} {name} NO ENCONTRADO en la pagina {pagina}")
                    #print(f" {surname_1} {surname_2} {name} NO ENCONTRADO en la pagina {pagina}")
        except Exception as e:
            print(e)
            break
        

def transform_unidecode_string(string):

    return unidecode(string).upper()


def search_strings_in_pdf(file_path,surname_1,surname_2,name):
    """
    Esta es la que escogemos
    """
    
    with open(file_path, 'rb') as pdf_file:
        # Crea un objeto PdfFileReader para leer el archivo PDF
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Verifica si el archivo PDF se puede leer correctamente
        if pdf_reader.isEncrypted:
            pdf_reader.decrypt("")  # Si el PDF está protegido con contraseña, proporciónala aquí

        # Imprime el número de páginas en el PDF
        num_paginas = pdf_reader.numPages
        print(f"El PDF tiene con rut {file_path} {num_paginas} páginas.")

        # Lee el contenido de todas las páginas del PDF
        
        surname_1 = transform_unidecode_string(surname_1)
        surname_2 = transform_unidecode_string(surname_2)
        name = transform_unidecode_string(name)
        
        finded = False
        for pagina_numero in range(num_paginas):
            pagina = pdf_reader.getPage(pagina_numero)
            texto = transform_unidecode_string(pagina.extractText())
            """
            patron = rf"\b{surname_1}\b.*\b{surname_2}\b.*\b{name}\b"
            coincidencias = re.search(patron, texto)
            
            if coincidencias:
                finded = True
                print("****************")
                print(f"Encontrados los apellidos y nombres {surname_1} {surname_2} {name} pagina {pagina_numero}")
                print("****************")
            else:
                pass
                #print("No se encontró la combinación de apellidos y nombre en el texto.")
            """
            
            """
            surname_1_pattern = r'\b' + re.escape(surname_1) + r'\b'
            surname_2_pattern = r'\b' + re.escape(surname_2) + r'\b'
            name_patter = r'\b' + re.escape(name) + r'\b'
   
            if re.search(surname_1_pattern,texto) and re.search(surname_2_pattern,texto) and re.search(name_patter,texto):
                print("****************")
                print(f"Encontrados los apellidos y nombres {surname_1} {surname_2} {name} pagina {pagina_numero}")
                print("****************")
                finded = True
            """

            if surname_1 in texto and surname_2 in texto and name in texto:
                # Logica repetida, la dejo por si decido implementar el orden en el que encuentro nombre y apellidos. Find me devuelve la posicion del caracter
                surname_1_char_position = texto.find(surname_1)
                surname_2_char_position = texto.find(surname_2)
                name_char_position = texto.find(name)
                
                if surname_1_char_position != -1 and surname_2_char_position != -1 and name_char_position != -1:
                    if surname_1_char_position < surname_2_char_position < name_char_position:
                        #print(f"Encontrados los apellidos y nombres {surname_1} {surname_2} {name}")
                        finded = True
    return finded 

if __name__ == "__main__":
        # Verifica si se proporcionaron los tres argumentos esperados
    """
    Scripg logico de prueba
    
    if len(sys.argv) != 4:
        print("Uso: python script.py <Apellido1> <Apellido2> <Nombre>")
        sys.exit(1)
    
    # Lee los argumentos de la línea de comandos
    surname_1 = transform_unidecode_string(sys.argv[1])
    surname_2 = transform_unidecode_string(sys.argv[2])
    name = transform_unidecode_string(sys.argv[3])
    """
    surname_1 = "MARTIN"
    surname_2 = "GUERRERO"
    name = "IVAN"
    """
    Prueba de funcion get_date
    """
    print("\n\n   Prueba de funcion get_date \n\n")
    print(get_date())
    day,month,year = get_date()
    
    """
    Prueba de funcion get_pdf_url_files
    """
    print("\n\n   Prueba de funcion get_pdf_url_files \n\n")
    pdf_url_files_list = get_pdf_url_files(year,month,day) 
    for pdf_url_file in pdf_url_files_list:
        print(pdf_url_file)
    
    """
    Prueba de funcion add_path
    """
    print("\n\n   Prueba de funcion add_path \n\n")

    today_files_path = add_today_files_path()
    print(today_files_path)
    
    """
    Descargar solo los ficheros que no tenemos descargados. 
    """

    for pdf_url_file in pdf_url_files_list:
        # write a code to check if file exists in directory today_files_path
        if pdf_url_file.split("/")[-1] not in os.listdir(today_files_path):
            download_pdf_files(pdf_url_file,today_files_path)
        else:
            print(f"El archivo {pdf_url_file.split('/')[-1]} ya existe")

    
    """
    Prueba de funcion read_local_pdf_files
    """
    
    print("\n\n   Prueba de funcion read_pdf_files \n\n")
    print("\n\n\n*10")
    
    file_list = read_local_pdf_files(today_files_path)
    for file in file_list:
        print(file)
        person_found = search_strings_in_pdf(file,surname_1,surname_2,name)
        if person_found:
            # Aqui va la logica de la noticificación, enviar a email, telegram etc.....
            print("****************")
            print(f"Encontrados los apellidos y nombres {surname_1} {surname_2} {name} file {file}")
            print("****************")