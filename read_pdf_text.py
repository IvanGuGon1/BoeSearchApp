
def transform_unidecode_string(string):
    from unidecode import unidecode
    
    return unidecode(string).upper()


def search_strings_in_pdf(file_path,surname_1,surname_2,name):
    import PyPDF2
    
    with open(file_path, 'rb') as pdf_file:
        # Crea un objeto PdfFileReader para leer el archivo PDF
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Verifica si el archivo PDF se puede leer correctamente
        if pdf_reader.isEncrypted:
            pdf_reader.decrypt("")  # Si el PDF está protegido con contraseña, proporciónala aquí

        # Imprime el número de páginas en el PDF
        num_paginas = pdf_reader.numPages
        print(f"El PDF tiene {num_paginas} páginas.")

        # Lee el contenido de todas las páginas del PDF
        
        surname_1 = transform_unidecode_string(surname_1)
        surname_2 = transform_unidecode_string(surname_2)
        name = transform_unidecode_string(name)
        
        finded = False
        for pagina_numero in range(num_paginas):
            pagina = pdf_reader.getPage(pagina_numero)
            texto = transform_unidecode_string(pagina.extractText())
            
            if surname_1 in texto and surname_2 in texto and name in texto:
                # Logica repetida, la dejo por si decido implementar el orden en el que encuentro nombre y apellidos. Find me devuelve la posicion del caracter
                surname_1_char_position = texto.find(surname_1)
                surname_2_char_position = texto.find(surname_2)
                name_char_position = texto.find(name)
                
                if surname_1_char_position != -1 and surname_2_char_position != -1 and name_char_position != -1:
                    print(f"Encontrados los apellidos y nombres {surname_1} {surname_2} {name}")
                    finded = True
                    
    return finded 
    
    
    
    
if __name__ == "__main__":
    
    search_strings_in_pdf('boe_tipo_4.pdf','MARTIN','GUERRERO','IVAN')
    

    
   