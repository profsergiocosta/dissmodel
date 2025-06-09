from dissmodel.core import Model

from libpysal.weights import KNN
import numpy as np

import random
from dissmodel.geo import regular_grid, fill, FillStrategy

from dissmodel.geo import CellularAutomaton

class Propagation(CellularAutomaton):


    prob: float
    perc_on: float

    def initialize(self):
        fill(
            strategy=FillStrategy.RANDOM_SAMPLE,
            gdf=self.gdf,
            attr="state",
            data={0: (1-self.perc_on), 1: self.perc_on}, 
            #data={0: 1, 1: 0}, 
            seed=42
        )

    def setup(self, prob=0.1, perc_on=0.4):
        self.prob = prob
        self.perc_on = perc_on

        self.create_neighborhood(strategy=KNN,k=4, use_index=True)
        self.initialize()

    def rule(self, idx):
        estado_atual = self.gdf.loc[idx, self.state_attr]

        if estado_atual == 1:
            return 1

        vizinhos = self.neighs_id(idx)
        if any(self.gdf.loc[v, self.state_attr] == 1 for v in vizinhos):
            if np.random.rand() < self.prob:
                return 1
        return estado_atual


