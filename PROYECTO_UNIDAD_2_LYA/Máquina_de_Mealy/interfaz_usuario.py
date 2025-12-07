# interfaz_usuario.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from definiciones import Input, PRODUCTOS
from maquina import MaquinaDispensadoraMealy
from salidas import set_app
from pantalla_grafo import PantallaGrafo

# -------------------------
# Directorio de imágenes y extensiones soportadas
# -------------------------

IMG_DIR = os.path.join(os.path.dirname(__file__), "IMG")
IMG_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".webp"]

# -------------------------
# Ajustes globales de tamaño de tarjeta (producto)
# -------------------------
CARD_W = 50   # ancho de cada tarjeta 
CARD_H = 130  # alto de cada tarjeta

# -------------------------
# Helper: cargar imagen de producto (busca por varias extensiones)
# -------------------------
# Busca la imagen asociada a un producto según su código
# Revisa varias extensiones posibles (png, jpg, etc.)
# Redimensiona la imagen a un tamaño de miniatura
# Devuelve un objeto PhotoImage para usar en Tkinter

def cargar_imagen_producto(code, thumb_size=(CARD_W-10, 60)):
    for ext in IMG_EXTS:
        path = os.path.join(IMG_DIR, f"{code}{ext}")
        if os.path.exists(path):
            try:
                img = Image.open(path)
                img.thumbnail(thumb_size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception:
                return None
    return None


# -------------------------
# Pantalla principal (todo en una sola ventana)
# -------------------------
class PantallaMain(tk.Frame):
# Constructor de la pantalla principal
# parent: contenedor padre
# app: referencia a la aplicación principal

    def __init__(self, parent, app):
        super().__init__(parent, bg="#2a2a2a")
        self.app = app
        self.maquina = app.maquina
        self.product_widgets = {}   # diccionario con widgets de cada producto
        self.product_images = {}    # cache de imágenes de productos

        self._build_layout()         # construir la interfaz


    def _build_layout(self):
        # Construye el layout de la pantalla principal.
        # Divide en dos columnas: Izquierda: grilla de productos (4x4), Derecha: display, keypad, ranura de monedas y bandeja.
        
        
        # --------- Left: grid de productos ----------
        left = tk.Frame(self, bg="#1f1f1f", padx=12, pady=12)
        left.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        
        right = tk.Frame(self, bg="#222222", padx=12, pady=12)
        right.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
        
        # Configuración de tamaños fijos
        left.config(width=720)  
        left.grid_propagate(False)   # evitar reajustes automáticos que muevan la grilla
        
        right.grid_propagate(False)  # fijar ancho del panel derecho
        right.config(width=360)      # ancho fijo para la columna derecha (ajústalo si quieres)
        
        # Configuración de columnas y filas principales
        self.grid_columnconfigure(0, minsize=600)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Título de la máquina
        tk.Label(left, text="Máquina Expendedora", bg="#1f1f1f", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=(0,8))

        # Frame para la grilla de productos
        grid_frame = tk.Frame(left, bg="#1f1f1f")
        grid_frame.grid_propagate(False)
        grid_frame.pack(expand=True, fill="both")

        letras = ['A', 'B', 'C', 'D']
    
        # configurar las columnas con minsize para que tengan al menos el ancho de la tarjeta
        for r in range(4):
            grid_frame.rowconfigure(r, weight=1, minsize=CARD_H + 8)
            grid_frame.columnconfigure(r, weight=1, minsize=CARD_W + 12)

        # Crear tarjetas A1..D4 con imagen, nombre y precio
        for row in range(4):
            for col in range(4):
                code = f"{letras[row]}{col+1}"

                # Frame de la tarjeta
                card = tk.Frame(grid_frame, bg="#ffffff", bd=1, relief="raised",
                                width=CARD_W, height=CARD_H)
                card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
                card.grid_propagate(False)    # evita que el contenido cambie el tamaño
                card.pack_propagate(False)

                # Código del producto
                lbl_code = tk.Label(card, text=code, anchor="nw", font=("Arial", 9, "bold"), bg="#ffffff")
                lbl_code.place(x=8, y=6)

                # Imagen del producto
                img_holder = tk.Frame(card, bg="#ffffff", width=CARD_W, height=50)
                img_holder.place(x=40, y=25)
                img_holder.pack_propagate(False)
                img_label = tk.Label(img_holder, bg="#ffffff")
                img_label.pack(expand=True)

                # Nombre del producto
                lbl_name = tk.Label(card, text="Nombre", bg="#ffffff", wraplength=80, justify="center")
                lbl_name.place(x=30, y=65)

                # Precio del producto
                lbl_price = tk.Label(card, text="$--", bg="#ffffff", font=("Arial", 10, "bold"))
                lbl_price.place(x=50, y=100)
                
                # Guardar referencias de widgets en diccionario
                self.product_widgets[code] = {
                    "frame": card,
                    "img_label": img_label,
                    "nombre_label": lbl_name,
                    "precio_label": lbl_price,
                    "code_label": lbl_code
                }

        # --------- Right display + keypad + monedero + dispensador ----------
        
        # Display principal (código + info)
        display_wr = tk.Frame(right, bg="#000000", bd=3, relief="sunken",
                      width=360, height=150)
        display_wr.pack_propagate(False) 
        display_wr.pack(fill="x", pady=(0,12))
        
        lbl_title = tk.Label(display_wr, text="DISPLAY", bg="#000000",
                             fg="#00ff66", font=("Consolas", 10, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, sticky="w",
                       padx=6, pady=(6,0))
        
        # -----------------------------
        # Columna izquierda → código seleccionado
        # -----------------------------
        self.display_code_label = tk.Label(
            display_wr,
            text="--",
            bg="#000000",
            fg="#00ff66",
            font=("Consolas", 32, "bold"),
            width=4,
            anchor="center"
        )
        self.display_code_label.grid(row=1, column=0, sticky="nsew",
                                     padx=10, pady=8)
        
        # -----------------------------
        # Columna derecha → información del producto
        # -----------------------------
        self.info_label = tk.Label(
            display_wr,
            text="Seleccione un producto…",
            bg="#000000",
            fg="white",
            width=28,
            height=5,
            font=("Arial", 11),
            justify="left",
            anchor="nw"
        )
        self.info_label.grid(row=1, column=1, sticky="nsew",
                             padx=10, pady=8)
        
        # Configuración de columnas del display 
        display_wr.grid_columnconfigure(0, minsize=140)   
        display_wr.grid_columnconfigure(1, weight=1)     
        
        
        # -------- keypad (Botones de selección) -------
        keypad_wr = tk.Frame(right, bg="#222222")
        keypad_wr.pack(pady=(6,12))

        # Botones de letras (A-D)
        letras_frame = tk.Frame(keypad_wr, bg="#222222")
        letras_frame.pack()
        for letra in ['A', 'B', 'C', 'D']:
            b = tk.Button(letras_frame, text=letra, width=4, height=2,
                          command=lambda L=letra: self._press_letra(L))
            b.pack(side="left", padx=6, pady=6)

        # Botones de números (1-4)
        nums_frame = tk.Frame(keypad_wr, bg="#222222")
        nums_frame.pack()
        for numero in ['1', '2', '3', '4']:
            b = tk.Button(nums_frame, text=numero, width=4, height=2,
                          command=lambda N=numero: self._press_numero(N))
            b.pack(side="left", padx=6, pady=6)

        # Botones acción (Confirmar, Cancelar, Ver Grafo)
        acciones = tk.Frame(right, bg="#222222")
        acciones.pack(pady=(10,12))
        tk.Button(acciones, text="CONFIRMAR", width=12, command=self._confirmar).pack(side="left", padx=6) 
        tk.Button(acciones, text="CANCELAR", width=12, command=lambda: self.maquina.procesar_entrada(Input.CANCELAR)).pack(side="left", padx=6)
        tk.Button(acciones, text="VER GRAFO", width=12, command=self._ver_grafo).pack(side="left", padx=6)

        # -------- Ranura de moneda + botones de valor de moneda ----------
        ranura_box = tk.Frame(right, bg="#111111", bd=2, relief="ridge")
        ranura_box.pack(fill="x", pady=(6,12))
        tk.Label(ranura_box, text="RANURA DE MONEDA", bg="#111111", fg="white").pack(pady=(6,6))

        monedas_wr = tk.Frame(ranura_box, bg="#111111")
        monedas_wr.pack(pady=(4,8))
        # Monedas: $1, $5, $10, $20 (mapea al Input correspondiente)
        monedas = [(1, Input.INSERT_1), (5, Input.INSERT_5), (10, Input.INSERT_10), (20, Input.INSERT_20)]
        for val, inp in monedas:
            btn = tk.Button(monedas_wr, text=f"${val}", width=6,
                            command=lambda I=inp: self._insert_coin(I))
            btn.pack(side="left", padx=6, pady=6)

        # Dispensador de productos / bandeja de salida
        disp = tk.Frame(right, bg="#0b0b0b", bd=2, relief="sunken", height=150)
        disp.pack(fill="x", pady=(6,0))
        disp.pack_propagate(False)
        self.bandeja_label = tk.Label(disp, text="Bandeja de salida", bg="#0b0b0b", fg="white")
        self.bandeja_label.pack(pady=6)
        self.producto_canvas = tk.Canvas(disp, width=220, height=90, bg="#FFFFFF", highlightthickness=0)
        self.producto_canvas.place(relx=0.5, rely=0.7, anchor="center")


    # ----------------- Acciones y utilidades que conectan con la máquina -----------------
    def _press_letra(self, letra):
        # Envía la letra seleccionada a la máquina (Input.LETRA)
        # Actualiza inmediatamente el display con el código parcial
        self.maquina.procesar_entrada(Input.LETRA, letra)
        self._refresh_display_from_machine()

    def _press_numero(self, numero):
        # Envía el número seleccionado a la máquina (Input.NUMERO)
        # Actualiza el display con el código completo si corresponde
        self.maquina.procesar_entrada(Input.NUMERO, numero)
        self._refresh_display_from_machine()

    def _insert_coin(self, input_enum):
        # Envía la acción de insertar moneda a la máquina
        # Actualiza el crédito mostrado en el subdisplay
        self.maquina.procesar_entrada(input_enum)
        self._refresh_display_from_machine()

    def _continuar(self):
        if self.maquina.selected_product:
            self._refresh_display_from_machine()
        else:
            # mostrar mensaje temporal
            self.show_temporary_message("Seleccione un producto primero.", 1200)

    def _ver_grafo(self):
        # Intenta generar el grafo usando Graphviz
        try:
            from salidas import generar_grafo_png
            ruta = generar_grafo_png("grafo_estados")
        except Exception as e:
            ruta = None
            print("[PantallaMain] generar_grafo_png error:", e)

        if ruta and os.path.exists(ruta):
            try:
                # # Cargar la imagen en el frame PantallaGrafo y mostrarlo
                self.app.frames["PantallaGrafo"].cargar_imagen(ruta)
                self.app.mostrar_pantalla("PantallaGrafo")
            except Exception as e:
                # Si Graphviz no está disponible o falla, mostrar mensaje temporal
                print("[PantallaMain] no se pudo mostrar PantallaGrafo:", e)
                self.show_temporary_message("No se pudo mostrar grafo.", 1200)
        else:
            self.show_temporary_message("Graphviz no disponible o error al generar grafo.", 1400)

    def _confirmar(self):
        # Envía la acción de confirmar compra a la máquina
        # Actualiza el display con el resultado (entrega o mensaje)
        self.maquina.procesar_entrada(Input.CONFIRMAR)
        self._refresh_display_from_machine()


    def show_temporary_message(self, msg, ms=1200):
        # Muestra un mensaje temporal en el display derecho
        # Después de 'ms' milisegundos, restaura el texto anterior
        prev = self.info_label.cget("text")
        self.info_label.config(text=msg)
        self.after(ms, lambda: self.info_label.config(text=prev))

    def _refresh_display_from_machine(self):
        # Sincroniza el display con el estado actual de la máquina
        code = self.maquina.selected_code or self.maquina.codigo_buffer or "__"
        prod = self.maquina.selected_product
        credito = self.maquina.credito
        # Display izquierdo: código seleccionado
        self.display_code_label.config(text=code)
        # Display derecho: información del producto y crédito
        if prod:
            self.info_label.config(text=f"{prod['nombre']}\nPrecio: ${prod['precio']}\nIngresado: ${credito}")
        else:
            self.info_label.config(text=f"Ingrese código\nIngresado: ${credito}")

    def refresh_products(self):
        # Refresca las tarjetas de productos desde el catálogo PRODUCTOS
        for code, widgets in self.product_widgets.items():
            prod = PRODUCTOS.get(code)
            if not prod:
                # Si el producto no existe, mostrar valores por defecto
                widgets["nombre_label"].config(text="N/A")
                widgets["precio_label"].config(text="$--")
                continue
            # Actualizar nombre y precio.
            widgets["nombre_label"].config(text=prod["nombre"])
            widgets["precio_label"].config(text=f"${prod['precio']}")

            # Cargar imagen del producto (si existe)
            img = cargar_imagen_producto(code)
            if img:
                widgets["img_label"].config(image=img)
                widgets["img_label"].image = img
                self.product_images[code] = img
            else:
                # Si no hay imagen, limpiar el espacio
                widgets["img_label"].config(image="", text="")

            # Si no hay stock, atenuar la tarjeta con un color distinto
            if prod["stock"] <= 0:
                widgets["frame"].config(bg="#f3adad")   # rojo claro = sin stock
            else:
                widgets["frame"].config(bg="#ffffff")   # blanco = disponible


# -------------------------
# Wrapper App que conecta con salidas.py sin cambiar su lógica
# -------------------------
class VendingMachineApp:
    def __init__(self, root, maquina: MaquinaDispensadoraMealy):
        # Configuración inicial de la ventana principal
        self.root = root
        self.root.title("Máquina Expendedora - Interfaz Integrada")
        self.root.configure(bg="#2a2a2a")
        self.maquina = maquina

        # Contenedor principal donde se apilan los frames (pantallas)
        # Se usa como stack para cambiar entre PantallaMain y PantallaGrafo
        self.container = tk.Frame(root, bg="#2a2a2a")
        self.container.pack(expand=True, fill="both")

        # Crear frames:
        # PantallaMain: vista principal con display, keypad, ranura y bandeja
        # PantallaGrafo: vista separada para mostrar el grafo generado en PNG
        self.frames = {}
        self.frames["PantallaMain"] = PantallaMain(parent=self.container, app=self)
        self.frames["PantallaGrafo"] = PantallaGrafo(parent=self.container, app=self)
       
        # Colocar los frames en la grilla (superpuestos en el mismo espacio)
        # Se usa tkraise() para decidir cuál se muestra
        for f in self.frames.values():
            f.grid(row=0, column=0, sticky="nsew")

        # Registrar la app en salidas.py para que las funciones de salida puedan actualizar la UI
        set_app(self)

        # Inicializar la máquina dentro del app para que salidas puedan acceder a app.maquina
        self.maquina = maquina

        # Inicializar widgets esperados por salidas.py:
        # Algunos métodos de salida esperan labels específicos, aquí se crean alias invisibles o referencias dentro de PantallaMain.
        main = self.frames["PantallaMain"]
        main.total_label = tk.Label(main, text=f"${self.maquina.credito}")  
        main.lbl_producto = None
        main.procesando_label = tk.Label(main, text="", bg="#111", fg="white")
        main.cambio_label = tk.Label(main, text="", bg="#111", fg="white")

        # Mostrar la pantalla principal
        self.mostrar_pantalla("PantallaMain")

        # Refrescar productos visuales (nombres, precios, imagenes, stock)
        main.refresh_products()

        # Registrar app en salidas
        set_app(self)

    # Mostrar pantalla:
    # Normaliza nombres y decide qué frame levantar
    # Por compatibilidad, cualquier nombre distinto a PantallaGrafo muestra PantallaMain
    def mostrar_pantalla(self, page_name):
        if page_name in ("PantallaGrafo", "PantallaGrafo"):
            frame = self.frames.get("PantallaGrafo")
        else:
            frame = self.frames.get("PantallaMain")
        if frame:
            frame.tkraise()

    # Métodos auxiliares que pueden usarse desde UI 
    def ingresar_letra(self, letra):
        #Envia la letra seleccionada a la maquina
        self.maquina.procesar_entrada(Input.LETRA, letra)

    def ingresar_numero(self, numero):
        #Envia el numero seleccionado a la maquina
        self.maquina.procesar_entrada(Input.NUMERO, numero)

    def insertar_moneda(self, valor):
        # Mapea el valor de la moneda al Input correspondiente y lo envía a la máquina
        mapping = {1: Input.INSERT_1, 5: Input.INSERT_5, 10: Input.INSERT_10, 20: Input.INSERT_20}
        inp = mapping.get(valor)
        if inp:
            self.maquina.procesar_entrada(inp)
    
    

# -------------------------
# MAIN: si ejecutas interfaz_usuario.py directamente
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()                              # Crear ventana principal
    maquina = MaquinaDispensadoraMealy()        # Instanciar la máquina expendedora
    app = VendingMachineApp(root, maquina)      # Crear la aplicación con la UI integrada
    root.geometry("1100x700")                   # Establecer tamaño de la ventana  
    root.mainloop()                             # Iniciar el loop principal de Tkinter
