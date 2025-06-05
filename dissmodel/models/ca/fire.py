

from dissmodel.core import Model

from dissmodel.geo.neihborhood import Neighborhood

# Fire in the forest
# https://github.com/TerraME/terrame/wiki/Paradigms

from libpysal.weights.contiguity import Rook
from libpysal.weights.contiguity import Queen

class FireModel(Model):

    FOREST = 0
    BURNING = 1
    BURNED = 2

    def setup (self,gdf):
         self.gdf = gdf
         self.neighborhood = Neighborhood(Queen, gdf, use_index=True)

    def rule(self, idx):

        state = self.gdf.loc[idx].state
             
        if state == FireModel.BURNING:
            return FireModel.BURNED
        elif state == FireModel.FOREST:
                neighs = self.neighborhood.neighs(idx)

                if (neighs.state == FireModel.BURNING).any():
                     return FireModel.BURNING
                else:
                     return state         
        else:
             return state
        

    def execute(self):
        # Aplicar a função `rule` a todos os índices e armazenar os novos estados
        self.gdf["state"] = self.gdf.index.map(self.rule)