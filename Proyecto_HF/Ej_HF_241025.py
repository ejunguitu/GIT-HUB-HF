#!/usr/bin/env python
# coding: utf-8

# In[48]:


""" 
De acuerdo con la configuración del juego, vamos a necesitar 4 tableros para 2 jugadores: 
- Jugador 1 : dos tableros (tablero de ataque + tablero de barcos/impactos).
- Jugador 2 : dos tableros (tablero de ataque + tablero de barcos/impactos). 

La estrategia de defenda del Jugador 1 será definida por él/ella. 
Sin embargo, la estrategia del Jugador 2 será definida de forma aleatoria (máquina). 

"""

# Definir elementos comunes

## Hay que configurar varios tableros. Filas y columnas son variables comunes
## El tamaño de todos los tableros deber ser uniforme. 
## Es decir, todos los tableros deben tener el mismo tamaño (área; x*y). 

x_filas = (5)
y_columnas = (5)

## El valor de las posiciones es común a todos los tableros. 

agua = "~" 
tocado = "X"
impacto_fallido = "."
barco = "O"

## El tamaño de la flota es común a ambos jugadores. 

## Como primer paso voy a crear un tablero con posiciones de agua.

# Parámetros del tablero
agua = "~"       # símbolo que representa agua
x_filas = 5      # número de filas
y_columnas = 5   # número de columnas

def crear_tablero():
    tablero = []  # matriz vacía
    for _ in range(x_filas):        # Recorremos las filas
        fila = []                   # fila vacía
        for _ in range(y_columnas): # Recorremos las columnas
            fila.append(agua)       # añadimos agua a la casilla
        tablero.append(fila)        # añadimos la fila completa al tablero
    return tablero

# Crear el tablero de ejemplo
tablero_ejemplo = crear_tablero()
for fila in tablero_ejemplo:
    print(fila)

