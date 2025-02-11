import pygame
import heapq
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
ANCHO_PANTALLA, ALTO_PANTALLA = 800, 600
ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Ladrón en el Supermercado")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)    # Ladrón
ROJO = (255, 0, 0)     # Guardias
AMARILLO = (255, 255, 0)  # Botines
AZUL = (0, 0, 255)     # Paredes

# Tamaño de celdas (para una cuadrícula)
TAM_CELDA = 20
COLUMNAS = ANCHO_PANTALLA // TAM_CELDA
FILAS = ALTO_PANTALLA // TAM_CELDA

# Clase Nodo para el algoritmo A*
class Nodo:
    def __init__(self, x, y, caminable=True):
        self.x = x
        self.y = y
        self.caminable = caminable
        self.padre = None
        self.g = 0  # Coste desde el inicio
        self.h = 0  # Heurística (distancia estimada al final)
        self.f = 0  # Coste total

    def __lt__(self, otro):
        return self.f < otro.f

# Función para crear el mapa del supermercado
def crear_mapa():
    mapa = [[Nodo(x, y) for y in range(FILAS)] for x in range(COLUMNAS)]
    # Crear pasillos horizontales y verticales
    for x in range(COLUMNAS):
        for y in range(FILAS):
            if x % 2 == 0 or y % 2 == 0:
                mapa[x][y].caminable = False  # Pared
    return mapa

# Función para obtener vecinos de un nodo
def obtener_vecinos(nodo, mapa):
    vecinos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in direcciones:
        x2, y2 = nodo.x + dx, nodo.y + dy
        if 0 <= x2 < COLUMNAS and 0 <= y2 < FILAS:
            if mapa[x2][y2].caminable:
                vecinos.append(mapa[x2][y2])
    return vecinos

# Heurística para el algoritmo A* (Distancia Manhattan)
def heuristica(nodo1, nodo2):
    return abs(nodo1.x - nodo2.x) + abs(nodo1.y - nodo2.y)

# Algoritmo A*
def a_estrella(mapa, inicio, fin):
    abierto = []
    cerrado = set()
    heapq.heappush(abierto, inicio)

    while abierto:
        actual = heapq.heappop(abierto)
        cerrado.add((actual.x, actual.y))

        if actual == fin:
            camino = []
            while actual.padre:
                camino.append(actual)
                actual = actual.padre
            camino.reverse()
            return camino

        for vecino in obtener_vecinos(actual, mapa):
            if (vecino.x, vecino.y) in cerrado:
                continue

            tentativo_g = actual.g + 1

            if tentativo_g < vecino.g or vecino not in abierto:
                vecino.g = tentativo_g
                vecino.h = heuristica(vecino, fin)
                vecino.f = vecino.g + vecino.h
                vecino.padre = actual

                if vecino not in abierto:
                    heapq.heappush(obierto, vecino)

    return None  # No se encontró camino

# Clase base para personajes
class Personaje:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(self.x * TAM_CELDA, self.y * TAM_CELDA, TAM_CELDA, TAM_CELDA)

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

# Clase Ladrón (controlado por el jugador)
class Ladron(Personaje):
    def mover(self, mapa):
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0
        if teclas[pygame.K_LEFT]:
            dx = -1
        if teclas[pygame.K_RIGHT]:
            dx = 1
        if teclas[pygame.K_UP]:
            dy = -1
        if teclas[pygame.K_DOWN]:
            dy = 1

        nueva_x = self.x + dx
        nueva_y = self.y + dy

        # Verificar límites y paredes
        if 0 <= nueva_x < COLUMNAS and 0 <= nueva_y < FILAS:
            if mapa[nueva_x][nueva_y].caminable:
                self.x = nueva_x
                self.y = nueva_y
                self.actualizar_rect()

    def actualizar_rect(self):
        self.rect.topleft = (self.x * TAM_CELDA, self.y * TAM_CELDA)

# Clase Guardia (con árbol de comportamiento y algoritmo A*)
class Guardia(Personaje):
    def __init__(self, x, y, color, mapa):
        super().__init__(x, y, color)
        self.mapa = mapa
        self.objetivo = None
        self.camino = []

    def actualizar(self, ladron):
        if self.ver_ladron(ladron):
            self.perseguir(ladron)
        else:
            self.patrullar()

    # Árbol de comportamiento
    def ver_ladron(self, ladron):
        # Si el ladrón está a cierta distancia (linea de visión simplificada)
        distancia = heuristica(self.mapa[self.x][self.y], self.mapa[ladron.x][ladron.y])
        return distancia < 10

    def perseguir(self, ladron):
        # Usar A* para mover hacia el ladrón
        inicio = self.mapa[self.x][self.y]
        fin = self.mapa[ladron.x][ladron.y]
        self.camino = a_estrella(self.mapa, inicio, fin)
        if self.camino and len(self.camino) > 0:
            siguiente = self.camino.pop(0)
            self.x = siguiente.x
            self.y = siguiente.y
            self.actualizar_rect()
        else:
            # Si no hay camino, se queda quieto
            pass

    def patrullar(self):
        # Movimiento de patrulla simple (al azar)
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nueva_x = self.x + dx
            nueva_y = self.y + dy
            if 0 <= nueva_x < COLUMNAS and 0 <= nueva_y < FILAS:
                if self.mapa[nueva_x][nueva_y].caminable:
                    self.x = nueva_x
                    self.y = nueva_y
                    self.actualizar_rect()
                    break  # Moverse solo una casilla
        # Si no puede moverse, se queda en su lugar

    def actualizar_rect(self):
        self.rect.topleft = (self.x * TAM_CELDA, self.y * TAM_CELDA)

# Clase Botín
class Botin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x * TAM_CELDA + TAM_CELDA//4, self.y * TAM_CELDA + TAM_CELDA//4, TAM_CELDA//2, TAM_CELDA//2)

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, AMARILLO, self.rect)

# Función para dibujar el mapa
def dibujar_mapa(superficie, mapa):
    for x in range(COLUMNAS):
        for y in range(FILAS):
            color = BLANCO if mapa[x][y].caminable else AZUL
            rect = pygame.Rect(x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA)
            pygame.draw.rect(superficie, color, rect)

# Función principal del juego
def juego():
    reloj = pygame.time.Clock()
    mapa = crear_mapa()

    # Instanciar personajes y botines
    ladron = Ladron(1, 1, VERDE)
    guardias = [Guardia(random.randint(0, COLUMNAS-1), random.randint(0, FILAS-1), ROJO, mapa) for _ in range(2)]
    botines = []
    for _ in range(5):
        while True:
            x, y = random.randint(0, COLUMNAS-1), random.randint(0, FILAS-1)
            if mapa[x][y].caminable and (x, y) != (ladron.x, ladron.y):
                botines.append(Botin(x, y))
                break

    # Bucle principal
    jugando = True
    while jugando:
        reloj.tick(10)  # 10 FPS

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        # Actualizar ladrón
        ladron.mover(mapa)

        # Verificar recolección de botines
        for botin in botines[:]:
            if ladron.rect.colliderect(botin.rect):
                botines.remove(botin)

        # Actualizar guardias
        for guardia in guardias:
            guardia.actualizar(ladron)
            # Verificar colisión con el ladrón
            if guardia.rect.colliderect(ladron.rect):
                print("¡Has sido atrapado!")
                jugando = False

        # Verificar si se han recolectado todos los botines
        if not botines:
            print("¡Has recolectado todos los botines y escapado!")
            jugando = False

        # Dibujar todo
        dibujar_mapa(ventana, mapa)
        for botin in botines:
            botin.dibujar(ventana)
        ladron.dibujar(ventana)
        for guardia in guardias:
            guardia.dibujar(ventana)
        pygame.display.flip()

    pygame.quit()

# Ejecutar el juego
juego()
