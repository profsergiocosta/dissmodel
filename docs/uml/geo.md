# Diagrama de Classes do Pacote Geo

Este diagrama mostra as classes e funções do pacote `geo`, responsável pela geração e manipulação de espaços geográficos.

![Diagrama de Classes do Geo](../images/uml/classes_GeoClasses.png)

## Descrição

O pacote `geo` contém:

- **CellularAutomaton**: Classe principal que herda de `core.Model`, usada para implementar autômatos celulares espaciais baseados em `GeoDataFrame`.
- Funções utilitárias:
  - `fill`: Preenche atributos em `GeoDataFrame` usando estratégias como `FillStrategy`.
  - `neighborhood`: Anexa informações de vizinhança ao `GeoDataFrame` (ex.: usando `libpysal.weights`).
  - `regular_grid`: Cria grades regulares para simulações espaciais.

## Relações

- `CellularAutomaton` herda de `core.Model`.
- Possui associações com `geopandas.GeoDataFrame` e `libpysal.weights` (ex.: `Queen`, `Rook`) para manipulação espacial.
- É usado por classes no subpacote `models/ca`, como `GameOfLife` e `FireModel`.