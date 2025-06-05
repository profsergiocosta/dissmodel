import json
from pathlib import Path
from libpysal.weights import W

class Neighborhood:
    def __init__(self, strategy=None, *args, neighbors_dict=None, **kwargs):
        """
        strategy: ex: Queen, Rook (libpysal)
        neighbors_dict: dicionário de vizinhos ou caminho para JSON
        *args e **kwargs: argumentos passados para from_dataframe
        """
        self.strategy = strategy
        self.args = args
        self.kwargs = kwargs
        self.neighbors_dict = self._load_neighbors(neighbors_dict)
        self._build()

    def _load_neighbors(self, neighbors_dict):
        # Se for string e arquivo existe, tenta carregar JSON
        if isinstance(neighbors_dict, str) and Path(neighbors_dict).is_file():
            with open(neighbors_dict) as f:
                return json.load(f)
        # Se já for um dicionário, retorna direto
        elif isinstance(neighbors_dict, dict):
            return neighbors_dict
        elif neighbors_dict is None:
            return None
        else:
            raise ValueError("`neighbors_dict` deve ser um dicionário ou caminho para um arquivo JSON.")

    def _build(self):
        if self.neighbors_dict is not None:
            self.w_ = W(self.neighbors_dict)
            self.df = self._extract_dataframe()
        else:
            if self.strategy is None:
                raise ValueError("Informe uma strategy ou neighbors_dict.")
            self.w_ = self.strategy.from_dataframe(*self.args, **self.kwargs)
            self.df = self._extract_dataframe()

    def _extract_dataframe(self):
        for arg in self.args:
            if hasattr(arg, "geometry"):
                return arg
        for value in self.kwargs.values():
            if hasattr(value, "geometry"):
                return value
        raise ValueError("Não foi possível identificar o GeoDataFrame.")

    def neighs(self, idx):
        ns = self.w_.neighbors.get(idx, [])
        return self.df.loc[ns]

    def idxs(self, idx):
        return self.w_.neighbors.get(idx, [])

    def update(self, strategy=None, *args, neighbors_dict=None, **kwargs):
        self.strategy = strategy
        self.args = args
        self.kwargs = kwargs
        self.neighbors_dict = self._load_neighbors(neighbors_dict)
        self._build()
