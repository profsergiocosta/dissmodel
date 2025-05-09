
from dissmodel.core import Model

import random


FOREST = 0
BURNING = 1
BURNED = 2

# Fire in the forest
# https://github.com/TerraME/terrame/wiki/Paradigms


class FireModel(Model):

    def rule(self, idx):

        state = self.env.gdf.loc[idx].state
             
        if state == BURNING:
            return BURNED
        elif state == FOREST:
                #neighs = self.env.gdf.loc[self.neighs(idx)]
                neighs = self.neighs(idx)

                if (neighs.state == BURNING).any():
                     return BURNING
                else:
                     return state         
        else:
             return state
        

    def execute(self):
        # Aplicar a função `rule` a todos os índices e armazenar os novos estados
        self.env.gdf["state"] = self.env.gdf.index.map(self.rule)


# Fire in the forest
# https://github.com/cesaraustralia/DynamicGrids.jl

prob_combustion=0.001
prob_regrowth=0.1

class FireModelProb(Model):

    def rule(self, idx):
        state = self.env.gdf.loc[idx].state
        
        if state == FOREST:
            neighs = self.neighs(idx)

            if (neighs.state == BURNING).any():
                return BURNING
            else:
                return BURNING if random.random() <= prob_combustion else FOREST

        elif state == BURNING:
            return BURNED
           
        else:
             return FOREST if random.random() <= prob_regrowth else BURNED
        

    def execute (self):
        self.env.gdf["state"] = self.env.gdf.index.map(self.rule)

