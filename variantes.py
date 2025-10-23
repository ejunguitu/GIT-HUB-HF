
""" 
Constantes y configuraciones para el juego Hundir la Flota.
"""

""" 
Primero se ha definido el tamaño del tablero, los símbolos que se usarán para representar
el agua, los barcos, los impactos y los fallos. 
Se ha considerado adecuado incluir código ANSI para representar los impactos en rojo. 
Por ello, se han añadido las constantes ANSI_ROJO y ANSI_RESET.
"""

filas = 10
columnas = 10
letras_columnas = [chr(ord("A") + i) for i in range(columnas)]

agua = "_"
barco = "O"
tocado = "X"
Fallo = "."

ANSI_ROJO = "\033[91m"
ANSI_RESET = "\033[0m"

""" 
Tal y como se ha definido en el ennunciado, se ha configurado la flota.  
"""
flota = [2, 2, 2, 3, 3, 4]

""" 
Por último, se ha considerado oportuno que el jugador pueda salir y guardar la partida 
para poder realizar estrategias adecuadas. 
En este sentido, se ha definido la constante ARCHIVO_PARTIDA.
"""
ARCHIVO_PARTIDA = "partida_guardada.pkl"
