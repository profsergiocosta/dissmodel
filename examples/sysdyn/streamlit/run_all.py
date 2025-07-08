import streamlit as st
import inspect

from dissmodel.core import Environment
from dissmodel.visualization import Chart, display_inputs

# Configurações iniciais da página
st.set_page_config(page_title="Modelos SysDyn", layout="centered")
st.title("Modelos do DisSModel (SysDyn)")



import dissmodel.models.sysdyn as sysdyn_models  # Substitua pelo seu módulo real

# Obter todas as classes definidas em dissmodel.models.sysdyn
model_classes = {
    name: cls
    for name, cls in inspect.getmembers(sysdyn_models, inspect.isclass)
}


# Seleciona a classe do modelo
model_name = st.sidebar.selectbox("Escolha o modelo", options=list(model_classes.keys()))

# Entrada para o número de passos da simulação
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=1000, value=10)

# Botão para executar a simulação
executar = st.button("Executar Simulação")

# Criação do ambiente de simulação
env = Environment(end_time=steps, start_time=0)

# Instanciação dinâmica do modelo
ModelClass = model_classes[model_name]
model_instance = ModelClass()

# Exibe os campos para entrada de dados do modelo
st.sidebar.subheader("Parâmetros do Modelo")
display_inputs(model_instance, st.sidebar)

# Área para o gráfico
Chart(plot_area=st.empty(), show_grid=True)

# Executa simulação
if executar:
    #env.add(model_instance)
    env.run()
