# Modelo FireModel baseado em dissmodel.CellularAutomaton

from dissmodel.geo import CellularAutomaton
from libpysal.weights import Rook


from dissmodel.geo import regular_grid, fill, FillStrategy


class FireModel(CellularAutomaton):
    # Estados possíveis
    FOREST = 0
    BURNING = 1
    BURNED = 2

    def initialize(self):
        fill(
            strategy=FillStrategy.RANDOM_SAMPLE,
            gdf=self.gdf,
            attr="state",
            data={FireModel.FOREST: 0.95, FireModel.BURNING: 0.05},  # 70% de células com 0, 30% com 1
            seed=42
        )

    def setup(self):
        """
        Cria a vizinhança com a estratégia Rook.
        """
        self.create_neighborhood(strategy=Rook, use_index=True)
        self.initialize()

    def rule(self, idx):
        """
        Define as regras de transição de estados para o modelo de incêndio florestal.
        """
        state = self.gdf.loc[idx, self.state_attr]

        if state == FireModel.BURNING:
            return FireModel.BURNED

        elif state == FireModel.FOREST:
            neighs = self.neighs(idx)
            if (neighs[self.state_attr] == FireModel.BURNING).any():
                return FireModel.BURNING
            else:
                return state
        
        else:
            return state
