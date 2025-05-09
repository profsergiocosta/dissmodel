

from dissmodel.visualization import Map, Chart



def display_inputs(obj, st):
    annotations = getattr(obj, '__annotations__', {})

    for name, type_ in annotations.items():
        value = getattr(obj, name, None)

        if isinstance(value, int):
            new_value = st.slider(name, 0, 100, value)
        elif isinstance(value, float):
            new_value = st.slider(name, 0.0, 1.0, value, step=0.01)
        elif isinstance(value, bool):
            new_value = st.checkbox(name, value=value)
        else:
            new_value = st.text_input(name, str(value))

        setattr(obj, name, new_value)


class StreamlitMap(Map):
    def setup(self, plot_params, plot_area=None):
        # Chama o setup da classe mãe para criar fig e ax
        super().setup(plot_params, pause=False)
        
        # Adiciona atributos específicos para Streamlit
        self.plot_area = plot_area

    def execute(self):
        # Usa o método da superclasse para atualizar a figura
        super().execute()
        
        # Depois disso, mostra a figura no Streamlit
        if self.plot_area:
            self.plot_area.pyplot(self.fig)
        

class StreamlitInputMixin:
    def display_inputs(self):
        # Pega a assinatura do __init__ da classe
        sig = inspect.signature(self.__init__)
        # Pega apenas os nomes dos parâmetros definidos no __init__, ignorando 'self'
        init_params = [p.name for p in sig.parameters.values() if p.name != 'self']

        for param in init_params:
            value = getattr(self, param, None)
            if isinstance(value, int):
                setattr(self, param, st.slider(param, min_value=0, max_value=10000, value=value))
            elif isinstance(value, float):
                setattr(self, param, st.slider(param, min_value=0.0, max_value=1.0, value=value, step=0.01))
            else:
                setattr(self, param, st.text_input(param, str(value)))

### isso ficaria no modul de visualizacao
class StreamlitChart (Chart):
    def setup(self, plot_area=None):
        # Chama o setup da classe mãe para criar fig e ax
        super().setup(pause=False)
        
        # Adiciona atributos específicos para Streamlit
        self.plot_area = plot_area

    def execute(self):
        # Usa o método da superclasse para atualizar a figura
        super().execute()

        
        # Depois disso, mostra a figura no Streamlit
        if self.plot_area:
            self.plot_area.pyplot(self.fig)
        



