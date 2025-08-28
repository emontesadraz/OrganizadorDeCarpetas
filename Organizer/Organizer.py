import os
from pathlib import Path
import yaml
import shutil

ruta_config = os.path.join(os.path.dirname(__file__),"..","Config", "default.yaml")

#Leer la configuración del Yaml
with open(ruta_config, "r") as f:
    config = yaml.safe_load(f)

escritorio = Path.home() / "Downloads"

for categoria, sufijos in config.items():
    carpeta_destino = escritorio / categoria.capitalize()
    carpeta_destino.mkdir(exist_ok=True)
    for archivo in escritorio.iterdir():
        if archivo.is_file() and archivo.suffix.lower() in sufijos:
            shutil.move(str(archivo), str(carpeta_destino / archivo.name))
    print("Archivos ordenados con éxito")

print (Path.home())
