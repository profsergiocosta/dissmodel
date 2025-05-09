import salabim as sim

class Environment(sim.Environment):
    """
    Ambiente de simulação estendido com suporte a tempo inicial customizado
    e integração com dados geográficos (GeoDataFrame).
    """

    def __init__(self, gdf=None, start_time=0, end_time=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = start_time
        self.end_time = end_time
        self.gdf = gdf        

    def run(self, end_time=None):
        """
        Executa a simulação do tempo inicial ao final.
        """
        print(f"Running from {self.start_time} to {self.end_time}")
        if end_time:
            self.end_time = end_time
            super().run(till=end_time - self.start_time)    
        else:
            super().run(till=self.end_time - self.start_time)

    def now(self):
        """
        Retorna o tempo atual da simulação ajustado pelo tempo inicial.
        """
        return super().now() + self.start_time

