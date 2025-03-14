import pygame
import random
from config import *
from ladron import Ladron
from guardia import Guardia
from astar import *
from mapa import MAPA, PASILLO, PARED

pygame.init()

pygame.mixer.init()

#Cargar el audio de fondo
pygame.mixer.music.load("assets/audio/sound.mp3")  # Ruta del archivo de audio
pygame.mixer.music.set_volume(0.5)  # Volumen del 0.0 al 1.0
pygame.mixer.music.play(-1)  # Repetir indefinidamente (-1)

pantalla = pygame.display.set_mode((len(MAPA[0]) * CELDA_ANCHO, len(MAPA) * CELDA_ALTO))
pygame.display.set_caption("Ladrón de Supermercado")

# Crea un reloj
clock = pygame.time.Clock()

# Función para obtener posiciones válidas (solo pasillos)
def obtener_posiciones_validas(mapa):
    posiciones_validas = []
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):
            if celda == PASILLO:  # Solo agregar celdas que son pasillos
                posiciones_validas.append((x, y))
    return posiciones_validas

# Obtener posiciones válidas desde el mapa
posiciones_validas = obtener_posiciones_validas(MAPA)

# Inicialización de personajes y objetos
# Posición inicial del ladrón
x, y = random.choice(posiciones_validas)


#posicion_ladron = (x * CELDA_ANCHO + CELDA_ANCHO // 2, y * CELDA_ALTO + CELDA_ALTO // 2)
posicion_ladron = (200, 100)
#ladron = Ladron(posicion_ladron)
ladron = Ladron(posicion_ladron, "assets/images/ladron.png")

# Inicialización de los guardias
guardias = pygame.sprite.Group()
for _ in range(3):  # Número de guardias (ajustable)
    x, y = random.choice(posiciones_validas)
#    posicion_guardia = (x * CELDA_ANCHO + CELDA_ANCHO // 2, y * CELDA_ALTO + CELDA_ALTO // 2)
#    guardia = Guardia(posicion_guardia)
    
    # Posición inicial del guardia
    posicion_guardia = (100, 150)

    # Crear el guardia pasando la posición y la ruta de la imagen
    guardia = Guardia(posicion_guardia, "assets/images/guardia.png")

    guardias.add(guardia)

# Agrupa todos los sprites
todos_los_sprites = pygame.sprite.Group(ladron, *guardias)

def dibujar_mapa(pantalla, mapa):
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):
            if celda == PARED:
                color = NEGRO
            elif celda == PASILLO:
                color = BLANCO
            pygame.draw.rect(pantalla, color, (x * CELDA_ANCHO, y * CELDA_ALTO, CELDA_ANCHO, CELDA_ALTO))

def bucle_juego():
    corriendo = True
    while corriendo:
        teclas = pygame.key.get_pressed()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        # Actualización del tiempo en milisegundos convertido a segundos
        delta_time = clock.tick(60) / 1000.0  # Convierte milisegundos a segundos
        
        # Actualización de los personajes
        ladron.update(teclas, MAPA, CELDA_ANCHO, CELDA_ALTO, delta_time)
        guardias.update(ladron, MAPA, CELDA_ANCHO, CELDA_ALTO, delta_time)  

        # Dibuja todo
        pantalla.fill(COLOR_FONDO)
        dibujar_mapa(pantalla, MAPA)
        todos_los_sprites.draw(pantalla)
        pygame.display.flip()
    
    pygame.quit()

def mostrar_texto(texto, tamano, color, x, y):
    fuente = pygame.font.Font(None, tamano)
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

def menu_principal():
    menu = True
    while menu:
        pantalla.fill(NEGRO)
        mostrar_texto("LADRÓN DE SUPERMERCADO", 50, BLANCO, len(MAPA[0]) * CELDA_ANCHO // 2, len(MAPA) * CELDA_ALTO // 4)
        mostrar_texto("1. Iniciar Juego", 40, BLANCO, len(MAPA[0]) * CELDA_ANCHO // 2, len(MAPA) * CELDA_ALTO // 2)
        mostrar_texto("2. Salir", 40, BLANCO, len(MAPA[0]) * CELDA_ANCHO // 2, len(MAPA) * CELDA_ALTO // 2 + 50)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                menu = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:  # Opción para iniciar el juego
                    menu = False
                    bucle_juego()
                elif evento.key == pygame.K_2:  # Opción para salir
                    menu = False
        
        pygame.display.flip()

menu_principal()
   