import os
from pathlib import Path


import yaml
import shutil

try:
    ruta_config = os.path.join(os.path.dirname(__file__),"..","Config", "default.yaml")

    #Leer la configuración del Yaml
    with open(ruta_config, "r") as f:
        config = yaml.safe_load(f)
except Exception as e:
    print(f"Error al leer la configuración: {e}")
    exit(1)

path = Path.home() / "Desktop"

for categoria, sufijos in config.items():
    carpeta_destino = path / categoria.capitalize()
    carpeta_destino.mkdir(exist_ok=True)
    for archivo in path.iterdir():
        if (archivo.is_file() and archivo.suffix.lower() in sufijos and archivo.parent != carpeta_destino):
            try:
                shutil.move(str(archivo), str(carpeta_destino / archivo.name))
                print(f"{archivo.name} -> {carpeta_destino}")
            except Exception as e:
                print(f"Error al mover {archivo.name}: {e}")
print("Archivos ordenados con éxito")
