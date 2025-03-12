import pygame
import random
from config import *
from astar import *
from mapa import PASILLO  # Añadir esta línea

class Guardia(pygame.sprite.Sprite):
    def __init__(self, posicion_inicial):
        super().__init__()
        self.image = pygame.Surface((TAM_GUARDIA, TAM_GUARDIA))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = posicion_inicial
        self.velocidad = 5  # Velocidad predeterminada
        self.direccion = random.choice(['izquierda', 'derecha', 'arriba', 'abajo'])  # Inicialización de dirección
        self.camino = []  # Usado para A*


    def update(self, ladron, mapa, celda_ancho, celda_alto, delta_time):
        if self.ver_ladron(ladron):  # Si el ladrón está visible
            # Convertir posiciones en píxeles a índices del mapa
            inicio = (self.rect.centerx // celda_ancho, self.rect.centery // celda_alto)
            meta = (ladron.rect.centerx // celda_ancho, ladron.rect.centery // celda_alto)
            
            # Validar que ambas posiciones estén en pasillos
            if mapa[inicio[1]][inicio[0]] != PASILLO or mapa[meta[1]][meta[0]] != PASILLO:
                print(f"Error: Guardia en {inicio} o ladrón en {meta} no están en un pasillo.")
                return
            
            # Depuración: Imprimir posiciones iniciales y meta
            print(f"Inicio: {inicio}, Meta: {meta}")
            
            # Calcular la ruta usando A*
            self.camino = a_star(inicio, meta, mapa, celda_ancho, celda_alto)
            print(f"Ruta hacia ladrón: {self.camino}")  # Depuración: Imprimir la ruta
            
            if self.camino and len(self.camino) > 1:
                self.mover_hacia(self.camino[1], delta_time)  # Ir al siguiente paso
        else:
            self.mover_aleatorio(mapa, celda_ancho, celda_alto, delta_time)

            
            


    def ver_ladron(self, ladron):
        distancia = ((self.rect.centerx - ladron.rect.centerx) ** 2 + (self.rect.centery - ladron.rect.centery) ** 2) ** 0.5
        return distancia < 200  # Ajusta este valor según el rango de visión que desees


    def mover_hacia(self, destino, delta_time):
        dx, dy = destino[0] - self.rect.centerx, destino[1] - self.rect.centery
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        if distancia > 1: # Moverse solo si la distancia es mayor a 1 píxel
            direccion_x = dx / distancia
            direccion_y = dy / distancia
            # Moverse hacia el destino usando velocidad y delta_time
            self.rect.x += int(direccion_x * self.velocidad * delta_time)
            self.rect.y += int(direccion_y * self.velocidad * delta_time)
            
            print(f"Moviendo hacia: {destino}, dx: {dx}, dy: {dy}")

            
        else:
            print("Destino alcanzado o demasiado cerca para moverse.")


    def mover_aleatorio(self, mapa, celda_ancho, celda_alto, delta_time):
        desplazamiento_x, desplazamiento_y = 0, 0
        if self.direccion == 'izquierda':
            desplazamiento_x = -self.velocidad * delta_time
        elif self.direccion == 'derecha':
            desplazamiento_x = self.velocidad * delta_time
        elif self.direccion == 'arriba':
            desplazamiento_y = -self.velocidad * delta_time
        elif self.direccion == 'abajo':
            desplazamiento_y = self.velocidad * delta_time

        nueva_pos_x = self.rect.x + desplazamiento_x
        nueva_pos_y = self.rect.y + desplazamiento_y
        x = int(nueva_pos_x // celda_ancho)
        y = int(nueva_pos_y // celda_alto)

        # Validación para moverse solo en pasillos
        if 0 <= x < len(mapa[0]) and 0 <= y < len(mapa) and mapa[y][x] == PASILLO:
            self.rect.x = nueva_pos_x
            self.rect.y = nueva_pos_y
        else:
            # Cambiar de dirección si encuentra un obstáculo
            self.direccion = random.choice(['izquierda', 'derecha', 'arriba', 'abajo'])


