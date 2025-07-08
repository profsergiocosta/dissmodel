import random
from dissmodel.geo import CellularAutomaton, parse_idx
from libpysal.weights import lat2W  # Von Neumann neighborhood

class Snow(CellularAutomaton):
    EMPTY = 0
    SNOW = 1

    probability: float


    def setup(self,  probability=0.02):   

        self.probability = probability
    
    def rule(self, idx):
        cell = self.gdf.loc[idx]
        x, y = parse_idx(idx)
        t = self.env.now()

        # Célula no TOPO: início da queda
        if y == self.dim - 1:
            if cell.state == self.EMPTY and t < (self.end_time - self.dim) and random.random() < self.probability:
                return self.SNOW
            return self.EMPTY

        # Célula abaixo (para verificar se a neve pode descer)
        below_idx = f"{y - 1}-{x}" if y - 1 >= 0 else None
        if cell.state == self.SNOW and y == 0:
            return self.SNOW 
        elif cell.state == self.SNOW and below_idx:
            below_state = self.gdf.loc[below_idx, "state"]
            if below_state == self.EMPTY:
                return self.EMPTY  # A neve "desce", célula atual fica vazia
            else:
                return self.SNOW  # Há neve abaixo, então acumula

        # Célula acima (a neve pode chegar nela)
        above_idx = f"{y + 1}-{x}" if y + 1 < self.dim else None
        if above_idx and self.gdf.loc[above_idx, "state"] == self.SNOW:
            return self.SNOW

        return self.EMPTY


