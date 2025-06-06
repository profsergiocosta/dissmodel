## Módulo Core

### Overview

O **Módulo Core** se baseia na poderosa biblioteca **Salabim**, que permite a construção de simulações discretas e o controle de eventos no tempo. O módulo é composto por duas classes principais: **Environment** e **Model**. Ambas são extensões das classes fornecidas pelo **Salabim**, mas com melhorias que oferecem um controle mais preciso sobre o tempo de simulação, além de permitir a coleta de dados para visualização durante a execução do modelo.

---

### Classe `Environment`

A classe **Environment** é uma extensão da classe `sim.Environment` do **Salabim**, que foi customizada para permitir a definição de um **tempo inicial e tempo final** de simulação, oferecendo maior flexibilidade no controle da execução.

### Funcionalidades

- **Tempo Inicial e Final Personalizados**: A classe permite a definição de um `start_time` e `end_time` personalizados para a simulação, proporcionando um controle mais preciso sobre os períodos em que a simulação deve ocorrer.
- **Execução da Simulação**: O método `run` da classe é responsável por rodar a simulação, respeitando os tempos de início e fim definidos. Se um tempo `till` for fornecido, ele substituirá o `end_time`, permitindo maior flexibilidade durante a execução.
- **Reset de Estatísticas**: O método `reset` é responsável por limpar os dados de visualização, caso existam, e reiniciar os componentes de estatísticas ou gráficos. Isso é útil quando se deseja reiniciar uma simulação com dados limpos.

### Classe `Model`

A classe **Model** é uma extensão da classe `sim.Component` do **Salabim**, com melhorias no controle de tempo de execução e no armazenamento de dados para visualizações gráficas.

### Funcionalidades

- **Controle de Tempo Personalizado**: Assim como na classe `Environment`, a classe **Model** permite que a simulação seja controlada por **tempo de início** e **tempo de término** definidos pelo usuário.
- **Execução do Processo**: O método `process` controla o ciclo de vida do modelo, aguardando até o **tempo de início** e realizando a execução até o **tempo de término**. O processo pode ser dividido em etapas (passos), com o tempo de espera entre essas etapas configurado pelo usuário.
- **Armazenamento de Dados para Visualização**: Ao definir atributos que devem ser plotados, a classe garante que esses dados sejam coletados e armazenados em um dicionário de metadados. Essa funcionalidade facilita a criação de gráficos durante a execução do modelo.

### Como Utilizar

- **Instanciação do Ambiente**: O usuário pode criar uma instância do ambiente com um tempo de início e fim definidos.
    
    ```python
    env = Environment(start_time=10, end_time=50)
    
    ```
    
- **Criação de Modelos**: Os modelos podem ser instanciados com tempos de início e fim específicos, além de definir o intervalo entre os passos.
    
    ```python
    model = Model(start_time=10, end_time=40, step=2, name="Modelo de Transporte")
    model.process()
    
    ```
    
- **Execução da Simulação**: Para rodar a simulação com os tempos definidos, o método `run` do ambiente deve ser chamado.
    
    ```python
    env.run()
    
    ```
    

---

Essas duas classes proporcionam um controle mais fino sobre os tempos de execução e permitem coletar dados automaticamente para visualização, o que facilita a análise dos resultados. Elas são fundamentais para construir modelos discretos mais dinâmicos e personalizados.

### Exemplos de Execução no Módulo Core

O controle de tempo no **Módulo Core** é um dos aspectos mais poderosos da ferramenta. A seguir, apresentamos um exemplo prático que demonstra como diferentes modelos podem ser executados em um ambiente de simulação com tempos de início e fim específicos, permitindo a execução paralela ou sequencial.

### Exemplo de Simulação com Vários Modelos

Vamos ilustrar como três modelos (`ModeloA`, `ModeloB` e `ModeloC`) podem ser configurados para executar em diferentes intervalos de tempo dentro de um ambiente de simulação. O exemplo abaixo utiliza as classes **Environment** e **Model** do módulo **Core**.

```python

from dissmodel.core import Model, Environment

class ModeloA(Model):
    def execute(self):
        print(f"[A] Tempo: {self.env.now()}")

class ModeloB(Model):
    def execute(self):
        print(f"[B] Tempo: {self.env.now()}")

class ModeloC(Model):
    def execute(self):
        print(f"[C] Tempo: {self.env.now()}")

# Cria o ambiente com tempo inicial e final definidos
env_a = Environment(name="Modelo A",
                    start_time = 2010, end_time=2016)

# Instancia os modelos com tempos de início e fim diferentes
ModeloA(start_time=2012)
ModeloB(end_time=2013)
ModeloC()

# Roda a simulação
env_a.run()

```

### Saída Esperada:

```
Running from 2010 to 2016 (duration: 6)
[B] Tempo: 2010.0
[C] Tempo: 2010.0
[B] Tempo: 2011.0
[C] Tempo: 2011.0
[A] Tempo: 2012.0
[B] Tempo: 2012.0
[C] Tempo: 2012.0
[A] Tempo: 2013.0
[C] Tempo: 2013.0
[A] Tempo: 2014.0
[C] Tempo: 2014.0
[A] Tempo: 2015.0
[C] Tempo: 2015.0
[A] Tempo: 2016.0
[C] Tempo: 2016.0

```

### Interpretação dos Resultados

Neste exemplo, instanciamos um ambiente de simulação com intervalo temporal entre **2010** e **2016**. Três modelos distintos são inseridos nesse ambiente, cada um com sua configuração temporal específica:

- `ModeloA`: executa a partir de 2012 até o final do ambiente (2016).
- `ModeloB`: inicia em 2010 e termina em 2013.
- `ModeloC`: executa continuamente durante todo o intervalo da simulação, de 2010 a 2016.

A saída mostra os registros temporais de execução de cada modelo, evidenciando como o mecanismo de controle de tempo personalizado permite a execução simultânea e coordenada dos modelos, de acordo com seus respectivos intervalos de atuação.