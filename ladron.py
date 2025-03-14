import pygame
import random
from config import *
from mapa import PASILLO  # Asegúrate de tener esta línea

class Ladron(pygame.sprite.Sprite):
    def __init__(self, posicion_inicial, imagen_ladron_path):
        super().__init__()
        # Cargar la imagen del ladrón desde la ruta proporcionada
        self.image = pygame.image.load("assets/images/ladron.png")  # Ruta de la imagen
        self.image = pygame.transform.scale(self.image, (30, 30))  # Escalar la imagen al tamaño deseado
        self.rect = self.image.get_rect()
        self.rect.center = posicion_inicial

        self.velocidad = 200  # Velocidad en píxeles por segundo

    def update(self, teclas, mapa, celda_ancho, celda_alto, delta_time):
        movimiento_x = 0
        movimiento_y = 0

        # Detectar teclas presionadas y calcular movimiento
        if teclas[pygame.K_LEFT]:
            movimiento_x = -self.velocidad * delta_time
        if teclas[pygame.K_RIGHT]:
            movimiento_x = self.velocidad * delta_time
        if teclas[pygame.K_UP]:
            movimiento_y = -self.velocidad * delta_time
        if teclas[pygame.K_DOWN]:
            movimiento_y = self.velocidad * delta_time

        # Calcular la nueva posición
        nueva_pos_x = self.rect.x + movimiento_x
        nueva_pos_y = self.rect.y + movimiento_y
        x = int(nueva_pos_x // celda_ancho)
        y = int(nueva_pos_y // celda_alto)

        # Validar que el ladrón no salga del pasillo
        if 0 <= x < len(mapa[0]) and 0 <= y < len(mapa) and mapa[y][x] == PASILLO:
            self.rect.x = nueva_pos_x
            self.rect.y = nueva_pos_y
        else:
            print(f"Ladrón intentó moverse fuera del pasillo a ({x}, {y})")
