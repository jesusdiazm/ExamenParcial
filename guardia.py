import pygame
import random
from astar import a_star
from mapa import PASILLO

# Nodos del árbol de comportamiento
class NodoComportamiento:
    def ejecutar(self, guardia):
        raise NotImplementedError

class Selector(NodoComportamiento):
    def __init__(self, nodos):
        self.nodos = nodos

    def ejecutar(self, guardia):
        for nodo in self.nodos:
            if nodo.ejecutar(guardia):  # Ejecuta hasta que un nodo tenga éxito
                return True
        return False

class Patrullar(NodoComportamiento):
    def ejecutar(self, guardia):
        print("Guardia está patrullando...")
        guardia.mover_aleatorio(guardia.mapa, guardia.celda_ancho, guardia.celda_alto, guardia.delta_time)
        return True

class Perseguir(NodoComportamiento):
    def ejecutar(self, guardia):
        if guardia.ver_ladron(guardia.ladron):
            print("Guardia persiguiendo al ladrón...")
            inicio = (guardia.rect.centerx // guardia.celda_ancho, guardia.rect.centery // guardia.celda_alto)
            meta = (guardia.ladron.rect.centerx // guardia.celda_ancho, guardia.ladron.rect.centery // guardia.celda_alto)

            # Validar que inicio y meta están en celdas válidas
            if guardia.mapa[inicio[1]][inicio[0]] != PASILLO or guardia.mapa[meta[1]][meta[0]] != PASILLO:
                print(f"Error: Guardia en {inicio} o ladrón en {meta} no están en un pasillo.")
                return False

            guardia.camino = a_star(inicio, meta, guardia.mapa, guardia.celda_ancho, guardia.celda_alto)
            if guardia.camino and len(guardia.camino) > 1:
                guardia.mover_hacia(guardia.camino[1], guardia.delta_time)
            return True
        return False

class Esperar(NodoComportamiento):
    def ejecutar(self, guardia):
        print("Guardia está esperando...")
        return True

# Clase principal del guardia
class Guardia(pygame.sprite.Sprite):
    def __init__(self, posicion_inicial, imagen_guardia_path):
        super().__init__()
        # Cargar la imagen del guardia
        self.image = pygame.image.load("assets/images/guardia.png") # Ruta de la imagen del guardia
        self.image = pygame.transform.scale(self.image, (30, 30))  # Escalar la imagen al tamaño deseado
        self.rect = self.image.get_rect()
        self.rect.center = posicion_inicial

        self.velocidad = 200  # Ajusta la velocidad del guardia
        self.camino = []  # Lista de pasos calculados por A*
        self.direccion = random.choice(['izquierda', 'derecha', 'arriba', 'abajo'])

    def ver_ladron(self, ladron):
        # Determina si el ladrón está en rango de visión
        distancia = ((self.rect.centerx - ladron.rect.centerx) ** 2 + (self.rect.centery - ladron.rect.centery) ** 2) ** 0.5
        return distancia < 200  # Ajusta el rango de visión

    def mover_hacia(self, destino, delta_time):
        # Calcula el movimiento hacia un destino usando A*
        dx, dy = destino[0] - self.rect.centerx, destino[1] - self.rect.centery
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        if distancia > 1:  # Mover solo si hay distancia suficiente
            direccion_x = dx / distancia
            direccion_y = dy / distancia
            self.rect.x += int(direccion_x * self.velocidad * delta_time)
            self.rect.y += int(direccion_y * self.velocidad * delta_time)

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

        if 0 <= x < len(mapa[0]) and 0 <= y < len(mapa) and mapa[y][x] == PASILLO:
            self.rect.x = nueva_pos_x
            self.rect.y = nueva_pos_y
        else:
            self.direccion = random.choice(['izquierda', 'derecha', 'arriba', 'abajo'])  # Cambiar dirección si hay obstáculo

    def update(self, ladron, mapa, celda_ancho, celda_alto, delta_time):
        # Asignar datos necesarios para los comportamientos
        self.ladron = ladron
        self.mapa = mapa
        self.celda_ancho = celda_ancho
        self.celda_alto = celda_alto
        self.delta_time = delta_time

        # Construir el árbol de comportamiento
        arbol_comportamiento = Selector([
            Perseguir(),
            Patrullar(),
            Esperar()
        ])

        # Ejecutar el árbol de comportamiento
        arbol_comportamiento.ejecutar(self)
