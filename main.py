from dijkstra.dijkstra_alg import *
from mindijkstra.mindijkstra_alg import *
import networkx as nx
import random
import time

def run_experiment(times: int, nodes_number: int, alg_version: str) -> None:
    """
    Runs the experiment with the chosen version of the Dijkstra algorithm using random connected weighted graphs.

    Args:
        times (int): number of times to repeat the experiment.
        nodes_number (int): maximum number of nodes in the graph to be generated.
        alg_version (str): "normald" or "minheapd" for the classical or MinHeap version of the algorithm.

    Returns:
        None: Prints the time passed and carbon emission of the given test conditions.
    """

    # Varia tamanhos até o máximo suportado
    sizes = [100, 1000, 5000, 10000, 50000, 100000]
    sizes = [n for n in sizes if n <= nodes_number]

    for n in sizes:
        print(f"\n--- Gerando grafo com {n} nós ---")
        start_gen = time.time()

        # Gera um grafo conectado
        # Começa com uma árvore geradora mínima (garante conectividade)
        G = nx.minimum_spanning_tree(nx.gnm_random_graph(n, n + 10))

        # Adiciona arestas extras para aumentar a densidade (opcional)
        extra_edges = int(n * 0.1)  # 10% de arestas extras
        possible_edges = list(nx.non_edges(G))
        random.shuffle(possible_edges)
        for u, v in possible_edges[:extra_edges]:
            G.add_edge(u, v)

        # Atribui pesos aleatórios às arestas
        for (u, v) in G.edges():
            G[u][v]['weight'] = random.randint(1, 100)

        end_gen = time.time()
        print(f"Grafo gerado em {end_gen - start_gen:.2f}s, {G.number_of_edges()} arestas.")

        # Executa o algoritmo escolhido
        for t in range(times):
            source = random.randint(0, n - 1)
            print(f"\nExecução {t+1}/{times} - nó origem: {source}")

            start_time = time.time()
            if alg_version == "normald":
                dijkstrasAlgorithm(source, G)
            elif alg_version == "minheapd":
                minHeapDijkstrasAlgorithm(G, source)
            else:
                print("Versão inválida do algoritmo. Use 'normald' ou 'minheapd'.")
                return

            end_time = time.time()
            print(f"Tempo de execução: {end_time - start_time:.2f}s")

run_experiment(5, 10, alg_version='normald')