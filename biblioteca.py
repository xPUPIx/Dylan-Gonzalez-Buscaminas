import json
import pygame
import random
from config import *

#-----------------------------  PANTALLA  ------------------------------------------------------

def cambiar_resolucion(resolucion):
    """
    Cambia la resolución de la ventana.
    Recibe: Tupla con ancho y alto de la ventana.
    Retorna: Nueva superficie con la resolución especificada.
    """
    return pygame.display.set_mode(resolucion)

def pantalla_inicio(sonido_mutado: bool, pantalla: pygame.Surface, font_inicio: pygame.font.Font, ancho:tuple, alto:tuple)->None:
    """
    Dibuja la pantalla de inicio del juego.
    Recibe: Sonido, superficie, fuente, dimensiones(width,height)
    Retorna: None.
    """
    pantalla.blit(imagen_fondo, (0, 0))
    dibujar_boton_sonido(sonido_mutado, imagen_unmute, imagen_mute, boton_mute)
    # Crear texto con gradiente
    texto_gradiente = texto_con_gradiente("BUSCAMINAS", font_inicio, (255, 0, 0), (0, 0, 0), ancho, alto)
    pantalla.blit(texto_gradiente, (ancho / 2 - texto_gradiente.get_width() // 2, alto / 2 - 180))

    # Dibujar botones
    pygame.draw.rect(pantalla, (75, 83, 32), boton_nivel)
    pygame.draw.rect(pantalla, (75, 83, 32), boton_jugar)  
    pygame.draw.rect(pantalla, (75, 83, 32), boton_puntajes)
    pygame.draw.rect(pantalla, (115, 18, 18), boton_salir)   
    pantalla.blit(texto_boton_nivel, (boton_nivel.x + 60, boton_nivel.y + 10))
    pantalla.blit(texto_boton_jugar, (boton_jugar.x + 53, boton_jugar.y + 10))
    pantalla.blit(texto_boton_puntajes, (boton_puntajes.x + 30, boton_puntajes.y + 10))
    pantalla.blit(texto_boton_salir, (boton_salir.x + 58, boton_salir.y + 10))


def dibujar_texto(texto: str, fuente:pygame.font.Font, color: tuple[int, int, int], x: int, y: int)->None:
    """
    Dibuja un texto en la pantalla.
    Recibe: 
        texto, fuente, color, desplazamiento_x ,desplazamiento_y 
    Retorna: None.
    """
    img=fuente.render(texto,True,color)
    pantalla.blit(img,(x,y))

#-----------------------------  LOGICA DE MATRICES  ------------------------------------------------


def inicializar_matriz(cant_filas: int, cant_colum: int)->list:
    """
    Crea una matriz de ceros.
    Recibe:
        cant_filas (int) - Cantidad de filas.
        cant_colum (int) - Cantidad de columnas.
    Retorna: list - Matriz con ceros.
    """
    matriz=[]
    for _ in range(cant_filas):
            fila=[0]*cant_colum
            #print(fila)
            matriz.append(fila)
    return matriz

def crear_matriz_buscaminas(cant_filas: int, cant_colum: int, minas: int)->list:
    """
    Genera una matriz con minas colocadas aleatoriamente.
    Recibe:
        Cantidad de filas.
        Cantidad de columnas.
        Cantidad de minas a colocar.
    Retorna una lista
    """
    matriz=inicializar_matriz(cant_filas,cant_colum)
    minas_colocadas=0
    
    while minas_colocadas < minas:
        fila_random=random.randint(0,cant_filas-1)
        columna_random=random.randint(0,cant_colum-1)

        if matriz[fila_random][columna_random]!=-1:
            matriz[fila_random][columna_random]=-1
            minas_colocadas+=1
            
    return matriz


def descrubir_minas_contiguas(cant_filas: int, cant_colum: int, matriz: list[list])->int:
    """
    Calcula la cantidad de minas contiguas a una celda.
    Recibe:
        Fila de la celda.
        Columna de la celda.
        Matriz del tablero.
    Retorna: int - Número de minas contiguas.
    """
    minas=0
    for i in range(cant_filas-1,cant_filas+2):                                              #Pongo -1 y +2 para recorrer las diagonales y los costado
        for j in range(cant_colum-1,cant_colum+2):
            if i >=0 and i<len(matriz):                                                     #verifico que este dentro de las dimensiones de la matriz
                if (j >=0 and j<len(matriz[0]))and (i!=cant_filas or j != cant_colum):      #Lo mismo aca,despues para que no recorra el mismo elemento.
                    if matriz[i][j]==-1:
                        minas+=1
    return minas


def matriz_minas_contiguas(cant_filas: int, cant_column: int, matriz: list[list])->list:
    """
    Calcula la matriz de pistas indicando minas contiguas.
    Recibe:
        Cantidad de filas.
        Cantidad de columnas.
        Matriz del tablero.
    Retorna: list - Matriz con pistas.
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j]==0:
                pistas=descrubir_minas_contiguas(i,j,matriz)                                #Mando la posicion de la matriz a fijar si tiene minas contiguas
                if pistas > 0:
                    matriz[i][j]=pistas
    return matriz


def test_matriz(matriz: list[list])->None:
    """
    Imprime la matriz en consola.
    Recibe: Matriz del tablero.
    Retorna: None.
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f"({matriz[i][j]})",end=" ")
        print("")


def crear_diccionario_estados(cant_filas: int, cant_colum: int)-> dict:
    """
    Crea un diccionario con los estados de las celdas.
    Recibe:
        Cantidad de filas.
        Cantidad de columnas.
    Retorna: dict - Diccionario de estados inicializado en True.
    """
    estados = {}
    for fila in range(cant_filas):
        for col in range(cant_colum):
            estados[(fila, col)] = True
    return estados

def crear_diccionario_banderas(cant_filas: int, cant_colum: int)-> dict:
    """
    Crea un diccionario para las banderas.
    Recibe:
        Cantidad de filas.
        Cantidad de columnas.
    Retorna: dict - Diccionario de banderas inicializado en False.
    """
    banderas = {}
    for fila in range(cant_filas):
        for col in range(cant_colum):
            banderas[(fila, col)] = False
    return banderas


def crear_rectangulos(matriz: list[list], estados:list[dict], pantalla: pygame.Surface, desplazamiento_x: int, desplazamiento_y: int, margen: int=2)->None:
    """
    Dibuja los rectángulos (casillas) del tablero, mostrando su estado (cubierto, descubierto, mina o número).
    
    Recibe:
    matriz: matriz del tablero de buscaminas.
    estados: diccionario con el estado de cada casilla (True = cubierta, False = descubierta).
    pantalla: superficie donde se dibujan los elementos.
    desplazamiento_x: desplazamiento horizontal para dibujar el tablero.
    desplazamiento_y: desplazamiento vertical para dibujar el tablero.
    margen: grosor de las líneas que separan las casillas.
    Retorna:
    None
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            x = desplazamiento_x + j * 40
            y = desplazamiento_y + i * 40
            if i == len(matriz) - 1:
            # Verificar si estamos en la mitad de esa última fila
                if j == len(matriz[i]) // 2:
                    posicion_x = x
                    posicion_y = y
                    
                    bandera = True  # Actualizamos el flag si la condición se cumple
                    
            if estados[(i, j)]:  # Si está cubierto (estando True)
                pantalla.blit(imagen_cuadrado, (x, y))
            elif matriz[i][j] == -1 and estados[(i, j)] == False:  # Si es una mina y descubierto
                pantalla.blit(imagen_mina, (x, y))
            elif matriz[i][j] == 0  and estados[(i, j)] == False:  # Si es un cuadrado vacío
                pygame.draw.rect(pantalla, COLOR_TABLERO, (x, y, 40,40))
            else:  # Si es un número y se lo descubre
                numero = matriz[i][j]
                match numero:
                    case 1:
                        color = (0, 0, 255)  # Azul
                    case 2:
                        color = (0, 128, 0)  # Verde
                    case 3:
                        color = (255, 0, 0)  # Rojo
                    case 4:
                        color = (0, 0, 128)  # Azul oscuro
                    case 5:
                        color = (232, 225, 26)  # Amarillo oscuro ?)
                    case 6:
                        color = (0, 128, 128)  # Verde azulado
                    case 7:
                        color = (128, 0, 0)  # Rojo oscuro
                    case 8:
                        color = (0, 0, 0)  # Negro

                texto = font_inicio.render(str(numero), True, color)
                pantalla.blit(texto, (x + 17, y + 10)) #el +17 y +10 es para centrar el numero y que quede mejor

            pygame.draw.line(pantalla, (0, 0, 0), (x, y), (x + 40, y), margen)  # Línea arriba
            pygame.draw.line(pantalla, (0, 0, 0), (x, y), (x, y + 40), margen)  # Línea izq
            pygame.draw.line(pantalla, (0, 0, 0), (x + 40, y), (x + 40, y + 40), margen)  # Línea der
            pygame.draw.line(pantalla, (0, 0, 0), (x, y + 40), (x + 40, y + 40), margen)  # Linea abajo



def descubre_casillero(estados: list[dict], banderas: list[dict], eventpos: tuple, desplazamiento_x: int, desplazamiento_y: int, matriz: list[list], puntos: int,sonido: pygame.mixer.music)->int:
    """
    Descubre un casillero del tablero si está permitido y actualiza la puntuación.

    Recibe:
    estados: diccionario con el estado de las casillas (cubiertas o descubiertas).
    banderas: diccionario que indica si una casilla tiene bandera.
    eventpos: posición del clic del ratón.
    desplazamiento_x: desplazamiento horizontal del tablero.
    desplazamiento_y: desplazamiento vertical del tablero.
    matriz: matriz del tablero de buscaminas.
    puntos: puntuación actual.

    Retorna:
    La puntuación actualizada. (int)
    """
    mouse_x, mouse_y = eventpos
    fila = (mouse_y - desplazamiento_y) // 40
    columna = (mouse_x - desplazamiento_x) // 40

    if (fila, columna) in estados and banderas[(fila, columna)] == False and estados[(fila, columna)] == True:  # 
        if matriz[fila][columna] == 0:  # Si es un 0, descubre el área
            sonido.play()
            puntos=descubrir_area(matriz, estados, fila, columna,banderas,puntos,sonido)
        else:  # Si es un número, solo descubre esa celda
            estados[(fila, columna)] = False
            sonido.play()
            puntos+=1
    return puntos

def poner_sacar_banderas(estados: list[dict], banderas: list[dict], eventpos: tuple, desplazamiento_x: int, desplazamiento_y: int)->None:
    """
    Coloca o quita una bandera en una casilla seleccionada.

    Recibe:
    estados: diccionario con el estado de las casillas.
    banderas: diccionario que indica si una casilla tiene bandera.
    eventpos: posición del clic del ratón.
    desplazamiento_x: desplazamiento horizontal del tablero.
    desplazamiento_y: desplazamiento vertical del tablero.

    Retorna:
    None
    """
    mouse_x, mouse_y = eventpos
    fila = (mouse_y - desplazamiento_y) // 40
    columna = (mouse_x - desplazamiento_x) // 40
    if (fila, columna) in estados and estados[(fila, columna)] == True: 
        if banderas[(fila, columna)] == False:                              # Si la posicion no está en la misma posicion de una bandera, pone una bandera
            banderas[(fila, columna)] = True
        else:                                                            # Si ya tiene bandera, saca la bandera
            banderas[(fila, columna)]=False


def redibujar_bandera(banderas: list[dict], desplazamiento_x: int, desplazamiento_y: int, eventpos: tuple)->None:
    """
    Redibuja las banderas en el tablero según el diccionario de banderas.

    Recibe:
    banderas: diccionario con las posiciones de las banderas.
    desplazamiento_x: desplazamiento horizontal del tablero.
    desplazamiento_y: desplazamiento vertical del tablero.
    eventpos: posición del evento del ratón.

    Retorna:
    None
    """
    mouse_x,mouse_y = eventpos
    
    fila = (mouse_y - desplazamiento_y) // 40
    columna = (mouse_x - desplazamiento_x) // 40
    for (fila, columna) in banderas:    
        if banderas[(fila,columna)]==True:                                        # Redibujar las banderas
            x = desplazamiento_x + columna * 40
            y = desplazamiento_y + fila * 40
            pantalla.blit(imagen_bandera, (x, y))


def texto_con_gradiente(texto: str, fuente:pygame.font.Font, color_inicio: list[tuple], color_fin: list[tuple], ancho: int, alto: int)->pygame.Surface:
    """
    Genera una superficie de texto con un gradiente de colores.

    Recibe:
    texto: texto a renderizar.
    fuente: fuente utilizada para renderizar el texto.
    color_inicio: color inicial del gradiente.
    color_fin: color final del gradiente.
    ancho: ancho de la superficie.
    alto: alto de la superficie.

    Retorna:
    Superficie con el texto y gradiente aplicado.
    """
    # Renderizar texto en blanco para tomar las dimensiones
    texto_superficie = fuente.render(texto, True, (255, 255, 255))
    texto_rect = texto_superficie.get_rect(center=(ancho // 2, alto // 2))
    
    # Crear superficie para el texto
    superficie = pygame.Surface((texto_rect.width, texto_rect.height), pygame.SRCALPHA)
    
    # Crear gradiente
    for i in range(texto_rect.height):
        # Interpolación lineal entre color_inicio y color_fin
        factor = i / texto_rect.height
        color_actual = (
            int(color_inicio[0] + factor * (color_fin[0] - color_inicio[0])),
            int(color_inicio[1] + factor * (color_fin[1] - color_inicio[1])),
            int(color_inicio[2] + factor * (color_fin[2] - color_inicio[2]))
        )
        pygame.draw.line(superficie, color_actual, (0, i), (texto_rect.width, i))
    
    # Combinar texto y gradiente (multiplicación alfa)
    superficie.blit(texto_superficie, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    return superficie


def manejar_perdida(matriz: list[list], estados: list[dict], eventpos: tuple, desplazamiento_x: int, desplazamiento_y: int, banderas: list[dict],sonido:pygame.mixer.music)->bool:
    """
    Verifica si el jugador pierde al descubrir una mina.

    Recibe:
    matriz: matriz del tablero de buscaminas.
    estados: diccionario con los estados de las casillas.
    eventpos: posición del clic del ratón.
    desplazamiento_x: desplazamiento horizontal del tablero.
    desplazamiento_y: desplazamiento vertical del tablero.
    banderas: diccionario con las posiciones de las banderas.

    Retorna:
    True si se pierde; False en caso contrario. (bool)
    """
    mouse_x, mouse_y = eventpos
    fila = (mouse_y - desplazamiento_y) // 40
    columna = (mouse_x - desplazamiento_x) // 40
    retorno=False
    if (fila, columna) in estados and matriz[fila][columna] == -1 and banderas[(fila,columna)]== False:
        sonido.play()
        retorno=True  # pierde
    return retorno  # no perdio

def limpiar_tablero(estados: list[dict], matriz: list[list], banderas: list[dict])->None:
    """
    Limpia el tablero, estableciendo todos los estados como descubiertos y removiendo las banderas.

    Recibe:
    estados: diccionario con los estados de las casillas.
    matriz: matriz del tablero de buscaminas.
    banderas: diccionario con las posiciones de las banderas.

    Retorna:
    None
    """
    for i in range (len(matriz)):
        for j in range(len(matriz[0])):
            estados[(i,j)] = False
            banderas[(i,j)] = False



def mostrar_niveles(pantalla:pygame.Surface, imagen_fondo:pygame.Surface)->None:
    """
    Dibuja la pantalla de selección de niveles.

    Recibe:
    pantalla: superficie donde se dibujan los elementos.
    imagen_fondo: fondo de la pantalla.

    Retorna:
    None
    """
    pantalla.blit(imagen_fondo, (0, 0))

    pygame.draw.rect(pantalla, (75, 83, 32), boton_facil)
    pygame.draw.rect(pantalla, (75, 83, 32), boton_medio)  
    pygame.draw.rect(pantalla, (75, 83, 32), boton_dificil)   

    pantalla.blit(texto_boton_Facil, (boton_facil.x + 60, boton_facil.y + 10))
    pantalla.blit(texto_boton_medio, (boton_medio.x + 53, boton_medio.y + 10))
    pantalla.blit(texto_boton_Dificil, (boton_dificil.x + 30, boton_dificil.y + 10))



def dibujar_boton_reiniciar(pantalla:pygame.Surface, font: pygame.font.Font, matriz:list[list], x:int, y:int, ancho:int, alto:int)->pygame.Rect:
    """
    Dibuja el botón de reinicio en el tablero.

    Recibe:
    pantalla: superficie donde se dibuja el botón.
    font: fuente del texto del botón.
    matriz: matriz del tablero.
    x: posición horizontal del tablero.
    y: posición vertical del tablero.
    ancho: ancho del botón.
    alto: alto del botón.

    Retorna:
    Objeto Rect del botón.
    """

    x_final=(x+len(matriz[0])*40/2) - (ancho // 2)
    y_final=(y+len(matriz)*40) + 10

    boton = pygame.Rect(x_final, y_final, ancho, alto)
    pygame.draw.rect(pantalla, (75, 83, 32), boton)
    texto_boton_reiniciar=font.render("Reiniciar", True,(255,255,255))
    pantalla.blit(texto_boton_reiniciar, texto_boton_reiniciar.get_rect(center=boton.center))
    
    return boton


def reiniciar_partida(tablero:list[list], estados:list[dict], banderas:list[dict], matriz_completa:list[list], mensaje_perder_mostrado:bool, ganaste:bool,filas,columnas,minas):
    """
    Reinicia la partida creando un nuevo tablero y restableciendo los estados.

    Recibe:
    tablero: tablero actual.
    estados: estados de las casillas.
    banderas: posiciones de las banderas.
    matriz_completa: matriz completa con pistas y minas.
    mensaje_perder_mostrado: estado del mensaje de derrota.
    ganaste: estado de victoria.
    filas: cantidad de filas del tablero.
    columnas: cantidad de columnas del tablero.
    minas: cantidad de minas.

    Retorna:
    Nuevos valores para tablero, estados, banderas, matriz_completa, mensaje_perder_mostrado y ganaste.
    """
    tablero = crear_matriz_buscaminas(filas, columnas, minas)
    estados = crear_diccionario_estados(filas, columnas)
    banderas = crear_diccionario_banderas(filas, columnas)
    matriz_completa = matriz_minas_contiguas(filas, columnas, tablero)
    mensaje_perder_mostrado = False
    ganaste = False
    print("Partida reiniciada.")
    return tablero, estados, banderas, matriz_completa, mensaje_perder_mostrado, ganaste

def descubrir_area(matriz:list[list], estados:list[dict], fila:int, columna:int, banderas:list[dict], puntos:int, sonido:pygame.mixer.music)->int:
    """
    Descubre un área del tablero a partir de una casilla vacía.

    Recibe:
    matriz: matriz del tablero de buscaminas.
    estados: estados de las casillas.
    fila: fila de la casilla inicial.
    columna: columna de la casilla inicial.
    banderas: posiciones de las banderas.
    puntos: puntuación actual.

    Retorna:
    Puntuación actualizada.
    """
    if (fila < 0 or fila >= len(matriz) or columna < 0 or columna >= len(matriz[0]) or estados[(fila, columna)] == False or  banderas[(fila, columna)] == True):
        return puntos
    
    estados[(fila, columna)] = False
    puntos += 1
    if matriz[fila][columna] != 0:
        return puntos
    sonido.play()

    puntos = descubrir_area(matriz, estados, fila - 1, columna, banderas, puntos, sonido)  # Arriba
    puntos = descubrir_area(matriz, estados, fila + 1, columna, banderas, puntos, sonido)  # Abajo
    puntos = descubrir_area(matriz, estados, fila, columna - 1, banderas, puntos, sonido)  # Izquierda
    puntos = descubrir_area(matriz, estados, fila, columna + 1, banderas, puntos, sonido)  # Derecha
    puntos = descubrir_area(matriz, estados, fila - 1, columna - 1, banderas, puntos, sonido)  # Arriba-Izquierda
    puntos = descubrir_area(matriz, estados, fila - 1, columna + 1, banderas, puntos, sonido)  # Arriba-Derecha
    puntos = descubrir_area(matriz, estados, fila + 1, columna - 1, banderas, puntos, sonido)  # Abajo-Izquierda
    puntos = descubrir_area(matriz, estados, fila + 1, columna + 1, banderas, puntos, sonido)  # Abajo-Derecha
    return puntos

def cambiar_estado_sonido(sonido_mutado:bool)->bool:
    """
    Cambia el estado del sonido (mute/unmute).
    Recibe:
    sonido_mutado: estado actual del sonido.
    Retorna:
    Nuevo estado del sonido.
    """
    sonido_mutado = not sonido_mutado
    if sonido_mutado:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(0.1)
    return sonido_mutado

def dibujar_boton_sonido(sonido_mutado:bool, imagen_unmute:pygame.Surface, imagen_mute:pygame.Surface, boton_mute:pygame.rect.Rect)->None:
    """
    Dibuja el botón de sonido según su estado.

    Recibe:
    - sonido_mutado: estado actual del sonido.
    - imagen_unmute: imagen del botón cuando el sonido está activado.
    - imagen_mute: imagen del botón cuando el sonido está desactivado.
    - boton_mute: rectángulo que delimita el botón.

    Retorna:
    - Nada.
    """
    if sonido_mutado:
        pantalla.blit(imagen_mute, boton_mute)
    else:
        pantalla.blit(imagen_unmute, boton_mute)



def verificar_victoria(matriz:list[list], estados:list[dict],cantidad, sonido):
    """
    Verifica si el jugador ha descubierto todas las casillas necesarias para ganar.

    Recibe:
    matriz: matriz del tablero de buscaminas.
    estados: estados de las casillas.
    cantidad: número de minas en el tablero.

    Retorna:
    True si se gana; False en caso contrario.
    """
    ganar = len(matriz)*len(matriz[0])-cantidad
    
    contador_espacios_descubiertos = 0
    victoria=False

    for i in range (len(matriz)):
        for j in range(len(matriz[i])):
            if estados[(i,j)] == False:
                contador_espacios_descubiertos += 1
    if contador_espacios_descubiertos == ganar:
        sonido.play()
        victoria = True
    return victoria


def contador_reloj(segundos_totales:int)->tuple:
    """
    Simula un reloj digital actualizando minutos y segundos.

    parametros:
        segundos_totales (int): Contador total de segundos.

    Returns:
        tupla: (minutos, segundos) actualizados.
    """
    segundos = segundos_totales % 60
    minutos = segundos_totales // 60
    return minutos, segundos


def dibujar_boton_volver(pantalla:pygame.Surface, boton_volver:pygame.rect.Rect, texto_boton_volver:pygame.font.Font)->None:
    """
    Dibuja un boton en la pantalla que sirve para volver al menu

    Recibe:
    pantalla: superficie donde se dibuja el botón.
    boton_volver: rect
    texto_boton_volver: fuente

    Retorna:
    None
    """
    pygame.draw.rect(pantalla, (75, 83, 32), boton_volver)
    pantalla.blit(texto_boton_volver, (boton_volver.x + 20, boton_volver.y + 5))


def dibujar_fondo_tablero(pantalla:pygame.Surface, matriz_completa:list[list], COLOR_TABLERO:tuple)->None:
    """
    Dibuja un fondo detrás del tablero del juego para evitar que la imagen de fondo afecte
    los casilleros descubiertos.

    Recibe:
    pantalla: superficie donde se dibuja el botón.
    matriz_completa: matriz del tablero de buscaminas con sus pistas incluidas.
    COLOR_TABLERO: tupla constante con 3 valores de int RGB

    Retorna:
    None
    """
    filas = len(matriz_completa)
    columnas = len(matriz_completa[0])
    
    # Calcular las dimensiones exactas del fondo que cubrirán el tablero
    ancho_tablero = columnas * (40)
    alto_tablero = filas * (40)
    
    # Calcular el desplazamiento para centrar el fondo
    desplazamiento_x = (PANTALLA_ANCHO - ancho_tablero) // 2
    desplazamiento_y = (PANTALLA_ALTO - alto_tablero) // 2
    
    # Dibujar el fondo con el tamaño adecuado
    pygame.draw.rect(pantalla, COLOR_TABLERO, (desplazamiento_x, desplazamiento_y, ancho_tablero, alto_tablero))


def mostrar_fondo_puntajes(pantalla:pygame.Surface, imagen_fondo:pygame.Surface)->None:
    """
    blitea el fondo de pantalla en la seccion de puntajes
    
    Recibe:
        la pantalla donde blitear (superficie)
        imagen_fondo es la superficie que se va a blitear sobre la pantalla
    
    Retorna 
    None
    """
    pantalla.blit(imagen_fondo, (0, 0))


def pedir_usuario(pantalla:pygame.Surface, font:pygame.Surface, imagen_fondo:pygame.Surface)->str:
    """
    blitea el fondo de pantalla en la seccion de puntajes
    
    Recibe:
        la pantalla donde blitear (superficie)
        font es la fuente que se va a utiliazr (pygame.Font)
        imagen_fondo es la superficie que se va a blitear sobre la pantalla
    
    Retorna 
    str  (el string del nombre)
    """
    nombre = ""
    ingresar_nombre_usuario = True

    while ingresar_nombre_usuario:
        pantalla.blit(imagen_fondo, (0,0))
        texto = font.render("Ingrese su Nickname:", True, (255, 255, 255))
        pantalla.blit(texto, (150, 300))

        # Mostrar el nombre ingresado
        nombre_render = font.render(nombre, True, (255, 255, 255))
        pantalla.blit(nombre_render, (150, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if nombre.strip():
                        ingresar_nombre_usuario = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12:
                        nombre += event.unicode
    return nombre


def guardar_puntaje(nombre:str, puntos:int, contador:int)->None:
    """
    la funcion abre el archivo json y le carga un nuevo diccionario con las claves de nombre-puntaje-tiempo
    
    Recibe:
        Nombre como string
        puntos como int
        contador como int
    
    Retorna 
    None
    """

    archivo_puntajes = "database/puntajes.json"

    try:
        with open(archivo_puntajes, "r") as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = []

    nombre_existente = False
    for registro in puntajes:
        if registro["nombre"] == nombre:        #FALTA ARREGLAR SI ES MENOR EL PUNTAJE 
            registro["puntaje"] = puntos
            registro["Tiempo"] = contador
            nombre_existente = True
            break

    if nombre_existente == False:
        puntajes.append({"nombre": nombre, "puntaje": puntos, "Tiempo": contador})

    with open(archivo_puntajes, "w") as archivo:
        json.dump(puntajes, archivo, indent=4)



def mostrar_puntos_tablero(pantalla:pygame.Surface, puntos, fuente:pygame.font.Font, color_rect:tuple[int,int,int], color_texto:tuple[int,int,int], x:int, y:int, ancho:int, alto:int)->None:
    """
    Define y dibuja un rectangulo, luego toma el texto de los puntajes y lo renderiza para usarlo como superficie y poder blitearlo
    
    Recibe:
        pantalla donde blitear (superficie)
        puntos como int
        fuente utilizada (Font)
        color_rect es una tupla con valor de color RGB
        color_texto una tupla con valor de color RGB
        x para calcular la posicion en el ancho de la pantalla (int)
        y para calcular la posicion en el alto de la pantalla (int)
        ancho el valor del ancho de la pantalla (itn)
        alto el valor del ancho de la pantalla (itn)
    
    Retorna 
    None
    """
    rectangulo_puntos = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, color_rect, rectangulo_puntos)

    texto_puntaje = str(f"{puntos:04}")
    texto_renderizado = fuente.render(texto_puntaje, True, color_texto)

    texto_rect = texto_renderizado.get_rect(center=rectangulo_puntos.center)
    pantalla.blit(texto_renderizado, texto_rect)


def dibujar_boton_timer(pantalla:pygame.Surface, texto_boton_timer:pygame.Surface, ancho:int, alto:int, x:int, y:int)->None:
    """
    define el valor de un nuevo rectangulo con respecto a las dimenciones y posicion que se le pasa por parametros, se dibuja el rectangulo
    se toma el texto renderizado como superficie y centrado
    se blitea el nuevo boton con su texto

    Recibe:
        pantalla donde blitear (superficie)
        texto_boton_timer superficie con el texto de str renderizado
        ancho el valor del ancho de la pantalla (itn)
        alto el valor del ancho de la pantalla (itn)
        x para calcular la posicion en el ancho de la pantalla (int)
        y para calcular la posicion en el alto de la pantalla (int)
    
    Retorna 
    None
    """
    boton_timer = pygame.Rect(x,y, ancho, alto)
    pygame.draw.rect(pantalla, (75, 83, 32), boton_timer)
    texto_rect = texto_boton_timer.get_rect(center = boton_timer.center)
    pantalla.blit(texto_boton_timer, texto_rect)


def acomodar_jugadores(archivo_puntajes:json)->list:
    """
    ordena por puntos los primeros 3 jugadores con más puntos del archivo json
    
    Recibe:
        pantalla donde blitear (superficie)
        puntos como int
        fuente utilizada (Font)
        color_rect es una tupla con valor de color RGB
        color_texto una tupla con valor de color RGB
        x para calcular la posicion en el ancho de la pantalla (int)
        y para calcular la posicion en el alto de la pantalla (int)
        ancho el valor del ancho de la pantalla (itn)
        alto el valor del ancho de la pantalla (itn)
    
    Retorna 
    retorna la lista de puntajes
    """


    try:
        with open(archivo_puntajes, "r") as archivo:
            puntajes = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        puntajes = []

    puntajes.sort(key=lambda dic: dic["puntaje"],reverse=True)

    with open(archivo_puntajes, "w") as archivo:
        json.dump(puntajes, archivo, indent=4)

    return puntajes


def mostrar_mejores_puntajes(pantalla:pygame.Surface, font:pygame.font.Font, font_2:pygame.font.Font, puntajes:list, x:int, y:int, ancho:int, alto:int, espacio:int)->None:
    """
    itera sobre 
    
    Recibe:
        pantalla donde blitear (superficie)
        font  es la fuenteutilizada (Font)
        font_2 segunda fuente (es mas grande, es un Font)
        puntajes es la lista de los valores ordenados
        x para calcular la posicion en el ancho de la pantalla (int)
        y para calcular la posicion en el alto de la pantalla (int)
        ancho el valor del ancho de la pantalla (itn)
        alto el valor del ancho de la pantalla (itn)
        espacio es el int que mide la separacion entre los rect
    
    Retorna 
    None
    """

    for i in range(0,3):

        nombre = puntajes[i]["nombre"]
        puntaje = puntajes[i]["puntaje"]
        tiempo = puntajes[i]["Tiempo"]

        if i == 1:
            x_pos = pantalla.get_width() - ancho - x
        elif i == 2:
            x_pos = x
        elif i == 0:
            x_pos = pantalla.get_width() // 2 - ancho // 2

        nombre_y = y
        puntaje_y = nombre_y + alto + espacio
        tiempo_y = puntaje_y + alto + espacio

        rect_nombre = pygame.Rect(x_pos, nombre_y, ancho, alto) 
        rect_puntaje = pygame.Rect(x_pos, puntaje_y, ancho, alto) 
        rect_tiempo = pygame.Rect(x_pos, tiempo_y, ancho, alto)
        rect_titulo = pygame.Rect(300,250, 0, 0)


        pygame.draw.rect(pantalla, (0,0,0), rect_titulo)
        pygame.draw.rect(pantalla, (150, 150, 150), rect_nombre)  
        pygame.draw.rect(pantalla, (150, 150, 150), rect_puntaje)  
        pygame.draw.rect(pantalla, (150, 150, 150), rect_tiempo)  

        texto_nombre = font.render(f"{nombre}", True, "white")
        texto_puntaje = font.render(f"Puntaje: {puntaje}", True, "white")
        texto_tiempo = font.render(f"Tiempo: {tiempo}", True, "white")
        texto_titulo = font_2.render("Puntajes", True, "white")

        pantalla.blit(texto_nombre, texto_nombre.get_rect(center=rect_nombre.center))
        pantalla.blit(texto_puntaje, texto_puntaje.get_rect(center=rect_puntaje.center))
        pantalla.blit(texto_tiempo, texto_tiempo.get_rect(center=rect_tiempo.center))
        pantalla.blit(texto_titulo, texto_titulo.get_rect(center=rect_titulo.center))