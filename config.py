import pygame

#-----------------------------  PANTALLA  ------------------------------------------------

# pantalla_alto = 760
# pantalla_ancho = 600
# resolucion_pantalla = (pantalla_ancho, pantalla_alto)

PANTALLA_ALTO = 760
PANTALLA_ANCHO = 600
RESOLUCION_PANTALLA = (PANTALLA_ANCHO, PANTALLA_ALTO)

INICIO_ALTO=760
INICIO_ANCHO=600
RESOLUCION_INICIO=(INICIO_ANCHO,INICIO_ALTO)
pantalla = pygame.display.set_mode(RESOLUCION_PANTALLA)
pantalla_inicio_2 = pygame.display.set_mode(RESOLUCION_INICIO)
color_fondo = [127, 157, 235]
posicion_personaje = [400, 300]



#-----------------------------  AUDIO  -------------------------------------------------

pygame.mixer.init()
pygame.mixer.music.load("audio/cancion.mp3")

sonido_click = pygame.mixer.Sound("audio/click_casillero.mp3")
sonido_click.set_volume(1.0)  # Ajusta el volumen (opcional)
sonido_bomba=pygame.mixer.Sound("audio/sonido_perder.mp3")
sonido_bomba.set_volume(0.015)
sonido_ganar=pygame.mixer.Sound("audio/sound_ganar.mp3")
sonido_ganar.set_volume(0.3)

#-----------------------------  COLORES  -------------------------------------------------

# Colores: RGB[A] (Red, Green, Blue) [Alpha] -> 0 - 255

COLOR_TABLERO = (169, 169, 169)

#----------------------------  FUENTE   -------------------------------------------------

pygame.font.init()

font_inicio=pygame.font.Font("font/mifuente.otf",24)
font_timer = pygame.font.Font("font/mifuente.otf",24)
font_puntajes = pygame.font.Font("font/mifuente.otf",16)


#---------------------------  IMAGENES  -------------------------------------------------

icono=pygame.image.load("img/logo_app.png")

imagen_mute = pygame.image.load("img/muteado.png")
imagen_mute = pygame.transform.scale(imagen_mute, (60, 60))
imagen_unmute = pygame.image.load("img/sonido.png")
imagen_unmute = pygame.transform.scale(imagen_unmute, (60, 60))

imagen_cuadrado=pygame.image.load("img/CUADRADO_BUSCAMINA.jpg")
imagen_cuadrado=pygame.transform.scale(imagen_cuadrado,(40,40))

imagen_mina = pygame.image.load("img/mina.png")
imagen_mina = pygame.transform.scale(imagen_mina, (40,40))

imagen_bandera = pygame.image.load("img/bandera.png")
imagen_bandera = pygame.transform.scale(imagen_bandera, (40,40))

imagen_fondo = pygame.image.load("img/fondo_menu.jpg")
imagen_fondo = pygame.transform.scale(imagen_fondo, (RESOLUCION_INICIO))

imagen_fondo_juego = pygame.image.load("img/fondo_juego.jpg")
imagen_fondo_juego = pygame.transform.scale(imagen_fondo_juego, (RESOLUCION_PANTALLA))

imagen_fondo_puntajes = pygame.image.load("img/fondo_puntajes.jpg")
imagen_fondo_puntajes = pygame.transform.scale(imagen_fondo_puntajes, (RESOLUCION_INICIO))

imagen_fondo_puntajes_final = pygame.image.load("img/fondo_puntajes.jpg")
imagen_fondo_puntajes_final = pygame.transform.scale(imagen_fondo_puntajes, (RESOLUCION_PANTALLA))

imagen_reiniciar = pygame.image.load("img/boton_reinicio.png")
imagen_reiniciar = pygame.transform.scale(imagen_reiniciar, (75, 75))

#--------------------------- BOTONES  --------------------------------------------------

boton_ancho = 200
boton_alto = 50

boton_mute = pygame.Rect(500, 40, 50, 50)

boton_nivel = pygame.Rect(200, 300, boton_ancho, boton_alto)
boton_jugar = pygame.Rect(200, 375, boton_ancho, boton_alto)
boton_puntajes = pygame.Rect(200, 450, boton_ancho, boton_alto)
boton_salir = pygame.Rect(200, 525, boton_ancho, boton_alto)

boton_facil = pygame.Rect(200, 300, boton_ancho, boton_alto)
boton_medio = pygame.Rect(200, 375, boton_ancho, boton_alto)
boton_dificil = pygame.Rect(200, 450, boton_ancho, boton_alto)
boton_reiniciar = pygame.Rect(263,650, boton_ancho, boton_alto )

boton_volver = pygame.Rect(25, 10, 150, 40)
boton_volver = pygame.Rect(25, 10, 150, 40)

#--------------------------- TEXTO DE BOTONES  ----------------------------------------

texto_boton_nivel=font_inicio.render("Nivel",True,(255,255,255))
texto_boton_jugar=font_inicio.render("Jugar",True,(255,255,255))
texto_boton_puntajes=font_inicio.render("Puntajes",True,(255,255,255))
texto_boton_salir=font_inicio.render("Salir",True,(255,255,255))

texto_boton_reiniciar=font_inicio.render("Reiniciar", True,(255,255,255))

texto_boton_Facil=font_inicio.render("Facil",True,(255,255,255))
texto_boton_medio=font_inicio.render("Medio",True,(255,255,255))
texto_boton_Dificil=font_inicio.render("Dificil",True,(255,255,255))

texto_boton_volver = font_inicio.render("VOLVER", True, (255, 255, 255))
