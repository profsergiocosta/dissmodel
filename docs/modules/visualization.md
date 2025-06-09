O módulo de visualização é projetado para fornecer representações interativas e atualizáveis de modelos em execução, seja através de gráficos temporais ou mapas geoespaciais. Ele é composto por duas principais classes: `Chart` e `Map`, ambas herdadas de `Model`, o que permite sua integração e controle direto pelo `Environment`.

### Classe `Chart`

A classe `Chart` é responsável por gerar gráficos temporais com dados provenientes da simulação. Os modelos podem ser anotados com o decorador `@track_plot`, que define quais variáveis devem ser rastreadas e visualizadas. A coleta e a atualização dos dados são feitas automaticamente a cada execução da simulação.

**Principais funcionalidades:**

- Integração direta com o `Environment`, executando a plotagem sincronizada com o tempo da simulação.
- Suporte à exibição local (modo interativo com `matplotlib`) e em dashboards (`Streamlit`).
- Visualização seletiva de variáveis via argumento `select`.


Com isso, basta adicionar `@track_plot` acima da definição de uma classe para que as variáveis sejam automaticamente monitoradas.

### Classe `Map`

A classe `Map` permite visualizar dinamicamente a evolução espacial de dados contidos em `GeoDataFrames`. A cada passo da simulação, o mapa é atualizado com base nos parâmetros definidos.

**Principais funcionalidades:**

- Plotagem automática de dados espaciais com `GeoPandas`.
- Integração direta com `Environment`.
- Suporte à exibição via `matplotlib` local ou `Streamlit`.

---


### Decoradores e anotações

Para especificar quais variáveis de um modelo devem ser exibidas no gráfico, utiliza-se o decorador `track_plot`. Esse decorador associa metadados ao modelo, que são lidos pela classe `Chart`.


O método `display_inputs` permite criar dinamicamente interfaces de entrada no Streamlit com base nas anotações de tipo do modelo:


### Exemplo

A seguir, mostramos como utilizar o decorador `@track_plot`, a interface de entrada via `Streamlit`, e a visualização automática com `Chart`.

#### Definição do Modelo SIR

 Importações

```python
from dissmodel.core import Model
from dissmodel.visualization import track_plot
```

- Model: Classe base de modelos no DisSModel. Todos os modelos devem herdar dessa classe.
- track_plot: Um decorador usado para indicar quais atributos devem ser monitorados e plotados ao longo do tempo. Serve para gerar automaticamente gráficos durante a simulação.

📊 Decoradores @track_plot(...)
```python
@track_plot("Susceptible", "green")
@track_plot("Infected", "red")
@track_plot("Recovered", "blue")
class SIR(Model):   

```
Esses decoradores dizem ao DisSModel para:

- Monitorar as variáveis susceptible, infected e recovered.

- Associar cada uma a uma cor no gráfico.

O resultado visual será um gráfico que mostra a evolução do número de pessoas em cada estado da epidemia ao longo do tempo.


Também será definido na classe os atributos serão utilizados pela funcão display_inputs.



```python
    susceptible: int
    infected: int
    recovered: int
    duration: int
```

Esses são atributos do modelo:
- susceptible: número de pessoas suscetíveis.
- infected: número de pessoas infectadas.
- recovered: número de pessoas recuperadas.
- duration: tempo médio que uma pessoa permanece infectada.

O comportamento deste modelo foi descrito no modulo core. Mas a seguir tem o exemplo com os elementos que serão utilizados a entrada de parâmetros pelo streamlit, e visualização do mapa. 

```python
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

#### Visualização com Streamlit




1. 📦 Importações
```python
import streamlit as st
from dissmodel.core import Environment
from dissmodel.visualization import Chart, display_inputs
from models import SIR
```

    - streamlit as st: biblioteca usada para construir interfaces web interativas com Python.
    - Environment: classe do DisSModel que gerencia o tempo da simulação.
    - Chart: componente que exibe os gráficos com base no @track_plot usado no modelo.
    - display_inputs: função que gera automáticamente sliders e campos no sidebar com base nos parâmetros do modelo (__init__).
    - SIR: o modelo de simulação definido anteriormente.

2. ⚙️ Configuração da Página

    ```python
    st.set_page_config(page_title="SIR Model", layout="centered")
    st.title("SIR Model (DisSModel)")
    ```

    Define o título da aba do navegador e o layout. Exibe o título da aplicação na interface.

3. 🎛️ Sidebar com Parâmetros
```python
st.sidebar.title("Parâmetros do Modelo")
steps = st.sidebar.slider("Número de passos da simulação", min_value=1, max_value=50, value=10)
executar = st.button("Executar Simulação")
```

    Cria um título na barra lateral. Um slider que permite ao usuário ajustar o número de passos da simulação. Um botão chamado "Executar Simulação", que inicia a execução quando clicado.

4. 🌍 Criação do Ambiente de Simulação

    ```python
    env = Environment(end_time=steps, start_time=0)
    Cria um ambiente temporal onde o modelo será executado.
    ```

    Define o tempo inicial (start_time=0) e final (end_time=steps) com base no valor do slider.

5. 🧪 Instanciação do Modelo e Inputs
    ```python
    sir = SIR()
    display_inputs(sir, st.sidebar)
    ```
    Cria uma instância do modelo SIR com os valores padrão. E display_inputs(...) gera campos automáticos na barra lateral com os parâmetros do modelo, como: contacts, probability, duration, infected, susceptible, etc.

    Isso elimina a necessidade de escrever manualmente todos os sliders.

6. 📈 Gráfico de Acompanhamento
```python
Chart(plot_area=st.empty())
```

    Cria um espaço vazio onde o gráfico da simulação será exibido.

    O gráfico mostra as variáveis com @track_plot, ou seja: susceptible, infected e recovered.

7. ▶️ Execução da Simulação
```python
if executar:
    env.reset()
    env.run()
```
    Quando o botão "Executar Simulação" for clicado:
    - env.reset(): reseta o tempo e os estados internos do ambiente.
    - env.run(): executa a simulação passo a passo, chamando o método execute() do modelo a cada passo.

    O gráfico será atualizado automaticamente com os dados do @track_plot.




O codigo completo
```python
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
