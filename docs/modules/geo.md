# Geo 

O módulo dissmodel.geo fornece utilitários para modelagem espacial, como:

```
from dissmodel.geo import Neighborhood, regular_grid, fill
```

Antes de destacar esses recurso, é importante ressaltar que **O coração da integração geográfica** está no fato de que qualquer modelo pode operar **diretamente sobre um `GeoDataFrame`** do GeoPandas. Isso permite que se use dados espaciais reais (como shapefiles, arquivos GeoJSON, etc.) como entrada e saída do modelo, facilitando análises espaciais visuais e quantitativas.

---

## Exemplo Simples de uso de dados geográficos

Começando pela  **definição do Modelo**

```python
@track_plot("media_altitude", "blue")
class ElevacaoSimples(Model):
    seaLevelRiseRate: float
    media_altitude: float

    def setup(self, gdf, seaLevelRiseRate=0.01):
        self.gdf = gdf
        self.seaLevelRiseRate = seaLevelRiseRate
        self.media_altitude = 0

    def execute(self):
        self.gdf["Alt2"] += self.seaLevelRiseRate
        self.media_altitude = self.gdf["Alt2"].mean()

```

- `gdf`: o `GeoDataFrame` com a geometria e atributos espaciais.
- A cada passo de tempo, a elevação (`Alt2`) é incrementada de forma uniforme.
- A média da elevação é calculada para acompanhamento em gráfico.

---

**Leitura dos Dados Geográficos**

```python
gdf = gpd.read_file("filename.shp")
```

O shapefile é carregado como um `GeoDataFrame`, que armazena:

- Informações espaciais (coluna `geometry`);
- Atributos como `"Alt2"` (elevação), `"Usos"`, etc.

---

**Instanciação do Modelo e Ambiente**

```python
env = Environment(start_time=1, end_time=20)
modelo = ElevacaoSimples(gdf=gdf, seaLevelRiseRate=0.01)

```

- O `Environment` controla o tempo e executa todos os modelos registrados.
- O modelo recebe o `GeoDataFrame` como parâmetro — isso já o conecta à estrutura espacial dos dados.

---

**Visualização Espacial e Temporal**

- Mapa

```python
Map(gdf=gdf, plot_params={
    "column": "Alt2", "scheme": "quantiles", "k": 5,
    "legend": True, "cmap": "Blues"
})

```

- O mapa mostra a coluna `Alt2` (elevação), atualizada a cada passo da simulação.
- A visualização pode ser local (matplotlib) ou em apps interativos (como Streamlit).

- Gráfico

```python
Chart(select={"media_altitude"})

```

- A curva da média de elevação é exibida dinamicamente ao longo do tempo.
- O decorador `@track_plot` automatiza isso sem código adicional.

---

**Execução da Simulação**

```python
env.run()
```

Com esse comando, o ambiente:

- Avança no tempo de `start_time` até `end_time`;
- Chama `execute()` do modelo a cada passo;
- Atualiza mapas e gráficos automaticamente.

---

Essa integração mostra a força da **orientação a objetos no DisSModel**: modelos simples podem operar diretamente sobre dados reais com código mínimo. Isso torna possível:

✅ Prototipar rapidamente cenários ambientais, urbanos, etc.

✅ Visualizar dinamicamente mapas e séries temporais.

✅ Ampliar o modelo com lógica espacial (vizinhança, inundação, etc.).




## Grade Regular (Regular Grid)


A função `regular_grid` cria um **grade retangular** de células (ou seja, polígonos quadrados ou retangulares), retornando um `GeoDataFrame` contendo:

- A geometria de cada célula (`Polygon`);
- Um identificador único (`id`);
- Atributos opcionais que podem ser usados na simulação;
- CRS opcional.

Esse tipo de estrutura é especialmente útil em modelos **baseados em espaço celular**, comuns em ecologia, urbanismo, dinâmica populacional, etc.


Você pode gerar a grade de 3 formas principais:

### 1. A partir de um `GeoDataFrame`

```python
regular_grid(gdf=meu_gdf, resolution=100)

```

Gera uma grade que cobre completamente os limites espaciais de um GeoDataFrame, com células de 100x100 unidades no sistema de coordenadas usado.

---

### 2. A partir de `bounds` e `resolution`

```python
regular_grid(bounds=(0, 0, 1000, 1000), resolution=100)

```

Gera uma grade regular de 10x10 células de 100x100 metros, cobrindo uma área de 1km².

---

### 3. A partir de `dimension` e `resolution` (sem localização geográfica)

```python
regular_grid(dimension=(5, 4), resolution=50)

```

Gera uma grade de 5 colunas e 4 linhas com células de 50x50 unidades, posicionada com canto inferior esquerdo em (0, 0). Útil para simulações puramente abstratas.

---

### 🧪 Exemplos de Uso

#### ✅ Exemplo 1: Grid sobre shapefile real

```python
import geopandas as gpd
from dissmodel.geo import regular_grid

gdf_base = gpd.read_file("usos.shp")
grid = regular_grid(gdf=gdf_base, resolution=50)

grid.plot(edgecolor="gray", facecolor="none")

```

Esse exemplo cria uma malha com células de 50 metros de lado sobre o shapefile de entrada. Pode ser usada para acoplar dados raster, simular ocupações ou iniciar modelos baseados em vizinhança.

---

#### ✅ Exemplo 2: Grid com atributos personalizados

```python
grid = regular_grid(bounds=(0, 0, 500, 500), resolution=100, attrs={"elevacao": 0.5, "ocupado": False})
print(grid.head())

```

Esse grid terá células de 100x100 cobrindo 500x500 unidades, cada uma com os atributos `"elevacao"` e `"ocupado"` inicializados.

---

#### ✅ Exemplo 3: Grid abstrato (sem localização real)

```python
grid = regular_grid(dimension=(10, 10), resolution=1)
grid.plot()

```

Cria uma grade 10x10 sem referência espacial (inicia em (0, 0)), útil para testes ou modelos conceituais sem georreferenciamento.

---
### Uso típico
O grid gerado pode ser usado diretamente em modelos como este:

```python
class ModeloAbstrato(Model):

    def setup(self, gdf):
        self.gdf = gdf

    def execute(self):
        # Simples exemplo: aumenta o valor de uma variável fictícia
        self.gdf["valor"] += 1

```

Você pode acoplar dados externos ao grid, usar `dissmodel.geo.Neighborhood` para definir vizinhanças, ou aplicar lógicas espaciais em cima dele.

---


A função `regular_grid` permite que você:

- Crie grades celulares alinhadas com o espaço real;
- Construa modelos espaciais com ou sem georreferenciamento;
- Agregue atributos simulados ou observados por célula;
- Visualize ou exporte esses grids para análise geográfica.


## Fill (preenchimento de células)

O módulo `fill` permite **atribuir ou agregar dados espaciais de forma automática** a uma grade regular.

Esse processo é essencial para modelagem espacial, pois permite associar:

- 📊 **dados contínuos** (ex: altitude, NDVI, temperatura — via **estatísticas zonais**);
- 📍 **dados pontuais ou poligonais** (ex: distância a rios, estradas — via **distância mínima**);
- 🎲 **dados sintéticos ou padrões** (ex: valores simulados — via **amostragem aleatória** ou padrões predefinidos).

---

**✳️ Estrutura do Módulo `fill`**

- `fill(strategy="nome", **kwargs)`: Interface principal.
- `FillStrategy`: Enum com estratégias como `zonal_stats`, `min_distance`, `random_sample`, `pattern`.

---

A seguir são apresentados alguns exemplos

### ✅ 1. Preencher a grade com estatísticas zonais de um raster (ex: altitude média por célula)

```python
from dissmodel.geo import regular_grid, fill, FillStrategy
import rasterio

# Cria a grade regular com base em shapefile de interesse
gdf_base = gpd.read_file("area.shp")
grade = regular_grid(gdf=gdf_base, resolution=50)

# Abre o raster
with rasterio.open("altitude.tif") as src:
    raster = src.read(1)
    affine = src.transform

# Aplica estatísticas zonais
fill(
    strategy=FillStrategy.ZONAL_STATS,
    vectors=grade,
    raster_data=raster,
    affine=affine,
    stats=["mean", "min", "max"],
    prefix="alt_"
)

print(grade[["alt_mean", "alt_min", "alt_max"]].head())

```

🔹 **Uso típico**: preencher as células com a média de elevação, cobertura vegetal, umidade, etc.

---

### ✅ 2. Atribuir a cada célula a menor distância até feições de interesse (ex: rios ou estradas)

```python
rios = gpd.read_file("rios.shp")

fill(
    strategy=FillStrategy.MIN_DISTANCE,
    from_gdf=grade,
    to_gdf=rios,
    attr_name="dist_rio"
)

print(grade[["dist_rio"]].head())

```

🔹 **Uso típico**: simulações que dependem de acessibilidade, risco de inundação, zonas de influência.

---

### ✅ 3. Amostragem aleatória de valores (ex: estados iniciais de ocupação, altitude sintética)

```python
fill(
    strategy=FillStrategy.RANDOM_SAMPLE,
    gdf=grade,
    attr="ocupacao",
    data={0: 0.7, 1: 0.3},  # 70% de células com 0, 30% com 1
    seed=42
)

grade["ocupacao"].value_counts()

```

🔹 **Uso típico**: inicializar modelos com padrões aleatórios realistas.

---

### ✅ 4. Aplicar um padrão fixo em grade (útil para testes ou comportamentos controlados)

```python

pattern = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]

fill(
    strategy=FillStrategy.PATTERN,
    gdf=grade,
    attr="tipo",
    pattern=pattern,
    start_x=0,
    start_y=0
)

grade["tipo"].value_counts()

```

🔹 **Uso típico**: teste de difusão, padrões iniciais em simulações de propagação, checagem visual.




A função `fill` e suas estratégias oferecem uma interface flexível e extensível para:

- **Integrar dados vetoriais e raster** a grades espaciais;
- **Preparar dados** de entrada para modelos baseados em célula;
- **Realizar análises espaciais simples** sem depender de ferramentas externas complexas.

Você pode até registrar novas estratégias personalizadas usando:

```python
@register_strategy("min_max_ratio")
def fill_min_max_ratio(...):
    ...

```



## Neighborhood (vizinhança)

- Permite construir relações de vizinhança via:
    - `strategy` (ex: `Queen`, `Rook` — adjacência com base em borda ou vértice)
    - Um dicionário `neighbors_dict` com vizinhos precomputados (ou de um JSON salvo)
- Exponibiliza:
    - `.neighs(idx)`: retorna o subconjunto `GeoDataFrame` com os vizinhos da célula `idx`
    - `.idxs(idx)`: retorna apenas os índices dos vizinhos

---

### ✅ Exemplo de Uso — Construção de vizinhança

```python
import geopandas as gpd
from libpysal.weights import Queen
from dissmodel.geo import Neighborhood

# Carregar grade ou polígonos
grade = gpd.read_file("grade_espacial.shp")

# Criar vizinhança do tipo Queen
vizinhanca = Neighborhood(strategy=Queen, gdf=grade, ids=grade.index)

# Ver vizinhos do elemento "5-4"
vizinhos_54 = vizinhanca.neighs("5-4")
print(vizinhos_54)

# Apenas os índices
print(vizinhanca.idxs("5-4"))

```

---

### 🧩 Exemplo dentro de um modelo: Difusão simples

Simulação de difusão onde cada célula adota o valor mais comum entre os vizinhos.

```python
from dissmodel.core import Model
from dissmodel.geo import Neighborhood
from collections import Counter

class DifusaoVizinhos(Model):
    def setup(self, gdf, attr="estado"):
        self.gdf = gdf
        self.attr = attr
        self.neigh = Neighborhood(strategy=Queen, gdf=gdf)

    def execute(self):
        novo_estado = {}

        for idx in self.gdf.index:
            vizinhos = self.neigh.idxs(idx)
            estados = self.gdf.loc[vizinhos, self.attr].tolist()
            if estados:
                mais_comum = Counter(estados).most_common(1)[0][0]
                novo_estado[idx] = mais_comum
            else:
                novo_estado[idx] = self.gdf.loc[idx, self.attr]

        self.gdf[self.attr] = self.gdf.index.map(novo_estado.get)

```

---

### 💾 Uso com vizinhança salva (JSON)

Você pode **salvar** a vizinhança pré-computada para reaproveitar ou ganhar performance:

```python
import json

# Salva dicionário de vizinhança
with open("vizinhanca.json", "w") as f:
    json.dump(vizinhanca.w_.neighbors, f)

# Carrega depois em outro ambiente
viz_salva = Neighborhood(neighbors_dict="vizinhanca.json")

```

---

### 📌 Aplicações comuns e integração com os modelos

| Objetivo | Estratégia |
| --- | --- |
| Modelos de difusão/propagação | Obter estados dos vizinhos |
| Autômatos celulares | Aplicar regras com base na vizinhança |
| Cálculo de estatísticas locais (ex: LISA) | Base para métricas espaciais locais |
| Aglomeração / clusterização regional | Definir contiguidade |
| Suavização de valores espaciais | Média/Moda entre vizinhos |

---


Esse componente se encaixa perfeitamente nos modelos espaciais da biblioteca `DisSModel`, pois você pode:

- Incluir a vizinhança como parte do `setup`
- Usar `self.neigh.idxs(idx)` no `execute`
- Trabalhar com padrões locais de interação espacial


Além de vizinhança topológica, é possível construir vizinhança **por distância** com `KNN`:

```python

from libpysal.weights import KNN
viz_knn = Neighborhood(strategy=KNN, gdf=grade, k=4)

print("Vizinhos de 5-5:", viz_knn.idxs("5-5"))

```

> 🧠 Útil em contextos como redes de sensores, dados de pontos ou quando os polígonos não se tocam.
> 

---

### 📌 Propagação Probabilística

Esse modelo representa um processo de **difusão espacial** com regras locais baseadas em vizinhança, útil para simulações como **contágio, incêndios florestais, epidemias, ou disseminação de inovação**.

```python
from dissmodel.core import Model
import numpy as np

class PropagacaoKNN(Model):
    def setup(self, gdf, attr="estado", k=4, prob=0.3):
        self.gdf = gdf
        self.attr = attr
        self.k = k
        self.prob = prob
        from dissmodel.geo import Neighborhood
        from libpysal.weights import KNN
        self.viz = Neighborhood(strategy=KNN, gdf=gdf, k=k)

    def execute(self):
        novo_estado = self.gdf[self.attr].copy()
        for idx in self.gdf.index:
            if self.gdf.loc[idx, self.attr] == 1:
                continue
            vizinhos = self.viz.idxs(idx)
            if any(self.gdf.loc[v, self.attr] == 1 for v in vizinhos):
                if np.random.rand() < self.prob:
                    novo_estado.loc[idx] = 1
        self.gdf[self.attr] = novo_estado

```

