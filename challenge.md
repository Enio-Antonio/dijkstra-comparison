# Comparação de Performance: Dijkstra Clássico vs Dijkstra com Min-Heap


## Objetivo


Avaliar **tempo de execução** e **pegada de carbono (CO₂)** das seguintes abordagens de caminho mínimo:
- **Dijkstra Clássico** (`O(V² + E)`), conforme implementado em sala;
- **Dijkstra com Min-Heap** (`O((V + E) * log V)`), conforme implementado em sala;

> **Obrigatório**: reutilizar as **versões das aulas** (`dijsktra.ipynb` e `dijsktra_min_heap.ipynb`). Ajustes menores são permitidos (p.ex., medições, modularização, execução), sem mudar a lógica.


## Descrição do Problema


Você deverá:
1. Gerar **grafos ponderados e conectados** com o `networkx` em diferentes tamanhos, **indo até 100.000 nós** (ou o máximo suportado pela sua máquina).
2. Para cada grafo, escolher **5 nós aleatórios** e calcular o **caminho mínimo** desses nós para **todos os demais nós** usando:
   - A versão **clássica** de Dijkstra;
   - A versão **com Min-Heap**;
   - A função de **referência** do `networkx`.
3. Repetir o experimento **15 a 20 vezes por tamanho** (trocando os 5 nós a cada repetição) para robustez estatística.
4. Medir e registrar para cada execução:
   - **Tempo** (s);
   - **CO₂** com [CodeCarbon](https://github.com/mlco2/codecarbon).
5. Calcular Intervalos de Confiança para as médias de tempo e CO₂.
6. Gerar **gráficos** e **tabelas** comparativas e **salvá-los no repositório**.



### Configuração Experimental


- Tamanhos sugeridos: `[100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]`.
- **Reprodutibilidade**: fixe sementes (`numpy` e `random`).
- Geração de grafos: `nx.gnp_random_graph(n, p)` com pesos inteiros positivos (ex.: `1..10`).  
  Garanta conectividade (ex.: use o **componente gigante** quando necessário).
- **15–20 repetições** por tamanho; **5 fontes** por repetição.
- Evite travamentos validando primeiro em tamanhos menores.

### Métricas e Estatística


Nesta etapa, você vai transformar os dados brutos coletados (tempos e emissões de CO₂ de cada execução) em informações **estatisticamente interpretáveis**.  
O objetivo é comparar o desempenho dos algoritmos a partir das **médias** e **desvios-padrão** das execuções.


Para cada par **(tamanho do grafo, algoritmo)**, calcule:

| Métrica | Símbolo | Descrição |
|----------|----------|-----------|
| Média | \\\\(\\bar{x}\\\\) | Tempo médio (ou CO₂ médio) das execuções |
| Desvio-padrão | \\\\(s\\\\) | Mede a variação dos resultados em torno da média |


Para cada algoritmo e tamanho de grafo, plote:

- **Eixo X:** número de nós do grafo  
- **Eixo Y:** tempo médio (ou CO₂ médio)  
- **Uma linha para cada algoritmo**  
- **Barras verticais** indicando a variação (\\(\bar{x} \pm s\\))



## Entregáveis


- **Repositório GitHub** contendo:
  - Notebook `.ipynb` com código, análises, **gráficos salvos** (`.png`/`.svg`) e tabelas (`.csv`);
  - `README.md` explicando metodologia, resultados e **link do vídeo**;
  - Vídeo (até 10min) Explique rapidamente os algoritmos, mostre a execução, apresente gráficos e discuta resultados. Sugestão de ferramentas (Loom e Youtube).
  - Organização clara e reprodutível (seções, funções, seeds).


## Avaliação (3 pts – Unidade 2)


| Critério | Descrição | Peso |
|---|---|---|
| Organização e reprodutibilidade | Estrutura limpa, README completo, seeds e scripts | 1.0 |
| Correção e **reutilização** das versões de sala | Aderência às implementações solicitadas | 1.0 |
| Análise e apresentação | Interpretação dos resultados, gráficos e vídeo | 1.0 |

**Individual ou em dupla.**

## Exemplos de código
```
!pip install codecarbon
```

```
import networkx as nx
import random
import matplotlib.pyplot as plt
import time
from codecarbon import EmissionsTracker

# Inicia o rastreador de emissões
tracker = EmissionsTracker(output_dir=".", save_to_file=False, log_level="error")
tracker.start()

# Mede o tempo total de geração e plotagem
start = time.time()

# Cria um grafo aleatório com 10 nós e probabilidade 0.3
G = nx.gnp_random_graph(n=10, p=0.3, seed=42)

# Adiciona pesos (inteiros entre 1 e 10)
for u, v in G.edges():
    G[u][v]['weight'] = random.randint(1, 10)

# Mostra algumas arestas com peso
for u, v, data in list(G.edges(data=True))[:5]:
    print(f"Aresta {u}-{v}, peso = {data['weight']}")

# Visualização com pesos nas arestas
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
plt.show()

# Finaliza o cálculo de tempo e emissões
end = time.time()
elapsed = end - start
emissions = tracker.stop()

print(f"Tempo total de execução: {elapsed:.3f} segundos")

print(f"Pegada de carbono estimada: {emissions:.8f} kg de CO₂e")
```