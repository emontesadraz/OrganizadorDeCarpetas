import os
from pathlib import Path
import yaml
import shutil
import sys
import tkinter as tk
from tkinter import messagebox, filedialog


def resource_path(relative_path: str) -> Path:
    """Devuelve la ruta absoluta tanto en desarrollo como en ejecutable (PyInstaller)."""
    if hasattr(sys, "_MEIPASS"):  # cuando se ejecuta como binario
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent.parent / relative_path

def organizar_archivos(ruta_usuario, text_resultado):
    try:
        ruta_config = resource_path("Config/default.yaml")
        with open(ruta_config, "r") as f:
            config = yaml.safe_load(f)

    except Exception as e:
        messagebox.showerror("Error", f"Error al leer la configuración: {e}")
        return

    path = Path(ruta_usuario).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        messagebox.showerror("Error", f"El directorio {ruta_usuario} no existe")
        return

    movimientos = []
    for categoria, sufijos in config.items():
        archivos_categoria = [
            archivo for archivo in path.iterdir()
            if archivo.is_file() and archivo.suffix.lower() in sufijos and archivo.parent == path
        ]
        if archivos_categoria:
            carpeta_destino = path / categoria.capitalize()
            carpeta_destino.mkdir(exist_ok=True)
            for archivo in archivos_categoria:
                try:
                    shutil.move(str(archivo), str(carpeta_destino / archivo.name))
                    movimientos.append(f"{archivo.name} → {carpeta_destino.name}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al mover {archivo.name}: {e}")
    text_resultado.config(state=tk.NORMAL)
    text_resultado.delete(1.0, tk.END)
    if movimientos:
        text_resultado.insert(tk.END, "\n".join(movimientos))
        messagebox.showinfo("Éxito", "Archivos ordenados con éxito")
    else:
        text_resultado.insert(tk.END, "No se movió ningún archivo")
    text_resultado.config(state=tk.DISABLED)


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

    frame_resultado = tk.Frame(root)
    frame_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
    text_resultado = tk.Text(frame_resultado, width=60, height=10, state=tk.DISABLED)
    scrollbar = tk.Scrollbar(frame_resultado, command=text_resultado.yview)
    text_resultado.config(yscrollcommand=scrollbar.set)
    text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Button(root, text="Organizar", command=lambda: organizar_archivos(entry_ruta.get(), text_resultado)).pack(
        padx=10, pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
