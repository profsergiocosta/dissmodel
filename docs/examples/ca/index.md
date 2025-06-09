# Autômatos Celulares no DisSModel

Autômatos celulares são modelos baseados em grades espaciais discretas, onde cada célula evolui segundo regras locais que dependem do estado da própria célula e de suas vizinhas.

No contexto do **DisSModel**, utilizamos autômatos celulares para simular processos como:

- Dinâmica de populações (ex. *Game of Life*)
- Propagação de distúrbios (ex. queimadas)
- Mudanças em coberturas do solo

A estrutura geral de um autômato celular no DisSModel inclui:

- Um ambiente espacial regular (grid)
- Um atributo de estado por célula
- Uma vizinhança (Rook, Queen, ou KNN via PySAL)
- Uma regra de atualização (`rule`)
- Um ciclo de execução (`execute`)

## Estratégias de vizinhança

O DisSModel suporta diversas estratégias de vizinhança:

- **Rook**: considera células vizinhas nas direções ortogonais (N, S, L, O)
- **Queen**: considera também as diagonais (N, NE, L, SE, S, SO, O, NO)
- **KNN**: vizinhos com base na proximidade (via `libpysal.weights.KNN`)

Você pode usar qualquer uma dessas abordagens com o objeto `Neighborhood`, por exemplo:

```python
from libpysal.weights import KNN
neigh = Neighborhood(KNN, gdf, use_index=True, k=4)
