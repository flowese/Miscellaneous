import re # importar libreria re para buscar patrones y reemplazar.

output_dir = 'output/'
filename = f'{output_dir}ejemplo.m3u'

def filtrar_m3u(): # Procesamineto y generación archivo M3U.
    with open(filename, 'r') as input_file:
        input_text = input_file.read()
        for line in input_text.splitlines(): # buscar el canal en el diccionario
            # search |ES| string in line if exists print tvg-name=""
            if '|ES|' in line:
                # print only tvg-name="<string>"
                canales_spain = re.search(r'tvg-name="([^"]*)"', line).group(1)
                # write search on canalones.txt
                with open(f'{output_dir}canales_filtrados.txt', 'a') as output_file:
                    output_file.write(canales_spain + '\n')
                    # close the file
                    output_file.close()

if __name__ == '__main__':
    filtrar_m3u()
    print('Proceso finalizado.')
