# Simulador de Dispensador Automático con Máquina de Mealy

## Descripción

Este proyecto es una **simulación interactiva de un dispensador automático de productos** desarrollada en **Python (versión 3.13)** con interfaz gráfica mediante **Tkinter** y visualización de estados con **Graphviz**.  

El sistema modela un **autómata finito tipo Mealy**, donde las **salidas dependen del estado actual y de la entrada recibida**.  
El dispensador permite seleccionar productos, insertar dinero, confirmar la compra, cancelar la operación (manual o automática tras 10 segundos) y manejar estados de error o mantenimiento.  

El programa cuenta con una **interfaz visual animada**, donde el usuario observa las transiciones de estados, el crédito acumulado, la animación de entrega en bandeja y el grafo de estados generado dinámicamente.


## Objetivos

* Implementar una **máquina de Mealy** para modelar un sistema real (dispensador automático).  
* Definir claramente **entradas, salidas y estados** del sistema.  
* Diseñar el **grafo de transiciones** y visualizarlo con Graphviz.  
* Simular el comportamiento completo en Python.  
* Desarrollar una **interfaz gráfica** que muestre las transiciones y salidas en tiempo real.  
* Documentar el proyecto con diagramas, tablas de transición y pruebas de funcionamiento.  


## Tecnologías utilizadas

* **Lenguaje:** Python 3.13  
* **Bibliotecas:**
  * `tkinter` (interfaz gráfica)  
  * `enum` (definición de estados, entradas y salidas)  
  * `dataclasses` (manejo de contexto del sistema)  
  * `threading` (temporizador de cancelación automática)  
  * `graphviz` (generación del grafo de estados en PNG)  
  * `PIL` (Pillow, para manejo de imágenes de productos)  
* **IDE recomendado:** Visual Studio Code  
* **Imágenes:**  
  * Carpeta `IMG/` con archivos `A1.webp` … `D4.webp` (productos)  


## Instalación y configuración

### 1. Instalar Python

* Descarga **Python 3.13** desde la página oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
* Durante la instalación, **marca la casilla** “Add Python to PATH”.  
* Verifica la instalación con:  

```bash
python --version
```

### 2. Instalar Graphviz

* Usa el instalador incluido en la carpeta `Instaladores/`.  
* Asegúrate de que el ejecutable `dot` esté accesible desde el sistema.  
* Verifica con:  

```bash
dot -V
```

### 3. Instalar la biblioteca Pillow

* Abre una terminal en tu computadora (PowerShell o CMD).
* Copia y ejecuta el siguiente comando (tu ruta de instalación puede variar):

   ```bash
   C:\Users\usuario1\AppData\Local\Programs\Python\Python313\python.exe -m pip install pillow
   ```
* Espera a que finalice la instalación.
   Si se instaló correctamente, verás un mensaje como:

   ```
   Successfully installed pillow-x.x.x
   ```

### 4. Estructura del proyecto
```
PROYECTO_UNIDAD_2_LYA/
│
├── Máquina_de_Mealy/
│   ├── IMG/                        ← Imágenes de productos (A1.webp, B3.jpg, etc.)
│   ├── definiciones.py             ← Enums y constantes
│   ├── maquina.py                  ← Lógica FSM Mealy
│   ├── salidas.py                  ← Funciones de salida (mostrar precio, entregar, etc.)
│   ├── interfaz_usuario.py         ← Interfaz gráfica con Tkinter
│   ├── pantalla_grafo.py           ← Visualización del grafo generado
│   ├── main.py                     ← Punto de entrada
|   |__pycache__/                    ← Archivos compilados (ignorar)
│
├── Graphviz/                       ← Instalación local de Graphviz
└── Instaladores/                   ← Instalador de Graphviz
 
```
### 5. Ejecutar el programa

Puedes ejecutar el programa de dos maneras:

#### Opción 1: Desde VS Code
* Abre la carpeta del proyecto en **Visual Studio Code**.  
* Abre el archivo `main.py`.  
* Haz clic en el botón **▷ “Correr”**.  

#### Opción 2: Desde PowerShell o CMD
* Abre una terminal en la carpeta del proyecto.  
* Escribe:  

```bash
python main.py
```

## Funcionamiento general

* **Estado INICIO:** El sistema espera la selección de producto.  
* **Selección:** Se muestra el precio y se espera la inserción de dinero.  
* **Pago:** Se acumula crédito y se muestra el faltante.  
* **Confirmar compra:** Si el crédito ≥ precio, se entrega el producto y se devuelve cambio.  
* **Cancelar:** Se devuelve el crédito acumulado (manual o automático tras 10 segundos).  
* **Error:** Se muestra mensaje de error (sin stock, insuficiente, selección inválida).  
* **Mantenimiento:** El sistema se bloquea hasta que se desactive el modo servicio.  


## Funcionalidades principales

* Simulación de un dispensador automático con máquina de Mealy.  
* Visualización gráfica de estados y transiciones.  
* Acumulación de crédito y cálculo de faltante.  
* Animación de entrega en bandeja con imagen del producto.  
* Cancelación manual y automática.  
* Generación dinámica del grafo de estados con Graphviz.  
* Validación automática de imágenes de productos en carpeta `IMG/`.  


## Interfaz gráfica

El programa utiliza **Tkinter** y se compone de tres áreas principales:

* **Display:** Muestra código, nombre, precio y crédito acumulado.  
* **Teclado virtual:** Botones A–D y 1–4 para seleccionar producto.  
* **Ranura de monedas:** Botones $1, $5, $10, $20.  
* **Bandeja de salida:** Animación de caída del producto.  
* **Pantalla de grafo:** Visualización del grafo generado en PNG.  
* **Botones de acción:** Confirmar, Cancelar, Ver Grafo.  


## Autores

Proyecto académico desarrollado por:  
* Rubi María Cobos Ramos    
* Ingridh Maricela Gracia Flores  
* Veyra María Gutiérrez Gómez  
* Jesús Emmanuel López Zuñiga  
* Jennifer Elizabeth Yépez López  
