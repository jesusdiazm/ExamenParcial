import pygame
import random
from config import *
from ladron import Ladron
from guardia import Guardia
from astar import *
from mapa import MAPA, PASILLO, PARED

pygame.init()

CELDA_ANCHO = 50
CELDA_ALTO = 50

pantalla = pygame.display.set_mode((len(MAPA[0]) * CELDA_ANCHO, len(MAPA) * CELDA_ALTO))
pygame.display.set_caption("Ladrón de Supermercado")

# Inicialización de personajes y objetos
ladron = Ladron((CELDA_ANCHO + CELDA_ANCHO//2, CELDA_ALTO + CELDA_ALTO//2))
guardias = pygame.sprite.Group(Guardia((2 * CELDA_ANCHO + CELDA_ANCHO//2, 2 * CELDA_ALTO + CELDA_ALTO//2)), 
                              Guardia((4 * CELDA_ANCHO + CELDA_ANCHO//2, 2 * CELDA_ALTO + CELDA_ALTO//2)), 
                              Guardia((6 * CELDA_ANCHO + CELDA_ANCHO//2, 2 * CELDA_ALTO + CELDA_ALTO//2)))
botines = pygame.sprite.Group()  # Añadir los botines aquí
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
        
        ladron.update(teclas, MAPA, CELDA_ANCHO, CELDA_ALTO)
        guardias.update(ladron, MAPA, CELDA_ANCHO, CELDA_ALTO)

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
