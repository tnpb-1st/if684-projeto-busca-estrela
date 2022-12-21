from math import pow, sqrt, abs
from collections import deque

_hash = {} # dicionario que irá mapear nome da cidade -> suas coordenadas
class Ponto:
    _x, _y, _z = 0.0 # coordenadas do nó
    def __init__(self, cord_x=0.0, cord_y=0.0, cord_z=0.0):
        self._x, self._y, self._z = cord_x, cord_y, cord_z
    def dist_euclidiana(self, ponto) -> float:
        return sqrt((pow(self._x - ponto._x) ,2) + pow((self._y - ponto._y) ,2) + pow((self._z - ponto._z) ,2))
    def dist_euclidiana(self, cord_x, cord_y, cord_z) -> float:
        return sqrt((pow(self._x - cord_x) ,2) + pow((self._y - cord_y) ,2) + pow((self._z - cord_z) ,2))
    def dist_manhattan(self, ponto) -> float:
        return abs(self._x - ponto._x) + abs(self._y - ponto._y) + abs(self._zs - ponto._z)
    def dist_manhattan(self, cord_x, cord_y, cord_z) -> float:
        return abs(self._x - cord_x) + abs(self._y - cord_y) + abs(self._zs - cord_z)

class Grafo:
    arestas = {}
    def inserir_aresta(self, v1, v2):
        if(not(v1 in self.nos)):
            self.arestas[v1] = []
        if(not(v2 in self.nos)):
            self.arestas[v2] = []
        self.arestas[v1].append(v2)
        self.arestas[v2].append(v1)
    def dfs(self,raiz) -> list(str):
        """retorna uma lista com os nos visitados a partir da raiz"""
        pilha = deque()
        pilha.appendleft(raiz)
        visitados = {raiz}
        while(pilha.count() > 0):
            v = pilha.popleft()
            for adj in self.arestas[v]:
                if(not(adj in visitados)):
                    visitados.add(adj)
                    pilha.appendleft(adj)
        return list(visitados)
    def bfs(self, raiz) -> list(tuple(int, str)):
        """retorna uma lista de tuplas em que o primeiro elemento é a ordem em que o no foi visitado a partir da raiz e
        o nome do no"""
        fila = deque()
        fila.append(raiz)
        visitados = {raiz}
        visitados_retorno = []
        cont = 0
        while(fila.count() > 0):
            v = fila.pop()
            for adj in self.arestas[v]:
                if(not(adj in visitados)):
                    visitados.add(adj)
                    fila.append(adj)
                    visitados_retorno.append((cont, adj))
                    cont += 1
        return visitados_retorno