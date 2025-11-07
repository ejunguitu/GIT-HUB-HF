
""" 
A continuación se detallan las bibliotecas de funciones para el juego (ver dabajo).
Se usan dos bibliotecas estándar de Python: random y pickle.
Una biblioteca personalizada llamada variantes.py contiene constantes y configuraciones del juego.
Y se importa el módulo os para interactuar con el sistema operativo. Se usa para comprobar 
si existe un archivo de partida guardada y para eliminarlo al final:
"""
import random
import pickle
import os
from variantes import filas, columnas, agua, Fallo, tocado, barco, letras_columnas, flota, ARCHIVO_PARTIDA, ANSI_ROJO, ANSI_RESET


""" 
Se han implementado las funciones necesarias para gestionar el juego El Hombre contra la máquina.
Estas funciones incluyen la creación y visualización de tableros, la colocación de barcos
tanto manual como automática, la gestión de los turnos de ataque, y la funcionalidad de
guardar y cargar partidas.
"""

"""
Funciones auxiliares para la gestión del juego El Hombre contra la máquina.
Estas funciones incluyen la creación y visualización de tableros,
la conversión de letras a índices, y la validación de celdas.
"""

"""
Crea un tablero vacío con agua.
"""
def crear_tablero():
    return [[agua for _ in range(columnas)] for _ in range(filas)]
            
""" 
Devuelve el símbolo a mostrar para una celda. 
Se mostrará el símbolo X en rojo si es tocado.
Se utiliza el método f-string para incluir los códigos ANSI.
Se utiliza el método isinstance y str.startswithpara para verificar si la celda 
contiene un identificador de barco.
La "P" indica un barco del jugador y la "E" un barco de la máquina.
"""
def valor_mostrar_celda(celda):
    if celda == tocado:        
        return f"{ANSI_ROJO}{tocado}{ANSI_RESET}"
    if celda == Fallo:
        return Fallo
    if celda == agua:
        return agua
    if isinstance(celda, str) and (celda.startswith("P") or celda.startswith("E")):
        return barco
    return str(celda)

"""
Imprime los tableros del jugador lado a lado.
Se han considerado dos tableros: 
-el de defensa (con barcos) y 
-el de ataque (sin barcos).
Además se ha añadido una cabecera para identificar cada tablero.
"""
def imprimir_tableros_lado(tablero_defensa, tablero_ataque, alias_jugador, mostrar_barcos=False):
    print(f"--- {alias_jugador}: Tablero de defensa vs Tablero de ataque ---")
    cabecera = "   " + " ".join(letras_columnas)
    espacio_entre_tableros = "   "
    print(f"{cabecera}{espacio_entre_tableros}{cabecera}")
    for i in range(filas):
        fila_def = " ".join(
            valor_mostrar_celda(c if mostrar_barcos else (c if c in (tocado, Fallo, agua) else agua))
            for c in tablero_defensa[i])
        fila_atq = " ".join(
            tocado if c == tocado else Fallo if c == Fallo else agua
            for c in tablero_ataque[i])
        print(f"{i+1:2} {fila_def}{espacio_entre_tableros}{i+1:2} {fila_atq}")
    print()

"""
Convierte letra de columna en índice numérico. 
Esto facilita la manipulación interna del tablero.
"""
def letra_a_indice(letra):
    letra = letra.upper()
    return letras_columnas.index(letra) if letra in letras_columnas else None

"""
Verifica si la celda está dentro del tablero. De esta forma se evita un error de índice.
"""
def celda_valida(fila, columna):
    return 0 <= fila < filas and 0 <= columna < columnas

"""" 
Se ha considerado oportuno incluir funciones que devuelvan las posiciones vecinas. 
Se entienden por posiciones vecinas aquellas que rodean una celda dada, incluyendo las diagonales.
Esto es útil para validar la colocación de barcos y para marcar 
las celdas alrededor de un barco hundido.
"""
def vecinas(fila, columna):
    posiciones_vecinas = []
    for df in (-1,0,1):
        for dc in (-1,0,1):
            if df==0 and dc==0:
                continue
            nf, nc = fila+df, columna+dc
            if celda_valida(nf,nc):
                posiciones_vecinas.append((nf,nc))
    return posiciones_vecinas

"""
Devuelve todas las celdas alrededor de una lista de posiciones. 
De esta forma, evitar colisiones y adyacencias entre barcos.
"""
def celdas_alrededor(posiciones):
    alrededor = set()
    for f,c in posiciones:
        for nf,nc in vecinas(f,c):
            if (nf,nc) not in posiciones:
                alrededor.add((nf,nc))
    return alrededor
# --------------------

""" 
Se han generado funciones relacionadas con la colocación de barcos, tanto manual como automática,
y la gestión de ataques y turnos.
Para la colocación de barcos, se han creado funciones para validar posiciones, 
crear barcos, y colocar barcos en el tablero.
Se ha creado un diccionario que representa un barco.
"""
def crear_barco(id_, tamaño, posiciones):
    return {"id": id_, "tamaño": tamaño, "posiciones": posiciones.copy(), "impactos": set()}

"""
Comprueba si las posiciones colisionan con otros barcos.
"""
def posiciones_colisionan(posiciones, otros_barcos):
    return any(p in b["posiciones"] for b in otros_barcos for p in posiciones)

"""
Valida si un barco puede colocarse en el tablero.
"""
def se_puede_colocar(posiciones, barcos_existentes):
    for f,c in posiciones:
        if not celda_valida(f,c):
            return False
    for b in barcos_existentes:
        if posiciones_colisionan(posiciones,[b]):
            return False
    cobertura_existente=set()
    for b in barcos_existentes:
        cobertura_existente.update(celdas_alrededor(b["posiciones"]))
    for p in posiciones:
        if p in cobertura_existente:
            return False
    filas_set={p[0] for p in posiciones}
    columnas_set={p[1] for p in posiciones}
    if not (len(filas_set)==1 or len(columnas_set)==1):
        return False
    if len(filas_set)==1:
        cols_sorted=sorted([p[1] for p in posiciones])
        if cols_sorted!=list(range(cols_sorted[0],cols_sorted[0]+len(cols_sorted))):
            return False
    else:
        filas_sorted=sorted([p[0] for p in posiciones])
        if filas_sorted!=list(range(filas_sorted[0],filas_sorted[0]+len(filas_sorted))):
            return False
    return True

"""
Coloca un barco en el tablero."""
def colocar_barco_en_tablero(tablero, barco):
    for f,c in barco["posiciones"]:
        tablero[f][c]=barco["id"]
"""
marca las celdas alrededor del barco hundido como fallos.
"""

def colocar_cobertura_en_tablero(tablero, barco):
    cov=celdas_alrededor(barco["posiciones"])
    for f,c in cov:
        if tablero[f][c]==agua:
            tablero[f][c]=Fallo

#-------------------------------

""" 
Se ha implementado la colocación manual de barcos para el jugador.
"""

"""
Permite al jugador colocar manualmente sus barcos.
Partimos de un tablero vacío y vamos pidiendo al jugador las posiciones.
Se valida cada posición y se actualiza el tablero tras cada colocación.
Se muestra el tablero actualizado después de cada colocación.

"""
def colocar_barcos_manual(jugador):
    barcos=[]
    tablero=crear_tablero()
    id_barco=1
    print(f"{jugador}, coloca tus barcos (filas 1-{filas}, columnas A-{letras_columnas[-1]})")
    for tamaño in flota:
        colocado=False
        while not colocado:
            try:
                print(f"Coloca un barco de tamaño {tamaño}. Ej: 4 B H")
                entrada=input("Fila Columna Direccion (H/V) o 'SALIR' para guardar y salir: ").strip().upper()
                if entrada in ("SALIR","Q"):
                    return "salir", tablero, barcos
                partes=entrada.replace(","," ").split()
                if len(partes)!=3:
                    print("Formato inválido")
                    continue
                fila_str,col_str,dir_str=partes
                if not fila_str.isdigit():
                    print("Fila inválida")
                    continue
                f0=int(fila_str)-1
                c0=letra_a_indice(col_str)
                if c0 is None:
                    print("Columna inválida")
                    continue
                dir_str=dir_str[0]
                posiciones=[]
                if dir_str=="H":
                    posiciones=[(f0,c0+i) for i in range(tamaño)]
                elif dir_str=="V":
                    posiciones=[(f0+i,c0) for i in range(tamaño)]
                else:
                    print("Dirección inválida")
                    continue
                if not se_puede_colocar(posiciones,barcos):
                    print("Error de posición. Vuelve a intentarlo")
                    continue
                barco=crear_barco(f"P{id_barco}",tamaño,posiciones)
                barcos.append(barco)
                colocar_barco_en_tablero(tablero,barco)
                id_barco+=1
                colocado=True
                imprimir_tableros_lado(tablero,crear_tablero(),jugador,mostrar_barcos=True)
            except Exception as e:
                print("Error inesperado:",e)
    return barcos, tablero, True

""" 
También se ha implementado la colocación automática de barcos para la máquina.
Se permite que los barcos se coloquen de forma aleatoria,
asegurando que no colisionen ni estén adyacentes.
Se han considerado 101 intentos para colocar cada barco antes de abortar para evitar bucles infinitos.
"""
def colocar_barcos_aleatorio_maquina():
    barcos=[]
    tablero=crear_tablero()
    id_barco=1
    for tamaño in flota:
        intentos=0
        colocado=False
        while not colocado and intentos<101:
            intentos+=1
            dir_aleatoria=random.choice(["H","V"])
            if dir_aleatoria=="H":
                f0=random.randrange(0,filas)
                c0=random.randrange(0,columnas-tamaño+1)
                posiciones=[(f0,c0+i) for i in range(tamaño)]
            else:
                f0=random.randrange(0,filas-tamaño+1)
                c0=random.randrange(0,columnas)
                posiciones=[(f0+i,c0) for i in range(tamaño)]
            if se_puede_colocar(posiciones,barcos):
                barco=crear_barco(f"E{id_barco}",tamaño,posiciones)
                barcos.append(barco)
                colocar_barco_en_tablero(tablero,barco)
                id_barco+=1
                colocado=True
        if not colocado:
            raise RuntimeError("No se pudo colocar todos los barcos de la máquina")
    return barcos, tablero

# ------------------------------------------------------------

""" 
Se han implementado funciones para gestionar los ataques y turnos de ambos jugadores.
Procesa un ataque y devuelve el resultado.
Comprueba si todos los barcos de la lista han sido hundidos para determinar el fin del juego.
"""
def recibir_ataque(fila,columna,barcos,tablero_defensa):
    actual=tablero_defensa[fila][columna]
    if actual==tocado:
        return 'ya',None
    for barco in barcos:
        if (fila,columna) in barco["posiciones"]:
            barco["impactos"].add((fila,columna))
            tablero_defensa[fila][columna]=tocado
            if set(barco["posiciones"])==barco["impactos"]:
                colocar_cobertura_en_tablero(tablero_defensa,barco)
                return 'impacto',barco
            else:
                return 'impacto',None
    tablero_defensa[fila][columna]=Fallo
    return 'fallo',None

def todos_barcos_hundidos(barcos):
    return all(set(b["posiciones"])==b["impactos"] for b in barcos)

# ------------------------------------------------------------
""" 
Se han implementado las funciones para gestionar los turnos de ataque del jugador y la máquina.
Hay dos funciones: 
- Gestiona el turno del jugador humano. El jugador introduce las coordenadas de ataque.
- Gestiona el turno de la máquina. La máquina elige aleatoriamente una celda no atacada.
Cada función actualiza los tableros de ataque y defensa según el resultado del ataque.
"""

def turno_jugador(tablero_ataque_jugador, barcos_enemigos, tablero_defensa_enemigo, alias_jugador, tablero_defensa_jugador):
    imprimir_tableros_lado(tablero_defensa_jugador,tablero_ataque_jugador,alias_jugador,mostrar_barcos=True)
    entrada=input("Introduce tu ataque (fila columna) o 'SALIR' para guardar y salir: ").strip().upper()
    if entrada in ("SALIR","Q"):
        return "salir",None
    partes=entrada.replace(","," ").split()
    if len(partes)!=2:
        print("Entrada no válida")
        input("Pulsa Enter para continuar...")
        return False,None
    fila_str,col_str=partes
    if not fila_str.isdigit():
        print("Fila no válida")
        input("Pulsa Enter para continuar...")
        return False,None
    f=int(fila_str)-1
    c=letra_a_indice(col_str)
    if c is None or not celda_valida(f,c):
        print("Coordenada fuera de rango.")
        input("Pulsa Enter para continuar...")
        return False,None
    resultado,barco_hundido=recibir_ataque(f,c,barcos_enemigos,tablero_defensa_enemigo)
    if resultado=='impacto':
        tablero_ataque_jugador[f][c]=tocado
        print("¡Impacto!")
        if barco_hundido is not None:
            print(f"¡Has hundido un barco de tamaño {barco_hundido['tamaño']}!")
        input("Pulsa Enter para continuar...")
        return True,barco_hundido
    elif resultado=='fallo':
        tablero_ataque_jugador[f][c]=Fallo
        print("¡Mala suerte! Has perdido tu turno")
        input("Pulsa Enter para continuar...")
        return False,None
    else:
        print("Posición ya atacada.")
        input("Pulsa Enter para continuar...")
        return False,None

def turno_maquina(tablero_ataque_maquina,barcos_jugador,tablero_defensa_jugador):
    print("Turno de la máquina...")
    opciones=[(f,c) for f in range(filas) for c in range(columnas)
              if tablero_ataque_maquina[f][c] not in (tocado,Fallo)]
    if not opciones:
        return False,None
    f,c=random.choice(opciones)
    print(f"La máquina ataca en {f+1}{letras_columnas[c]} ...")
    resultado,barco_hundido=recibir_ataque(f,c,barcos_jugador,tablero_defensa_jugador)
    if resultado=='impacto':
        tablero_ataque_maquina[f][c]=tocado
        print("¡La máquina ha impactado!")
        input("Pulsa Enter para continuar...")
        return True,barco_hundido
    elif resultado=='fallo':
        tablero_ataque_maquina[f][c]=Fallo
        print("La máquina ha fallado. Te toca a ti.")
        input("Pulsa Enter para continuar...")
        return False,None
    else:
        return False,None
# ------------------------------------------------------------

""" 
Se han implementado funciones para guardar y cargar el estado de la partida.
Se utiliza el módulo pickle para serializar y deserializar el estado del juego.
import pickle
import os

Guarda el estado actual de la partida.
Carga una partida guardada si existe.
"""
def guardar_partida(estado):
    with open(ARCHIVO_PARTIDA,'wb') as f:
        pickle.dump(estado,f)
    print("Partida guardada correctamente.")

def cargar_partida():
    if os.path.exists(ARCHIVO_PARTIDA):
        with open(ARCHIVO_PARTIDA,'rb') as f:
            return pickle.load(f)
    return None