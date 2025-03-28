import heapq
from mapa import PASILLO  # Asegurarse de importar PASILLO

def a_star(inicio, meta, mapa, celda_ancho, celda_alto):
    lista_abierta = []
    heapq.heappush(lista_abierta, (0, inicio))
    de_donde_vengo = {}
    puntaje_g = {inicio: 0}
    puntaje_f = {inicio: heuristica(inicio, meta)}

    while lista_abierta:
        _, actual = heapq.heappop(lista_abierta)
        
        if actual == meta:
            return reconstruir_camino(de_donde_vengo, actual)
        
        for vecino in obtener_vecinos(actual, mapa, celda_ancho, celda_alto):
            g_score_tentativo = puntaje_g[actual] + dist_entre(actual, vecino)
            if g_score_tentativo < puntaje_g.get(vecino, float('inf')):
                de_donde_vengo[vecino] = actual
                puntaje_g[vecino] = g_score_tentativo
                puntaje_f[vecino] = puntaje_g[vecino] + heuristica(vecino, meta)
                heapq.heappush(lista_abierta, (puntaje_f[vecino], vecino))
                
    return []

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def obtener_vecinos(nodo, mapa, celda_ancho, celda_alto):
    vecinos = []
    x, y = nodo
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimientos en celdas (arriba, abajo, izquierda, derecha)
    for dx, dy in movimientos:
        vecino = (x + dx, y + dy)
        if 0 <= vecino[0] < len(mapa[0]) and 0 <= vecino[1] < len(mapa):  # Dentro de los límites
            if mapa[vecino[1]][vecino[0]] == PASILLO:  # Solo agregar pasillos
                vecinos.append(vecino)
    return vecinos


def dist_entre(a, b):
    return 1

def reconstruir_camino(de_donde_vengo, actual):
    camino = [actual]
    while actual in de_donde_vengo:
        actual = de_donde_vengo[actual]
        camino.append(actual)
    return camino[::-1]
