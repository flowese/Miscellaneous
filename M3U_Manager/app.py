# GESTIONA LOGOS DE CANALES EN ARCHIVOS M3U.
"""Written by: @flowese in 2022."""

import requests # importar libreria para descargar archivos.
import re # importar libreria re para buscar patrones y reemplazar.
import os # importar libreria gestionar ficheros.
import time # importar libreria time para gestionar tiempos.

def leer_listas_m3u(): # Leer listas M3U.
    with open('config/listas.txt', 'r') as listas_file:
        try:        
            listas_text = listas_file.read()
            listas_file.close()
            listas = eval(listas_text)
            return listas
        except:
            print(' (KO) Error al leer el archivo de listas.')
            exit()

def descargar_m3u(url): # Descargar archivo M3U.
    try:
        r = requests.get(url)
        with open('temp.m3u', 'wb') as f:
            f.write(r.content)
            canales = 'temp.m3u'
            # close the file
            f.close()
            print(' (OK) Archivo M3U descargado.')
    except:
        print(' (KO) Error al descargar el archivo M3U.')
        exit()

def leer_canales(): # Leer diccionario de Canales.
    try:   
        with open('config/canales.txt', 'r') as dict_file:
            dict_text = dict_file.read()
            lista_canales = eval(dict_text)
            dict_file.close()
            print(' (OK) Diccionario de canales cargado.')
            return lista_canales
    except:
        print(' (KO) Error al leer el archivo de canales.')
        exit()

def generar_m3u(lista_canales, new_filename): # Procesamineto y generación archivo M3U.
    try:
        with open('temp.m3u', 'r') as input_file:
            input_text = input_file.read()
            for line in input_text.splitlines(): # buscar el canal en el diccionario
                for canal in lista_canales: 
                    if canal in line: # si existe el canal en la linea
                        line = re.sub(r'tvg-logo="[^"]*"', 'tvg-logo="' + lista_canales[canal] + '"', line)# reemplazar con el logo del canal de la lista_canales
                with open(f'output/{new_filename}.m3u', 'a') as output_file: # generamos archivo nuevo y lo cerramos
                    output_file.write(line + '\n')
                output_file.close()
            input_file.close()
            print(' (OK) Archivo M3U generado.')
    except:
        print(' (KO) Error al generar el archivo M3U.')
        exit()

def gestionar_temporales(): # Borrar archivos temporales
    try:  
        os.remove('temp.m3u')
        print(' (OK) Archivos temporales eliminados.')
    except:
        print(' (KO) Error al borrar archivos temporales.')
        exit()


if __name__ == '__main__': # INICIO SCRPIT
    listas_de_usuario = leer_listas_m3u() # 1. Leer listas M3U de listas.txt.
    for usuarios in listas_de_usuario: # 2. Descargar archivo M3U de las listas.
        tiempo_inicio = time.time()
        print(f'\n[{usuarios}]')
        url = listas_de_usuario[usuarios]
        descargar_m3u(url)
        lista_canales = leer_canales() # 3. Leer diccionario de canales.
        generar_m3u(lista_canales, usuarios) # 4. Procesar y generar archivo M3U.
        gestionar_temporales() # 5. Borrar archivos temporales.
        tiempo_fin = time.time()
        # tiempo_total as integer
        tiempo_total = int(tiempo_fin - tiempo_inicio)
        print(f' (OK) Proceso finalizado en {tiempo_total} segundos.')
