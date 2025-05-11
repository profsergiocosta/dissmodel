

from dissmodel.core import Model

# Fire in the forest
# https://github.com/TerraME/terrame/wiki/Paradigms



class FireModel(Model):

    FOREST = 0
    BURNING = 1
    BURNED = 2


    def rule(self, idx):

        state = self.env.gdf.loc[idx].state
             
        if state == FireModel.BURNING:
            return FireModel.BURNED
        elif state == FireModel.FOREST:
                #neighs = self.env.gdf.loc[self.neighs(idx)]
                neighs = self.neighs(idx)

                if (neighs.state == FireModel.BURNING).any():
                     return FireModel.BURNING
                else:
                     return state         
        else:
             return state
        

    def execute(self):
        # Aplicar a função `rule` a todos os índices e armazenar os novos estados
        self.env.gdf["state"] = self.env.gdf.index.map(self.rule)