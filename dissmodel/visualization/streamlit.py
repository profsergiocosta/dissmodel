

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
        






