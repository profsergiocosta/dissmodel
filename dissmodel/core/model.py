import salabim as sim
from pysal.lib import weights

class Model (sim.Component):


    def __init__(self, hold = 1, name="",  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self._hold = hold

        
    def process(self):
            while True: 
                self.execute() 
                self.hold(self._hold)
    
    

    def __setattr__(self, name, value):
        
        cls = self.__class__

        
        # Verifica se o atributo faz parte dos que devem ser plotados
        if hasattr(cls, "_plot_info") and name.lower() in cls._plot_info:
            plot_info = cls._plot_info[name.lower()]
            plot_info["data"].append(value)


            # Garante que _plot_metadata existe
            if not hasattr(self.env, "_plot_metadata"):
                self.env._plot_metadata = {}

            # Garante que a label está registrada no _plot_metadata
            if plot_info["label"] not in self.env._plot_metadata:
                self.env._plot_metadata[plot_info["label"]] = plot_info

        # Atribui normalmente
        super().__setattr__(name, value)

