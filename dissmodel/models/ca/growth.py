import random
from dissmodel.geo import CellularAutomaton, parse_idx

from libpysal.weights import Queen

class Growth(CellularAutomaton):

    EMPTY = 0
    ALIVE = 1

    probability: float


    def initialize(self):
        # Define célula central como viva no tempo inicial
        center = self.dim // 2
        center_idx = f"{center}-{center}"
        self.gdf.loc[:, "state"] = self.EMPTY
        self.gdf.loc[center_idx, "state"] = self.ALIVE

    def setup(self, probability=0.15):
        self.probability = probability
        self.create_neighborhood(strategy=Queen, use_index=True)

    def rule(self, idx):
        cell = self.gdf.loc[idx]

        # Se já está viva, permanece viva
        if cell.state == self.ALIVE:
            return self.ALIVE

        # Obtém os vizinhos da célula atual
        neighs = self.neighs(idx)

        # Conta quantos vizinhos estão vivos
        alive_neighbors = (neighs[self.state_attr] == self.ALIVE).sum()

        # Se tem pelo menos um vizinho vivo, pode tornar-se vivo
        if alive_neighbors > 0 and random.random() < self.probability:
            return self.ALIVE

        return self.EMPTY
