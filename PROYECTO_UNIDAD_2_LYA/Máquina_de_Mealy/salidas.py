# salidas.py
from definiciones import Output
import os
import tkinter as tk

# forzar ruta de Graphviz
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

# Graphviz libreria para generar el grafo
try:
    from graphviz import Digraph
    _GRAPHVIZ_OK = True
except Exception:
    _GRAPHVIZ_OK = False
    print("[salidas] aviso: graphviz no disponible.")

# -----------------------------
# REGISTRO DE APP
# -----------------------------
# _app: variable global que guarda la referencia a la aplicación principal
# set_app(app): registra la instancia de la aplicación para que las funciones de salida puedan acceder a la UI
# _call_ui(fn): ejecuta de forma segura una función de actualización de la interfaz
# Si la app está registrada, corre la función y captura errores
# Si no hay app registrada, muestra un aviso en consola

_app = None 

def set_app(app): 
    global _app
    _app = app

def _call_ui(fn): 
    if _app:
        try:
            fn()
        except Exception as e:
            print("[salidas] error UI:", e)
    else:
        print("[salidas] UI no registrada")


# -----------------------------
# Generar grafo PNG
# -----------------------------
# Esta función construye y exporta un grafo de estados de la máquina expendedora
# Usa Graphviz para definir nodos (estados) y aristas (transiciones)
# Cada estado se dibuja con un color distinto para facilitar la lectura
# Las transiciones muestran la entrada y la salida asociada
# El grafo se guarda como archivo PNG en la ruta indicada
# Parámetros: nombre_archivo: nombre base del archivo de salida (por defecto "grafo_estados")
# Retorna: Ruta del archivo PNG generado, o None si ocurre un error

def generar_grafo_png(nombre_archivo="grafo_estados"):
    if not _GRAPHVIZ_OK:
        return None
    try:
        dot = Digraph(comment="Máquina Expendedora")
        dot.attr(dpi="800")
        dot.attr(rankdir="LR", size="8,5")

        # Estados con colores
        dot.node("INICIO", shape="circle", style="filled", fillcolor="lightblue")
        dot.node("BUILD_CODE", shape="circle", style="filled", fillcolor="lightgreen")
        dot.node("ESPERANDO_DINERO", shape="circle", style="filled", fillcolor="yellow")
        dot.node("PROCESSING", shape="circle", style="filled", fillcolor="orange")
        dot.node("FIN", shape="circle", style="filled", fillcolor="red")

        # Transiciones
        dot.edge("INICIO", "BUILD_CODE", label="LETRA / SHOW_CODE")
        dot.edge("BUILD_CODE", "ESPERANDO_DINERO", label="NUMERO / SHOW_PRICE")
        dot.edge("ESPERANDO_DINERO", "ESPERANDO_DINERO", label="INSERT_x / UPDATE_TOTAL")
        dot.edge("ESPERANDO_DINERO", "PROCESSING", label="CONFIRMAR / DELIVER")
        dot.edge("ESPERANDO_DINERO", "INICIO", label="CANCELAR / RETURN_CHANGE", style="dashed")
        dot.edge("PROCESSING", "FIN", label="entrega / DELIVER")
        dot.edge("FIN", "INICIO", label="reset / SHOW_CODE")

        output_path = os.path.abspath(nombre_archivo)
        rendered = dot.render(output_path, format="png", cleanup=True)
        return rendered
    except Exception as e:
        print("[salidas] generar_grafo_png error:", e)
        return None
    
# -----------------------------
# SHOW_CODE → ACTUALIZAR SOLO EL CÓDIGO A LA IZQUIERDA
# -----------------------------
# Esta función actualiza la interfaz cuando el usuario ingresa una letra del código
# Muestra el código parcial o completo en el display izquierdo
# Si ya hay un producto seleccionado, muestra su nombre y precio en el display derecho
# Si solo se ingresó la letra, muestra el mensaje "Esperando número…"
# Usa _call_ui para ejecutar la actualización de forma segura en la interfaz

def show_code(machine):
    code = machine.selected_code or machine.codigo_buffer or "--"

    def fn():
        main = _app.frames["PantallaMain"]

        # izquierda → código grande
        main.display_code_label.config(text=code)

        # derecha → nombre/estado del producto
        prod = machine.selected_product
        if prod:
            main.info_label.config(
                text=f"{prod['nombre']}\nPrecio: ${prod['precio']}"
            )
        else:
            main.info_label.config(text="Esperando número…")

    _call_ui(fn)


# -----------------------------
# SHOW_PRICE → mostrar nombre + precio + crédito
# -----------------------------
# Esta función actualiza la interfaz cuando el usuario completa el código del producto
# Muestra en el display izquierdo el código seleccionado
# En el display derecho muestra: Nombre del producto, Precio del producto, Crédito acumulado hasta el momento
# Usa 'payload' si se pasa información directa, o toma los datos del producto seleccionado
# Ejecuta la actualización de forma segura con _call_ui

def show_price(machine, payload=None):
    nombre = payload.get("nombre") if payload else (machine.selected_product.get("nombre") if machine.selected_product else "")
    precio = payload.get("precio") if payload else (machine.selected_product.get("precio") if machine.selected_product else 0)

    def fn():
        main = _app.frames["PantallaMain"]

        main.display_code_label.config(text=machine.selected_code or "--")

        main.info_label.config(
            text=f"Producto: {nombre}\n"
                 f"Precio: ${precio}\n"
                 f"Crédito actual: ${machine.credito}"
        )

    _call_ui(fn)


# -----------------------------
# UPDATE_TOTAL → actualizar crédito mostrado en la derecha
# -----------------------------
# Esta función se invoca cada vez que el usuario inserta una moneda
# Obtiene el producto seleccionado (si existe)
# Si hay producto:Muestra nombre y precio del producto, Muestra el crédito acumulado
# Si no hay producto: Solo muestra el crédito acumulado
# Usa _call_ui para ejecutar la actualización de forma segura en la interfaz

def update_total(machine, payload=None):
    def fn():
        main = _app.frames["PantallaMain"]

        prod = machine.selected_product
        if prod:
            main.info_label.config(
                text=f"Producto: {prod['nombre']}\n"
                     f"Precio: ${prod['precio']}\n"
                     f"Crédito actual: ${machine.credito}"
            )
        else:
            main.info_label.config(text=f"Crédito actual: ${machine.credito}")

    _call_ui(fn)


# -----------------------------
# SHOW_MESSAGE → mensaje temporal
# -----------------------------
# Esta función muestra mensajes temporales en la interfaz (ej. errores o avisos)
# Obtiene el texto desde 'payload' (cadena directa o diccionario con clave "msg")
# Actualiza el display derecho con el mensaje y resetea el código en el display izquierdo
# Después de 1.5 segundos, restablece los textos a su estado inicial: Izquierda: "--", Derecha: "Seleccione un producto…"
# Usa _call_ui para ejecutar la actualización de forma segura en la interfaz.

def show_message(machine, payload=None):
    msg = payload if isinstance(payload, str) else (payload.get("msg") if payload else "")

    def fn():
        main = _app.frames["PantallaMain"]

        main.info_label.config(text=msg)
        main.display_code_label.config(text="--")

        _app.root.after(
            1500,
            lambda: (
                main.display_code_label.config(text="--"),
                main.info_label.config(text="Seleccione un producto…")
            )
        )

    _call_ui(fn)


# -----------------------------
# DELIVER → animación + mensajes en display + mostrar grafo
# -----------------------------
# Esta función se ejecuta al confirmar una compra
# Muestra mensaje inicial con el producto y el cambio
# Dibuja la bandeja y anima la caída del producto en el canvas
# Al finalizar la animación: Muestra mensaje de "Compra exitosa", Refresca el stock de productos, Genera y muestra el grafo de estados en PantallaGrafo
# Reasigna el botón "Volver" para limpiar la interfaz, resetear la máquina y regresar a PantallaMain
# Usa _call_ui para ejecutar la actualización de forma segura en la interfaz

def deliver(machine, payload=None):
    nombre = payload.get("nombre") if payload else (machine.selected_product.get("nombre") if machine.selected_product else "")
    precio = payload.get("precio") if payload else (machine.selected_product.get("precio") if machine.selected_product else 0)
    cambio = payload.get("cambio") if payload else 0

    def fn():
        main = _app.frames["PantallaMain"]

        # Mostrar mensaje inicial
        main.display_code_label.config(text=machine.selected_code or "--")
        main.info_label.config(
            text=f"Entregando {nombre}...\nCambio: ${cambio}"
        )

        # Canvas para animación
        canvas = main.producto_canvas
        try:
            canvas.delete("all")
        except Exception:
            pass

        bandeja_y = 70
        # Dibujar bandeja (estática)
        canvas.create_rectangle(8, bandeja_y+30, 192, bandeja_y+42,
                                fill="#777", outline="#444")

        # Obtener imagen del producto desde cache en PantallaMain
        img = main.product_images.get(machine.selected_code)
        img_placeholder = img is None

        # Posición inicial y parámetros animación
        y = -40
        x = int(canvas.winfo_reqwidth() / 2) if canvas.winfo_reqwidth() else 110
        end_y = 40
        step = 6

        def anim():
            nonlocal y
            canvas.delete("all")
            # bandeja visible
            canvas.create_rectangle(8, bandeja_y+30, 192, bandeja_y+42,
                                    fill="#777", outline="#444")
            if img_placeholder:
                # rectángulo de respaldo
                canvas.create_rectangle(x-40, y, x+40, y+40,
                                        fill="#f39c12", outline="#c87f0a")
            else:
                # mostrar la imagen (PhotoImage)
                try:
                    canvas.create_image(x, y, image=img, anchor="n")
                except Exception as e:
                    # en caso de error con la imagen, dibujar placeholder
                    print("[deliver] error al dibujar imagen:", e)
                    canvas.create_rectangle(x-40, y, x+40, y+40,
                                            fill="#f39c12", outline="#c87f0a")

            y += step
            if y < end_y:
                _app.root.after(30, anim)
            else:
                # Fin animación
                main.info_label.config(
                    text=f"Compra exitosa!\nCambio: ${cambio}\nGenerando grafo..."
                )
                _app.root.after(5000, lambda: _app.mostrar_pantalla("PantallaGrafo"))

                # refrescar productos (usar el método del frame)
                try:
                    _app.frames["PantallaMain"].refresh_products()
                except Exception:
                    print("[deliver] no se pudo refrescar productos")

                # Intentar generar el grafo y mostrar el frame PantallaGrafo
                try:
                    ruta_grafo = generar_grafo_png("grafo_estados")
                    if ruta_grafo and os.path.exists(ruta_grafo):
                        # cargar imagen en PantallaGrafo y mostrarla
                        try:
                            _app.frames["PantallaGrafo"].cargar_imagen(ruta_grafo)

                            # buscar el botón "Volver" en los hijos de PantallaGrafo y reasignar su comando
                            pg = _app.frames["PantallaGrafo"]
                            for child in pg.winfo_children():
                                # comparamos texto si es Button
                                if isinstance(child, tk.Button) and child.cget("text").lower() == "volver":
                                    def on_volver(cb_pg=pg):
                                        # limpiar canvas de main, resetear máquina y volver a main
                                        try:
                                            _app.frames["PantallaMain"].producto_canvas.delete("all")
                                        except Exception:
                                            pass
                                        try:
                                            machine._reset()
                                        except Exception:
                                            pass
                                        _app.frames["PantallaMain"].display_code_label.config(text="--")
                                        _app.frames["PantallaMain"].info_label.config(text="Seleccione un producto…")
                                        try:
                                            _app.frames["PantallaMain"].refresh_products()
                                        except Exception:
                                            pass
                                        _app.mostrar_pantalla("PantallaMain")
                                    child.config(command=on_volver)
                                    break
                        except Exception as e:
                            print("[deliver] error mostrando PantallaGrafo:", e)
                            # fallback: resetear y limpiar
                            try:
                                machine._reset()
                            except Exception:
                                pass
                            canvas.delete("all")
                            main.display_code_label.config(text="--")
                            main.info_label.config(text="Seleccione un producto…")
                    else:
                        # no se pudo generar grafo: solo resetear
                        try:
                            machine._reset()
                        except Exception:
                            pass
                        canvas.delete("all")
                        main.display_code_label.config(text="--")
                        main.info_label.config(text="Seleccione un producto…")
                        try:
                            _app.frames["PantallaMain"].refresh_products()
                        except Exception:
                            pass
                except Exception as e:
                    print("[deliver] Error generando o mostrando grafo:", e)
                    try:
                        machine._reset()
                    except Exception:
                        pass
                    canvas.delete("all")
                    main.display_code_label.config(text="--")
                    main.info_label.config(text="Seleccione un producto…")

        anim()

    _call_ui(fn)


# -----------------------------
# RETURN_CHANGE → cancelar compra
# -----------------------------
# Esta función se ejecuta cuando el usuario presiona CANCELAR
# Calcula el monto de cambio a devolver (payload numérico o diccionario)
# Actualiza la interfaz: Display izquierdo: "--", Display derecho: mensaje de cancelación + monto devuelto
# Dibuja el monto devuelto en el canvas de la bandeja
# Después de 2 segundos: Resetea la máquina, Refresca la lista de productos, Restablece los textos iniciales, Limpia el canvas
# Usa _call_ui para ejecutar la actualización de forma segura
# El diccionario 'funciones_salidas' conecta las salidas de la máquina con las funciones de interfaz correspondientes (SHOW_CODE, SHOW_PRICE, UPDATE_TOTAL, DELIVER, RETURN_CHANGE, SHOW_MESSAGE, SHOW_CHANGE)

def return_change(machine, payload=None):
    amount = payload if isinstance(payload, (int, float)) else (payload.get("amount") if payload else 0)

    def fn():
        main = _app.frames["PantallaMain"]

        main.display_code_label.config(text="--")
        main.info_label.config(text=f"Operación cancelada\nCambio: ${amount}")

        canvas = main.producto_canvas
        try:
            canvas.delete("all")
            canvas.create_text(100, 40, text=f"${amount}",
                               font=("Arial", 18), fill="white")
        except Exception:
            pass

        _app.root.after(
            2000,
            lambda: (
                (machine._reset() if hasattr(machine, "_reset") else None),
                (getattr(_app.frames["PantallaMain"], "refresh_products", lambda: None)()),
                main.display_code_label.config(text="--"),
                main.info_label.config(text="Seleccione un producto…"),
                (canvas.delete("all") if canvas else None)
            )
        )

    _call_ui(fn)


# Diccionario que usa la máquina
funciones_salidas = {
    Output.SHOW_CODE: show_code,
    Output.SHOW_PRICE: show_price,
    Output.UPDATE_TOTAL: update_total,
    Output.DELIVER: deliver,
    Output.RETURN_CHANGE: return_change,
    Output.SHOW_MESSAGE: show_message,
    Output.SHOW_CHANGE: return_change,
}
