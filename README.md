
Bienvenido a uno de los juegos de estrategia más conocidos. 

![Diagrama](./img/hundir-la-flota-juego-de-mesa.jpg)


Se trata de un juego de estrategia de "El Hombre contra la máquina".
En este juego hay dos jugadores.

Paso 1: 
Al jugador uno le dejaremos elegir un "Alias de jugador". 
El jugador dos será por defecto identificado como "El enemigo", y estará representado por una máquina.

Paso 2: 
En este paso se crearán los tableros para jugar. 
Su tamaño será de 10 líneas por 10 columnas (10x10). 
El índice de las líneas será numérico (empezando por 1) y el índice de las columnas será alfabético y en mayúsculas (empezando por A). 

Cada jugador tendrá dos tableros. 
Un tablero para posicionar la estrategia de defensa y disparo. 
Y otro tablero para representar el resultado del ataque. 
Del mismo modo, cada jugador dispondrá de 6 barcos en total: 3 barcos x 2 esloras | 2 barcos x 3 esloras | 1 barco x 4 esloras. 

Vayamos con las características principales de los tableros del primer jugador. 
En el primer tablero se representarán los barcos en su posición de defensa y preparados para disparar. 
Se representarán 6 barcos en total: 3 barcos x 2 esloras | 2 barcos x 3 esloras | 1 barco x 4 esloras. 
La posición de los barcos será elegida por el primer jugador creando una lista conteniendo el detalle de los barcos (posición línea / columna / Nº esloras). 
La posición de los barcos se representará en el tablero con una X. 
Alrededor de los barcos de este primer jugador tiene que haber una distancia de cobertura de una posición a lo largo de toda su área. Salvo que uno de los lados coincida con el borde del tablero, se considerará la distancia de cobertura. Si por error el primer jugador superpone un barco, o quiere posicionar un barco en la distancia de cobertura, se mostrará en pantalla el mensaje de error "Error de posición. Vuelve a intentarlo". Igualmente, se considerará la selección de la posición de las líneas y columnas acotada a la matriz 10X10.
En el segundo tablero, se representará un tablero vacío para identificar la estrategia de alcance y error del ataque según se vaya desarrollando el juego. 

Quiero tener los barcos del primer jugador y de el enemigo representados en dos listas (variables): 
lista 1 = donde se representará la estrategia de posición de los barcos del primer jugador.
lista 2 = donde se representará el resultado del ataque estratégico realizado contra "El enemigo". 
Cada lista estará formada por el número y tamaño de barcos indicados: 3x2 | 2x3 | 1x4

Vayamos ahora con el segundo jugador (la máquina). 
Para ello, consideraremos la misma dinámica de juego pero para la selección de la posición de los barcos, utilizaremos un método aleatorio. 

Notas: 
- los barcos serán representados con "O"
- la distancia de seguridad estará representada con un punto.
- el impacto acertado será representado por una "X"
- el error del ataque será representado con un punto. 

Paso 3: 
Comienza el juego. 
Para ello, hay que establecer el turno de inicio del juego. 
Le daremos la ventaja de elegir la opción de "cara" o "cruz" al primer jugador. 
De forma aleatoria obtendremos el resultado para establecer el inicio del juego.

Normas: 
Vamos a partir de la premisa que todas las acciones de la máquina serán ejecutadas de forma aleatoria. 
Para iniciar el ataque hay que identificar una posición de línea y una posición de columna. 
Si la posición de ataque elegida obtiene como resultado un impacto, se eliminará la posición de la lista de barco y se representará el impacto con una "X" en el tablero correspondiente. 
El acierto en el ataque da derecho a seguir manteniendo el turno.
Si el segundo ataque da como resultado otro impacto, podremos conocer la dirección del barco pero no su tamaño por lo que todavía es prematuro conocer las posiciones de la distancia de seguridad. 
Sólo conoceremos el tamaño del barco cuando sus posiciones extremas den como resultado un error (ambas). Únicamente cuando los dos extremos representen una posición de error, podremos identificar las posiciones de la distancia de seguridad. 
Si el resultado de la posición indicada es un error, entonces se pasará el turno y se indicará en un texto: "¡Mala suerte!. Has perdido tu turno". 

Cuando un barco tenga todas las posiciones de la distancia de seguridad marcadas con un punto, entonces habremos obtenido un blanco perfecto. Se mostrará un texto en pantalla de barco hundido. 
El juego finalizará cuando alguno de los dos jugadores haya hundido todos los barcos de su contrincante. 
