

import random
from dissmodel.core import Model


# Fire in the forest
# https://github.com/cesaraustralia/DynamicGrids.jl

class FireModelProb(Model):

    FOREST = 0
    BURNING = 1
    BURNED = 2

    prob_regrowth: float
    prob_combustion: float

    def __init__(self, prob_combustion=0.001,  prob_regrowth=0.1, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.prob_combustion = prob_combustion
        self.prob_regrowth = prob_regrowth

    def rule(self, idx):
        state = self.env.gdf.loc[idx].state
        
        if state == FireModelProb.FOREST:
            neighs = self.neighs(idx)

            if (neighs.state == FireModelProb.BURNING).any():
                return FireModelProb.BURNING
            else:
                return FireModelProb.BURNING if random.random() <= self.prob_combustion else FireModelProb.FOREST

        elif state == FireModelProb.BURNING:
            return FireModelProb.BURNED
           
        else:
             return FireModelProb.FOREST if random.random() <= self.prob_regrowth else FireModelProb.BURNED
        

    def execute (self):
        self.env.gdf["state"] = self.env.gdf.index.map(self.rule)


