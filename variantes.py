
""" 
Debajo se representan las variables constantes y las configuraciones para 
el juego 'El Hombre contra la máquima'.
"""

""" 
Primero se ha definido el tamaño del tablero, los símbolos que se usarán para representar
el agua, los barcos, los impactos y los fallos. 
Se ha considerado adecuado incluir código ANSI para representar los impactos en rojo."""

filas = 10
columnas = 10
letras_columnas = [chr(ord("A") + i) for i in range(columnas)]

agua = "_"
barco = "O"
tocado = "X"
Fallo = "."

""" 
Como se ha indicado con anterioridad, se ha utilizado la secuencia ANSI para 
identificar los impactos en rojo en la consola.
ANSI_ROJO = "\033[91m": 
\033 es el carácter de escape en Python para iniciar una secuencia ANSI.
[91m indica color rojo brillante para el texto.
"""

ANSI_ROJO = "\033[91m"
ANSI_RESET = "\033[0m"

""" 
Tal y como se ha definido en el ennunciado, se ha configurado la flota.  
"""
flota = [2, 2, 2, 3, 3, 4]

""" 
Por último, se ha considerado oportuno que el jugador pueda salir y guardar la partida 
para poder reanudar el juego en otro momento. 
En este sentido, se ha definido una variable que guarda 
el nombre de un archivo: 'partida_guardada.pkl'.
La extensión .pkl indica que es un archivo “pickle” de Python, es decir, 
un archivo que guarda objetos de Python (listas, diccionarios, etc.) 
de forma que puedan cargarse después con pickle.load().
"""
ARCHIVO_PARTIDA = "partida_guardada.pkl"
