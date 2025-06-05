# https://github.com/pysal/libpysal/blob/main/libpysal/weights/contiguity.py



class Neighborhood:
    def __init__(self, strategy, *args, **kwargs):
        self.strategy = strategy
        self.args = args
        self.kwargs = kwargs
        self._build()

    def _build(self):
        self.w_ = self.strategy.from_dataframe(*self.args, **self.kwargs)
        self.df = self._extract_dataframe()

    def _extract_dataframe(self):
        # Procura o GeoDataFrame nos args e kwargs
        for arg in self.args:
            if hasattr(arg, "geometry"):
                return arg
        for value in self.kwargs.values():
            if hasattr(value, "geometry"):
                return value
        raise ValueError("Não foi possível identificar o GeoDataFrame.")

    def neighs(self, idx):
        ns = self.w_.neighbors[idx]
        return self.df.loc[ns]

    def idxs(self, idx):
        return self.w_.neighbors[idx]

    def update(self, strategy, *args, **kwargs):
        self.strategy = strategy
        self.args = args
        self.kwargs = kwargs
        self._build()