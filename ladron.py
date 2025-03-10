import pygame
from config import *
from mapa import PASILLO  # Añadir esta línea

class Ladron(pygame.sprite.Sprite):
    def __init__(self, posicion_inicial):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.center = posicion_inicial
        self.velocidad = 2 # Ajusta este valor para cambiar la velocidad del ladrón
    
    def update(self, teclas, mapa, celda_ancho, celda_alto):
        movimiento_x = 0
        movimiento_y = 0
        if teclas[pygame.K_LEFT]:
            movimiento_x = -self.velocidad
        if teclas[pygame.K_RIGHT]:
            movimiento_x = self.velocidad
        if teclas[pygame.K_UP]:
            movimiento_y = -self.velocidad
        if teclas[pygame.K_DOWN]:
            movimiento_y = self.velocidad

        nueva_pos_x = self.rect.x + movimiento_x
        nueva_pos_y = self.rect.y + movimiento_y

        x = nueva_pos_x // celda_ancho
        y = nueva_pos_y // celda_alto
        
        if 0 <= x < len(mapa[0]) and 0 <= y < len(mapa) and mapa[y][x] == PASILLO:
            self.rect.x = nueva_pos_x
            self.rect.y = nueva_pos_y
