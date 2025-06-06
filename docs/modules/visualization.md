O módulo de visualização é projetado para fornecer representações interativas e atualizáveis de modelos em execução, seja através de gráficos temporais ou mapas geoespaciais. Ele é composto por duas principais classes: `Chart` e `Map`, ambas herdadas de `Model`, o que permite sua integração e controle direto pelo `Environment`.

### Classe `Chart`

A classe `Chart` é responsável por gerar gráficos temporais com dados provenientes da simulação. Os modelos podem ser anotados com o decorador `@track_plot`, que define quais variáveis devem ser rastreadas e visualizadas. A coleta e a atualização dos dados são feitas automaticamente a cada execução da simulação.

**Principais funcionalidades:**

- Integração direta com o `Environment`, executando a plotagem sincronizada com o tempo da simulação.
- Suporte à exibição local (modo interativo com `matplotlib`) e em dashboards (`Streamlit`).
- Visualização seletiva de variáveis via argumento `select`.

### Decorador `@track_plot`

Para especificar quais variáveis de um modelo devem ser exibidas no gráfico, utiliza-se o decorador `track_plot`. Esse decorador associa metadados ao modelo, que são lidos pela classe `Chart`.


Com isso, basta adicionar `@track_plot` acima da definição de uma classe para que as variáveis sejam automaticamente monitoradas.

### Classe `Map`

A classe `Map` permite visualizar dinamicamente a evolução espacial de dados contidos em `GeoDataFrames`. A cada passo da simulação, o mapa é atualizado com base nos parâmetros definidos.

**Principais funcionalidades:**

- Plotagem automática de dados espaciais com `GeoPandas`.
- Integração direta com `Environment`.
- Suporte à exibição via `matplotlib` local ou `Streamlit`.

---


### Geração Dinâmica de Inputs

O método `display_inputs` permite criar dinamicamente interfaces de entrada no Streamlit com base nas anotações de tipo do modelo:


### Exemplo Integrado: Modelo SIR com Visualização

A seguir, mostramos como utilizar o decorador `@track_plot`, a interface de entrada via `Streamlit`, e a visualização automática com `Chart`.

### Definição do Modelo SIR

```python
python
CopyEdit
from dissmodel.core import Model
from dissmodel.visualization import track_plot

@track_plot("Susceptible", "green")
@track_plot("Infected", "red")
@track_plot("Recovered", "blue")
class SIR(Model):
    susceptible: int
    infected: int
    recovered: int
    duration: int

    def __init__(self, susceptible=9998, infected=2, recovered=0, duration=2,
                 contacts=6, probability=0.25, final_time=30):
        super().__init__()
        self.susceptible = susceptible
        self.infected = infected
        self.recovered = recovered
        self.duration = duration
        self.contacts = contacts
        self.probability = probability
        self.final_time = final_time

    def update(self):
        total = self.susceptible + self.infected + self.recovered
        alpha = self.contacts * self.probability
        prop = self.susceptible / total
        new_infected = self.infected * alpha * prop
        new_recovered = self.infected / self.duration
        self.susceptible -= new_infected
        self.infected += new_infected - new_recovered
        self.recovered += new_recovered

    def execute(self):
        self.update()

```

### Visualização com Streamlit

```python
python
CopyEdit
import streamlit as st
from dissmodel.core import Environment
from dissmodel.visualization import Chart, display_inputs
from models import SIR

st.set_page_config(page_title="SIR Model", layout="centered")
st.title("SIR Model (DisSModel)")

st.sidebar.title("Parâmetros do Modelo")
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
executar = st.button("Executar Simulação")

# Ambiente de simulação
env = Environment(end_time=steps, start_time=0)

# Instanciação do modelo com valores padrão
sir = SIR()
display_inputs(sir, st.sidebar)  # Interface automática

# Componente gráfico
Chart(plot_area=st.empty())

# Execução da simulação
if executar:
    env.reset()
    env.run()

```

---

Esse exemplo demonstra como a modelagem orientada a objetos, combinada com visualização interativa e a arquitetura baseada em ambiente, permite a construção de simulações ricas, parametrizáveis e altamente visuais — tudo isso com código limpo e extensível.