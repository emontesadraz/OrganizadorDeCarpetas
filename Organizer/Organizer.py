import os
from pathlib import Path
import yaml
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

def organizar_archivos(ruta_usuario):
    try:
        ruta_config = os.path.join(os.path.dirname(__file__), "..", "Config", "default.yaml")
        with open(ruta_config, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer la configuración: {e}")
        return

    path = Path(ruta_usuario).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        messagebox.showerror("Error", f"El directorio {ruta_usuario} no existe")
        return

    for categoria, sufijos in config.items():
        carpeta_destino = path / categoria.capitalize()
        carpeta_destino.mkdir(exist_ok=True)
        for archivo in path.iterdir():
            if archivo.is_file() and archivo.suffix.lower() in sufijos and archivo.parent != carpeta_destino:
                try:
                    shutil.move(str(archivo), str(carpeta_destino / archivo.name))
                except Exception as e:
                    messagebox.showerror("Error", f"Error al mover {archivo.name}: {e}")
    messagebox.showinfo("Éxito", "Archivos ordenados con éxito")

def main():
    root = tk.Tk()
    root.title("Organizador de Archivos")

    tk.Label(root, text="Ruta del directorio a ordenar:").pack(padx=10, pady=5)
    entry_ruta = tk.Entry(root, width=50)
    entry_ruta.pack(padx=10, pady=5)

    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            entry_ruta.delete(0, tk.END)
            entry_ruta.insert(0, carpeta)

    tk.Button(root, text="Seleccionar carpeta...", command=seleccionar_carpeta).pack(padx=10, pady=5)
    tk.Button(root, text="Organizar", command=lambda: organizar_archivos(entry_ruta.get())).pack(padx=10, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()