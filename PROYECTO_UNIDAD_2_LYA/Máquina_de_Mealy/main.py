# main.py
import tkinter as tk
from interfaz_usuario import VendingMachineApp
from maquina import MaquinaDispensadoraMealy 

def main():
    root = tk.Tk()

    # Tamaño de la ventana
    win_w = 1080
    win_h = 640

    # Obtener tamaño de la pantalla
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Calcular coordenadas para centrar
    pos_x = int((screen_w / 2) - (win_w / 2))
    pos_y = int((screen_h / 2) - (win_h / 2))

    # Configurar geometría centrada
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

    # Crear máquina 
    maquina = MaquinaDispensadoraMealy()
    app = VendingMachineApp(root, maquina)

    root.mainloop()


# Ejecutar la aplicación desde el main siempre
if __name__ == "__main__":
    main()
