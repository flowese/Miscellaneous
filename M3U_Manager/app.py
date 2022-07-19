# GESTIONA LOGOS DE CANALES EN ARCHIVOS M3U.
"""Written by: @flowese in 2022."""

import requests # importar libreria para descargar archivos.
import re # importar libreria re para buscar patrones y reemplazar.
import os # importar libreria gestionar ficheros.
import time # importar libreria time para gestionar tiempos.

listas_path = 'config/listas.txt'
canales_path = 'config/canales.txt'
output_dir = 'output/'

def leer_listas_m3u(): # Leer listas M3U.
    with open(listas_path, 'r') as listas_file: 
        listas_text = listas_file.read()
        listas_file.close()
        listas = eval(listas_text)
        return listas

def leer_canales(): # Leer diccionario de Canales.
    with open(canales_path, 'r') as dict_file:
        dict_text = dict_file.read()
        lista_canales = eval(dict_text)
        dict_file.close()
        print(' (OK) Diccionario de canales cargado.')
        return lista_canales

def descargar_m3u(url): # Descargar archivo M3U.
    r = requests.get(url)
    with open('temp.m3u', 'wb') as f:
        f.write(r.content)
        # close the file
        f.close()
        print(' (OK) Archivo M3U descargado.')

def generar_m3u(lista_canales, new_filename): # Procesamineto y generación archivo M3U.
    with open('temp.m3u', 'r') as f:
        # read the file line by line
        lines = f.readlines()
        # loop through the lines
        for i, line in enumerate(lines):
            # if the line contains the tvg-name tag
            if 'tvg-name' in line:
                # search content for the tvg-name tag
                tvg_name = re.search(r'tvg-name="(.*?)"', line).group(1)
                # if the tvg-name tag is in the list of channels
                if tvg_name in lista_canales:
                    # replace the tvg-logo tag with the correct logo
                    lines[i] = re.sub(r'tvg-logo="(.*?)"', r'tvg-logo="{}"'.format(lista_canales[tvg_name]), line)
        # write the new file with the correct logos on output/
        with open(f'{output_dir}{new_filename}.m3u', 'w') as f:
            f.writelines(lines)
            f.close()
            print(' (OK) Archivo M3U generado.')

if  __name__ == '__main__':
    # 1. Leer diccionario de listas m3u.
    diccionario_listas = leer_listas_m3u()
    # 2. Leer diccionario de canales.
    diccionario_canales = leer_canales()
    # 3. Para cada usuario, descargar archivo m3u y generar archivo m3u.
    for usuario, url_m3u in diccionario_listas.items():
        descargar_m3u(url_m3u)
        generar_m3u(diccionario_canales, usuario)
        # 4. Borrar archivo temporal.
        os.remove('temp.m3u')
