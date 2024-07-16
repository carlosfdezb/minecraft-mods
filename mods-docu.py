import zipfile
import os
import toml
import urllib.parse
import socket

contenido_md = """
# Listado de MODS
"""
nombre_archivo = "README.md"

with open(nombre_archivo, 'w') as archivo:
    archivo.write(contenido_md)

jar_paths = [f for f in os.listdir('./') if f.endswith('.jar')]

toml_filename = 'META-INF/mods.toml'

for jar_path in jar_paths:
    with zipfile.ZipFile(jar_path, 'r') as jar:
        with jar.open(toml_filename) as toml_file:
            toml_content = toml_file.read().decode('utf-8')

            # Parsear el contenido TOML
            data = toml.loads(toml_content)
            # print(data)
            if 'mods' in data and 'displayName' in data['mods'][0]:
                nombre_mod = data['mods'][0]['displayName']
                # print(nombre_mod)
            url_mod = None
            if 'mods' in data and 'displayURL' in data['mods'][0]:
                url_mod = data['mods'][0]['displayURL']
                # print(url_mod)
                
            contenido_md = """
- ### """+nombre_mod
            with open(nombre_archivo, 'a') as archivo:
                archivo.write(contenido_md)
                
            if url_mod:
                parsed_url = urllib.parse.urlparse(url_mod)
                dominio = parsed_url.netloc
                contenido_md = """
    link: ["""+dominio+"""]("""+url_mod+""")
"""
                with open(nombre_archivo, 'a') as archivo:
                    archivo.write(contenido_md)
