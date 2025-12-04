# Simulador de Dispensador Automático con Máquina de Mealy

## Descripción

Este proyecto es una **simulación interactiva de un dispensador automático de comida** desarrollado en **Python (versión 3.13)** con interfaz gráfica mediante **Tkinter**.  

El sistema modela el comportamiento de un **autómata finito tipo Mealy**, donde las **salidas dependen del estado actual y de la entrada recibida**.  
El dispensador permite seleccionar productos, insertar dinero, confirmar la compra, cancelar la operación (manual o automática tras 10 segundos) y manejar estados de error o mantenimiento.  

El programa cuenta con una **interfaz visual**, donde el usuario observa las transiciones de estados y las salidas generadas (mostrar precio, acumular crédito, entregar producto, devolver cambio, mostrar errores).

---

## Objetivos

* Implementar una **máquina de Mealy** para modelar un sistema real (dispensador automático).  
* Analizar y definir **entradas y salidas** del sistema.  
* Diseñar el **autómata finito** con sus estados y transiciones.  
* Simular el comportamiento del sistema en Python.  
* Desarrollar una **interfaz gráfica** que muestre las transiciones de estados y las salidas en tiempo real.  
* Documentar el proyecto con diagramas, tablas de transición y pruebas de funcionamiento.  

---

## Tecnologías utilizadas

* **Lenguaje:** Python 3.13  
* **Bibliotecas:**  
  * `tkinter` (interfaz gráfica)  
  * `enum` (definición de estados, entradas y salidas)  
  * `dataclasses` (manejo de contexto del sistema)  
  * `threading` o `asyncio` (temporizador de cancelación automática)  
* **IDE recomendado:** Visual Studio Code  

---

## Instalación y configuración

### 1. Instalar Python

* Descarga **Python 3.13** desde la página oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
* Durante la instalación, marca la casilla **“Add Python to PATH”**.  
* Verifica la instalación con:  

```bash
python --version
```

---













### 2. Archivos requeridos

El proyecto se organiza en varios archivos:

* `definiciones.py` → Estados, Entradas y Salidas.  
* `maquina.py` → Lógica de transiciones de la máquina de Mealy.  
* `salidas.py` → Funciones que muestran las salidas (precio, crédito, errores, etc.).  
* `interfaz_usuario.py` → Interfaz gráfica con Tkinter.  
* `simulacion.py` → Escenarios de prueba.  
* `main.py` → Integración y ejecución del sistema.  

---

### 3. Ejecutar el programa

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

---

## Funcionamiento general

* **Estado Idle (Espera):** El sistema espera la selección de producto.  
* **Selección:** Se muestra el precio y se espera la inserción de dinero.  
* **Pago:** Se acumula crédito y se muestra el faltante.  
* **Confirmar compra:** Si el crédito ≥ precio, se entrega el producto y se devuelve cambio.  
* **Cancelar:** Se devuelve el crédito acumulado (manual o automático tras 10 segundos).  
* **Error:** Se muestra mensaje de error (sin stock, insuficiente, selección inválida).  
* **Mantenimiento:** El sistema se bloquea hasta que se desactive el modo servicio.  

---

## Funcionalidades principales

* Simulación de un dispensador automático con máquina de Mealy.  
* Visualización gráfica de estados y transiciones.  
* Acumulación de crédito y cálculo de faltante.  
* Entrega de producto y devolución de cambio.  
* Cancelación manual y automática.  
* Manejo de errores y modo mantenimiento.  

---

## Interfaz gráfica


---

## Autores

Proyecto académico desarrollado por:  
* Rubi María Cobos Ramos
* Kenia Elizondo Maravilla
* Ingridh Maricela Gracia Flores  
* Veyra María Gutiérrez Gómez  
* Jesús Emmanuel López Zuñiga  
* Jennifer Elizabeth Yépez López  

