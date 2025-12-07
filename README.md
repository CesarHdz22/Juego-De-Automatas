# Juego de Autómatas

Este proyecto es una aplicación que simula y evalúa autómatas finitos deterministas (DFA).  
El usuario puede ingresar cadenas, verificar si son aceptadas o rechazadas por el autómata y avanzar entre diferentes niveles configurados mediante reglas.

---

## Descripción

El sistema está dividido en tres partes principales:

- **automata/**  
  Contiene la implementación del DFA, incluyendo estados, transiciones, alfabeto, estado inicial y estados de aceptación.

- **engine/**  
  Incluye la lógica del juego, como validación de niveles y reglas.

- **ui/**  
  Implementación de la interfaz gráfica utilizando Tkinter.

El archivo **main.py** es el punto de entrada para ejecutar la aplicación.

---

## Requisitos

- Python 3.8 o superior  
- Tkinter (normalmente ya viene incluido con Python)

---

## Ejecución

Desde la carpeta principal del proyecto:


python automata_game/main.py

En Windows también puede funcionar:

py automata_game/main.py


## Funcionamiento General

1. El usuario ingresa una cadena en la interfaz.  
2. El sistema procesa la cadena utilizando el autómata cargado.  
3. Se evalúa si la cadena es aceptada o no.  
4. Dependiendo del nivel, pueden aplicarse reglas adicionales.  
5. El resultado se muestra en pantalla.

---

## Modificación y Extensión

- Nuevos autómatas pueden agregarse editando o añadiendo archivos dentro de `automata/`.
- Nuevas reglas o niveles pueden implementarse en `engine/level_rules.py`.
- La interfaz puede modificarse dentro de `ui/app_tk.py`.

---

## Licencia

Uso libre para fines educativos y de práctica.
