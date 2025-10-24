
# Bienvenido al juego El Hombre contra la máquina

![Diagrama](./img/hundir-la-flota-juego-de-mesa.jpg)

Vamos a jugar a un juego llamado "El Hombre contra la máquina" basado en el mítico juego "Hundir la flota".
Las bases de funcionamiento son similares a 'Hundir la Flota' que es un juego de estrategia para dos jugadores,
donde se simula una batalla naval. Los jugadores colocan secretamente su flota de barcos en un tablero de cuadrícula y,
por turnos, "disparan" a la cuadrícula del oponente mediante coordenadas, intentando adivinar la posición de sus barcos.
El objetivo es ser el primero en hundir por completo la flota enemiga.

En este proyecto se ha intentado simular este juego.
Del mismo modo, en "El Hombre contra la máquina" hay dos jugadores

- Jugador 1: el jugador 1 será el usuario y le permitiremos elegir un "Alias de jugador".
- Jugador 2: el jugador dos será por defecto identificado como "El enemigo", y estará representado por una máquina.

Cada jugador podrá visualizar dos tableros:

- Un tablero para posicionar la estrategia de defensa y disparo.
- Y otro tablero para representar el resultado del ataque.

Los tableros tendrán un tamaño de 10 líneas por 10 columnas (10x10). El índice de las líneas del tablero será numérico (empezando por 1), y el índice de las columnas del tablero será alfabético y en mayúsculas (empezando por A).

Cada jugador dispondrá de 6 barcos en total:

- 3 barcos x 2 esloras | 2 barcos x 3 esloras | 1 barco x 4 esloras.

Vayamos con las características principales de los tableros del primer jugador (usuario).

________________

Inicio:

Al iniciar el juego, se le pedirá al jugador 1 (usuario) que se identifique con un alias.
Como segundo paso, deberá elegir su estrategia de defensa y ataque eligiendo las coordinadas de sus barcos en el tablero
Se le solicitará el detalle de:

- la posición de línea
- la posición de la columna
- la dirección del barco en el tablero (horizontal / vertical).

La posición de los barcos se representará en el tablero de defensa con una "O".

*alrededor de los barcos se ha parametrizado una distancia de cobertura de una posición a lo largo de toda su área. Salvo que uno de los lados coincida con el borde del tablero, se considerará la distancia de cobertura. Si por error el primer jugador superpone un barco, o quiere posicionar un barco en la distancia de cobertura, se mostrará en pantalla el mensaje de error "Error de posición. Vuelve a intentarlo". Igualmente, se considerará la selección de la posición de las líneas y columnas acotada a la matriz 10X10.

Notas:

- los barcos serán representados con "O"
- la distancia de seguridad estará representada con un punto.
- el impacto acertado será representado por una "X"
- el error del ataque será representado con un punto.

Vayamos ahora con el segundo jugador (la máquina).
Para ello, consideraremos la misma dinámica de juego pero para la selección de la posición de los barcos, pero en esta ocasión utilizaremos un método aleatorio.

Una vez creados los tableros, el siguiente paso será establecer el turno de inicio del juego. Le daremos la ventaja de elegir la opción de cara ("C") o cruz ("X") al primer jugador.
De forma aleatoria obtendremos el resultado para establecer el inicio del juego.

Es a partir de este momento cuando comenzará el ataque.
¡Buena suerte jugadores!

________________;

Funcionalidades principales:

⦁ Vamos a partir de la premisa de que todas las acciones de la máquina serán ejecutadas de forma aleatoria.
⦁ Para iniciar el ataque hay que identificar una posición de línea y una posición de columna.
⦁ Si la posición de ataque elegida obtiene como resultado un impacto, se representará el impacto con una "X" en el tablero de ataque.
⦁ Si el enemigo consigue impactar contra cualquier posición de nuestro barco, se representará con una "X" en color rojo en el tablero de defensa.
⦁ El acierto en el ataque da derecho a seguir manteniendo el turno.
⦁ Conoceremos el tamaño del barco cuando todas sus posiciones hayan sido alcanzadas. Se mostrará un texto en pantalla de barco hundido.
⦁ Si el resultado de la posición indicada es un error, entonces se pasará el turno y se indicará en un texto: "¡Mala suerte!. Has perdido tu turno".
⦁ El juego finalizará cuando alguno de los dos jugadores haya hundido todos los barcos de su contrincante.

## Detalle variantes

Se incluye un archivo python con el detalle de las variantes: variantes.py
Como observaciones principales de este archivo se destaca:

- tamaño del tablero
- posiciones de barco, impacto, error
- uso de secuencias ANSI para identificar el color rojo del impacto en el
tablero de defensa del jugador 1
- configuración de la flota (3x2) + (2x3) + (1x4)
- el uso de pickle para guardar archivos para poder reanudar la partida desde un punto fijo.

## Detalle funciones

Como paso inicial, se detallan las bibliotecas estándares y personalizadas que se utilizan en el juego:

- Random; para crear los barcos y los impactos de la máquina.
- Pickle y os; para guardar e identificar el archvio que contiene la jugada para reanudar la partida.
- Variantes; personalizada a los detalles considerados en el punto anterior.

Se crean funciones auxiliares para:

- la creación y visualización de tableros
- la colocación de los barcos (inputs jugador y aleatoria random)
- la gestión de turnos
- la funcionalidad guardar

Adicionalmente, se crean las funciones para:

- crear un tablero de juego a partir de un tablero vacío.
Se creará un tablero para los barcos del jugador (P), y
otro para los barcos de la máquina (E).El jugador deberá introducir:
posición fila+columna+dirección (H/V).
- se imprimen los tableros para el jugador (defensa/sus barcos - y ataque).
Además se parametrizan las funciones para convertir la letra de la columna
del tablero en índice numérico.
- se crean las funciones para identificar las posiciones que rodean a un barco "posiciones vecinas":(arriba, abajo y diagonal). El objetivo es
colocar los barcos y evitar colisiones.
- se crean las funciones relacionadas con turnos y ataques.
Según las posiciones de los impactos se conocerá si todos los barcos
han sido hundidos.

## Main Juego

En este apartado se parametrizan las funciones para el juego:

- alias de jugador
- tablero defensa jugador(inputs)
- posición de barcos jugador(colocación)
- tablero ataque jugador.
- posición de barcos máquina (random)
- tablero de ataque de la máquina
- tablero de defensa de la máquina
- turnos (elegir turno; random.choice)
- contador de turnnos
- abandonar partida (SALIR)
- todos los barcos hudidos máquina: victoria jugador.
- todos los barcos hundidos jugador: game over.
- ejecución juego principal

## Esquema funcional del juego

VARIABLES GLOBALES

- filas, columnas, letras_columnas
- símbolos: agua "_", barco "O", tocado "X", fallo "."
- colores ANSI (rojo, reset)
- flota = [2, 2, 2, 3, 3, 4]
- archivo_guardado (ej: "partida.pkl")

FUNCIONES AUXILIARES

- crear_tablero()
- valor_mostrar_celda(celda)
- imprimir_tableros_lado(defensa, ataque, alias)
- letra_a_indice(letra)
- celda_valida(f, c)
- vecinas(f, c) / celdas_alrededor(f, c)

CREACIÓN Y GESTIÓN DE BARCOS

- crear_barco(id, tamaño, posiciones)
- posiciones_colisionan(posiciones, otros_barcos)
- se_puede_colocar(posiciones, barcos_existentes)
- colocar_barco_en_tablero(tablero, barco)
- colocar_cobertura_en_tablero(tablero, barco)

COLOCACIÓN DE BARCOS (JUGADOR / MÁQUINA)

- colocar_barcos_manual(jugador): pide fila, columna, orientación H/V o SALIR
- colocar_barcos_aleatorio_maquina(): genera coordenadas válidas aleatorias

ATAQUES

- recibir_ataque(f, c, barcos, tablero_defensa): devuelve: 'impacto', 'fallo'
- todos_barcos_hundidos(barcos)

TURNOS DE JUEGO

- turno_jugador(tab_atq, barcos_enem, tab_def_enem)
- turno_maquina(tab_atq_M, barcos_J, tab_def_J)
*gestionan input, impacto/fallo

GUARDAR Y CARGAR PARTIDA

- guardar_partida(estado):pickle.dump
- cargar_partida():pickle.load

FLUJO JUEGO PRINCIPAL

1. ¿Existe partida guardada?: cargar o nueva
2. Pedir alias al jugador
3. Colocar barcos jugador
4. Colocar barcos máquina
5. Moneda al aire: gestión del turno
6. Bucle de turnos: -turno_jugador() o turno_maquina()
7. Mostrar tableros finales y borrar guardado

¿usuario escribe SALIR?: guardar y salir
¿barcos hundidos?: fin de partida.
