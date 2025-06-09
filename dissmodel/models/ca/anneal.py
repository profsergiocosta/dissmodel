import random
from dissmodel.geo import CellularAutomaton
from libpysal.weights import Queen

class Anneal(CellularAutomaton):
    L = 0
    R = 1

    def initialize(self):
        self.gdf["state"] = [random.choice([self.L, self.R]) for _ in range(len(self.gdf))]
        
    def setup(self):
        # Inicializa estados aleatórios: 0 (L) ou 1 (R)
        self.create_neighborhood(strategy=Queen, use_index=True)

    def rule(self, idx):
        cell = self.gdf.loc[idx]
        neighbors = self.neighs(idx)

        # Conta vizinhos com estado L (0)
        alive = (neighbors[self.state_attr] == self.L).sum()

        # Adiciona a célula atual à contagem se for L
        if cell.state == self.L:
            alive += 1

        # Aplica regras de transição
        if alive <= 3:
            return self.R
        elif alive >= 6:
            return self.L
        elif alive == 4:
            return self.L
        elif alive == 5:
            return self.R

        # Fallback (não deve ser necessário)
        return cell.state
