# pantalla_grafo.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from graphviz import Digraph
import os

# Clase PantallaGrafo
# -----------------------------
# Esta pantalla muestra el grafo de estados de la compra
# Incluye: Un título ("Grafo de la compra"), Un Label (self.canvas) donde se cargará la imagen del grafo, Un botón "Volver" que regresa a la pantalla principal 
# Método cargar_imagen(ruta): Abre la imagen desde la ruta indicada, Redimensiona la imagen, Convierte la imagen a formato compatible con Tkinter (PhotoImage), Actualiza el Label self.canvas para mostrar la imagen
# Si ocurre un error al cargar la imagen, lo muestra en consola.


class PantallaGrafo(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        tk.Label(self, text="Grafo de la compra", font=("Arial", 16)).pack(pady=10)

        self.canvas = tk.Label(self)  # donde pondremos la imagen
        self.canvas.pack(pady=10)

        tk.Button(self, text="Volver",
                  command=lambda: self.app.mostrar_pantalla("PantallaMain")
        ).pack(pady=10)

    def cargar_imagen(self, ruta):
        try:
            from PIL import Image, ImageTk
            img = Image.open(ruta)
            img = img.resize((900, 300))
            self.img_tk = ImageTk.PhotoImage(img)
            self.canvas.config(image=self.img_tk)
        except Exception as e:
            print("[PantallaGrafo] Error al cargar imagen:", e)
