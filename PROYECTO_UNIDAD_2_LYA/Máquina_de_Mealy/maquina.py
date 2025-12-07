# maquina.py
from definiciones import Estado, Input, Output, PRODUCTOS
from salidas import funciones_salidas

class MaquinaDispensadoraMealy:
    def __init__(self):
        self.estado = Estado.INICIO
        self.codigo_buffer = ""       # primero letra, luego número
        self.selected_code = None     # snapshot del código seleccionado
        self.selected_product = None  # snapshot del producto seleccionado
        self.credito = 0              # crédito acumulado
        self.funciones = funciones_salidas 

    def procesar_entrada(self, entrada, valor=None):
        
        # ---------------------------
        # 1) ENTRADA LETRA (A–D)
        # ---------------------------
        if entrada == Input.LETRA:
            letra = str(valor).upper()
            if letra not in ['A','B','C','D']:
                self._emit(Output.SHOW_MESSAGE, f"Letra inválida: {valor}")
                return

            self.codigo_buffer = letra
            self.selected_code = None
            self.selected_product = None
            self.estado = Estado.BUILD_CODE
            self._emit(Output.SHOW_CODE) 
            return

        # ---------------------------
        # 2) ENTRADA NÚMERO (1–4)
        # ---------------------------
        if entrada == Input.NUMERO:
            if self.estado != Estado.BUILD_CODE or not self.codigo_buffer:
                self._emit(Output.SHOW_MESSAGE, "Seleccione primero una letra (A-D).")
                return

            numero = str(valor)
            if numero not in ['1','2','3','4']:
                self._emit(Output.SHOW_MESSAGE, f"Número inválido: {valor}")
                self._reset_buffer()
                return

            codigo = f"{self.codigo_buffer}{numero}"
            prod = PRODUCTOS.get(codigo)

            if not prod:
                self._emit(Output.SHOW_MESSAGE, f"Código {codigo} no existe.")
                self._reset()
                return

            if prod['stock'] <= 0:
                self._emit(Output.SHOW_MESSAGE, f"Sin stock: {codigo}")
                self._reset()
                return

            # Selección válida → guardar snapshot
            self.selected_code = codigo
            self.selected_product = {
                "nombre": prod["nombre"],
                "precio": prod["precio"],
                "stock": prod["stock"]
            }

            self.credito = 0
            self.estado = Estado.ESPERANDO_DINERO

            # Mandar nombre y precio del producto seleccionado
            self._emit(Output.SHOW_PRICE, {
                "nombre": self.selected_product["nombre"],
                "precio": self.selected_product["precio"]
            })

            return

        # ---------------------------
        # 3) ENTRADA DINERO ($1, $5, $10, $20)
        # ---------------------------
        if entrada in (Input.INSERT_1, Input.INSERT_5, Input.INSERT_10, Input.INSERT_20):
            if self.estado != Estado.ESPERANDO_DINERO:
                self._emit(Output.SHOW_MESSAGE, "Seleccione un producto primero.")
                return

            added = {
                Input.INSERT_1: 1,
                Input.INSERT_5: 5,
                Input.INSERT_10: 10,
                Input.INSERT_20: 20
            }[entrada]

            # Acumular crédito
            self.credito += added

            # Emitir actualización de crédito
            self._emit(Output.UPDATE_TOTAL, self.credito)

            # No despachamos aquí, solo mostramos el total
            return

        # ---------------------------
        # 4) BOTÓN CONFIRMAR COMPRA
        # ---------------------------
        if entrada == Input.CONFIRMAR:
            if self.estado != Estado.ESPERANDO_DINERO:
                self._emit(Output.SHOW_MESSAGE, "No hay transacción en curso.")
                return

            if self.credito < self.selected_product['precio']:
                falta = self.selected_product['precio'] - self.credito
                self._emit(Output.SHOW_MESSAGE, f"Faltan ${falta}")
                return

            # Ahora sí despachamos
            change = self.credito - self.selected_product['precio']
            self._deliver_and_finish(change)
            return

        # ---------------------------
        # 5) BOTÓN CANCELAR
        # ---------------------------
        if entrada == Input.CANCELAR:
            if self.credito > 0:
                amt = self.credito
                self._emit(Output.RETURN_CHANGE, amt)
                self._reset()
            else:
                self._emit(Output.SHOW_MESSAGE, "Operación cancelada.")
                self._reset()
            return


    # =========================================================
    #   ENTREGAR PRODUCTO 
    # =========================================================
    def _deliver_and_finish(self, change):
    # Descontar stock
        if self.selected_code:
            PRODUCTOS[self.selected_code]['stock'] -= 1

    # Emitir salida DELIVER
        self._emit(Output.DELIVER, {
        "nombre": self.selected_product['nombre'],
        "precio": self.selected_product['precio'],
        "cambio": change
    })
        


    # =========================================================
    # RESETEAR BUFFER Y ESTADO
    # =========================================================
    def _reset_buffer(self):
        self.codigo_buffer = ""
        self.selected_code = None
        self.selected_product = None
        self.estado = Estado.INICIO

    def _reset(self):
        self.codigo_buffer = ""
        self.selected_code = None
        self.selected_product = None
        self.credito = 0
        self.estado = Estado.INICIO


    # =========================================================
    # SALIDAS
    # =========================================================
    def _emit(self, salida, payload=None):
        fn = self.funciones.get(salida)

        if not fn:
            print("[maquina] salida sin handler:", salida)
            return

        try:
            if payload is None:
                fn(self)
            else:
                fn(self, payload)
        except TypeError:
            fn(self)
