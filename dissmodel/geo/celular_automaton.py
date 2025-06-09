
import math
from libpysal.weights import Queen
from dissmodel.core import Model
from dissmodel.geo import attach_neighbors


class CellularAutomaton(Model):
    """
    Classe base para autômatos celulares espaciais baseada em um GeoDataFrame.

    Parâmetros:
    - gdf: GeoDataFrame com geometrias e atributo de estado.
    - state_attr: nome da coluna que representa o estado da célula.
    - step, start_time, end_time, name: parâmetros herdados da classe Model.
    """

    def __init__(self, gdf, state_attr="state", step=1, start_time=0, end_time=math.inf, name="", dim=None, *args, **kwargs):
        self.gdf = gdf
        self.state_attr = state_attr
        self._neighborhood_created = False
        self.dim = dim
        super().__init__(step=step, start_time=start_time, end_time=end_time, name=name, *args, **kwargs)

    def initialize(self):
        """
        Deve ser sobrescrito pelas subclasses.
        """
        pass

    def create_neighborhood(self, strategy=Queen, neighbors_dict=None, *args, **kwargs):
        """
        Cria e anexa a vizinhança no GeoDataFrame.

        Parâmetros:
        - neighborhood_strategy: estratégia de vizinhança (ex: Queen, Rook)
        - neighbors_dict: dicionário ou caminho JSON para vizinhança externa
        - *args, **kwargs: parâmetros extras para a estratégia
        """
        self.gdf = attach_neighbors(
            gdf=self.gdf,
            strategy=strategy,
            neighbors_dict=neighbors_dict,
            *args,
            **kwargs
        )
        self._neighborhood_created = True

    def neighs_id(self, idx):
        """
        Retorna a lista de índices vizinhos da célula `idx`.
        """
        return self.gdf.loc[idx, "_neighs"]

    def neighs(self, idx):
        """
        Retorna as células vizinhas da célula `idx`.

        Lança erro se a vizinhança ainda não foi criada.
        """
        if not self._neighborhood_created:
            raise RuntimeError("Vizinhança ainda não foi criada. Use `.create_neighborhood()` primeiro.")
        if "_neighs" not in self.gdf.columns:
            raise ValueError("A coluna '_neighs' não está presente no GeoDataFrame.")
        return self.gdf.loc[self.neighs_id(idx)]

    def rule(self, idx):
        """
        Deve ser sobrescrito pelas subclasses. Define a regra de transição de estado.
        """
        raise NotImplementedError("A subclasse deve implementar a regra.")

    def execute(self):
        """
        Executa um passo do autômato aplicando a regra a cada célula.
        """
        #if not self._neighborhood_created:
        #    raise RuntimeError("Você deve criar a vizinhança antes de executar o modelo. Use `.create_neighborhood()`.")
        
        self.gdf[self.state_attr] = self.gdf.index.map(self.rule)
        #print(self.env.now())
