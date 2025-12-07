# definiciones.py
from enum import Enum, auto

class Estado(Enum):
    INICIO = auto()
    BUILD_CODE = auto()
    ESPERANDO_DINERO = auto()
    PROCESSING = auto()
    FIN = auto()

class Input(Enum):
    LETRA = auto()     # valor: 'A'..'D'
    NUMERO = auto()    # valor: '1'..'4'
    INSERT_1 = auto()  # valor: cantidad insertada
    INSERT_5 = auto()  # valor: cantidad insertada
    INSERT_10 = auto() # valor: cantidad insertada
    INSERT_20 = auto() # valor: cantidad insertada
    CONFIRMAR = auto() # confirmar compra
    CANCELAR = auto()  # cancelar compra

class Output(Enum):
    SHOW_CODE = auto()      # muestra el código en pantalla1
    SHOW_PRICE = auto()     # manda nombre+precio a pantalla2
    UPDATE_TOTAL = auto()   # actualiza total en pantalla2
    DELIVER = auto()        # procesa entrega -> pantalla3 y luego pantalla4
    RETURN_CHANGE = auto()  # mostrar cambio en pantalla4
    SHOW_MESSAGE = auto()   # mensajes en pantalla3
    SHOW_CHANGE = auto()    # alias para RETURN_CHANGE

# Productos A1..D4 (nombres, precios y stock inicial)
PRODUCTOS = {
    "A1": {"nombre": "Agua Ciel", "precio": 12, "stock": 10},
    "A2": {"nombre": "Coca Cola", "precio": 18, "stock": 8},
    "A3": {"nombre": "Pepsi", "precio": 17, "stock": 7},
    "A4": {"nombre": "Sprite", "precio": 18, "stock": 6},
    "B1": {"nombre": "Sabritas", "precio": 19, "stock": 10},
    "B2": {"nombre": "Doritos", "precio": 20, "stock": 8},
    "B3": {"nombre": "Ruffles", "precio": 21, "stock": 5},
    "B4": {"nombre": "Takis", "precio": 22, "stock": 6},
    "C1": {"nombre": "Galletas Emperador", "precio": 14, "stock": 12},
    "C2": {"nombre": "Galletas Oreo", "precio": 16, "stock": 9},
    "C3": {"nombre": "Barrita Marinela", "precio": 13, "stock": 11},
    "C4": {"nombre": "Chokis", "precio": 15, "stock": 10},
    "D1": {"nombre": "Chocolate Hershey's", "precio": 17, "stock": 7},
    "D2": {"nombre": "Chocolate Carlos V", "precio": 15, "stock": 8},
    "D3": {"nombre": "Bubulubu", "precio": 10, "stock": 10},
    "D4": {"nombre": "Panditas", "precio": 12, "stock": 9},
}
