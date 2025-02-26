import pygame
import random
from config import *
from astar import *
from mapa import PASILLO  # Añadir esta línea

class Guardia(pygame.sprite.Sprite):
    def __init__(self, posicion_inicial):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = posicion_inicial
        self.direccion = random.choice(['izquierda', 'derecha', 'arriba', 'abajo'])
        self.velocidad = 1  # Ajusta este valor para cambiar la velocidad de los guardias
    
    def update(self, ladron, mapa, celda_ancho, celda_alto):
        if self.ver_ladron(ladron):
            path = a_star(self.rect.center, ladron.rect.center, mapa, celda_ancho, celda_alto)
            if path and len(path) > 1:
                next_pos = path[1]  # La siguiente posición en el camino A*
                self.rect.center = next_pos
        else:
            self.mover_aleatorio(mapa, celda_ancho, celda_alto)
    
    def ver_ladron(self, ladron):
        distancia = ((self.rect.x - ladron.rect.x) ** 2 + (self.rect.y - ladron.rect.y) ** 2) ** 0.5
        return distancia < 100

    def mover_aleatorio(self, mapa, celda_ancho, celda_alto):
        if self.direccion == 'izquierda':
            nueva_pos_x = self.rect.x - self.velocidad
            nueva_pos_y = self.rect.y
        elif self.direccion == 'derecha':
            nueva_pos_x = self.rect.x + self.velocidad
            nueva_pos_y = self.rect.y
        elif self.direccion == 'arriba':
            nueva_pos_x = self.rect.x
            nueva_pos_y = self.rect.y - self.velocidad
        elif self.direccion == 'abajo':
            nueva_pos_x = self.rect.x
            nueva_pos_y = self.rect.y + self.velocidad

        x = nueva_pos_x // celda_ancho
        y = nueva_pos_y // celda_alto

        if 0 <= x < len(mapa[0]) and 0 <= y < len(mapa) and mapa[y][x] == PASILLO:
            self.rect.x = nueva_pos_x
            self.rect.y = nueva_pos_y
        else:
            self.direccion = random.choice(['izquierda', 'derecha', 'arriba', 'abajo'])

class Nodo:
    def ejecutar(self):
        pass

class Selector(Nodo):
    def __init__(self, *nodos):
        self.nodos = nodos

    def ejecutar(self):
        for nodo in self.nodos:
            if nodo.ejecutar():
                return True
        return False

class Secuencia(Nodo):
    def __init__(self, *nodos):
        self.nodos = nodos

    def ejecutar(self):
        for nodo in self.nodos:
            if not nodo.ejecutar():
                return False
        return True

class VerLadron(Nodo):
    def __init__(self, guardia, ladron):
        self.guardia = guardia
        self.ladron = ladron

    def ejecutar(self):
        return self.guardia.ver_ladron(self.ladron)

class Patrullar(Nodo):
    def __init__(self, guardia):
        self.guardia = guardia

    def ejecutar(self):
        self.guardia.mover_aleatorio(self.guardia.mapa, self.guardia.celda_ancho, self.guardia.celda_alto)
        return True

class Perseguir(Nodo):
    def __init__(self, guardia, ladron, mapa, celda_ancho, celda_alto):
        self.guardia = guardia
        self.ladron = ladron
        self.mapa = mapa
        self.celda_ancho = celda_ancho
        self.celda_alto = celda_alto

    def ejecutar(self):
        path = a_star(self.guardia.rect.center, self.ladron.rect.center, self.mapa, self.celda_ancho, self.celda_alto)
        if path and len(path) > 1:
            next_pos = path[1]  # La siguiente posición en el camino A*
            self.guardia.rect.center = next_pos
        return True

def inicializar_arbol_comportamiento(guardia, ladron, mapa, celda_ancho, celda_alto):
    return Selector(
        VerLadron(guardia, ladron),
        Secuencia(
            VerLadron(guardia, ladron),
            Perseguir(guardia, ladron, mapa, celda_ancho, celda_alto)
        ),
        Patrullar(guardia)
    )
