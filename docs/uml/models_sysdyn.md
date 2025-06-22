# Diagrama de Classes do Subpacote Models/SysDyn

Este diagrama exibe as classes do subpacote `models/sysdyn`, que implementam modelos de dinâmica de sistemas.

![Diagrama de Classes do Models/SysDyn](../images/uml/classes_SysDynModels.png)

## Descrição

O subpacote `models/sysdyn` contém classes que herdam de `core.Model` para simular dinâmicas contínuas:

- **SIR**: Modela a propagação de doenças (Suscetível, Infectado, Recuperado).
- **PredatorPrey**: Simula a dinâmica predador-presa.
- **PopulationGrowth**: Modela o crescimento populacional.
- **Lorenz**: Implementa o sistema de equações de Lorenz (caos).
- **Daisyworld**: Simula a regulação climática com margaridas.
- **Coffee**: Modela o resfriamento de uma xícara de café.

## Relações

- Todas as classes herdam de `core.Model`.
- Utilizam o decorador `visualization.track_plot` para rastrear variáveis e gerar gráficos.
- Integram-se com `core.Environment` para gerenciar o tempo da simulação.