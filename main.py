import time
import random
import warnings
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
from codecarbon import OfflineEmissionsTracker

from dijkstra.dijkstra_alg import dijkstrasAlgorithm
from mindijkstra.mindijkstra_alg import minHeapDijkstrasAlgorithm

# Ignorar warnings para manter a saída limpa
warnings.filterwarnings('ignore', category=UserWarning)

def convert_nx_to_adj_list(G: nx.Graph):
    """
    Converte um grafo networkx para o formato de lista de adjacências
    exigido pela sua função: list[list[list[int]]].
    """
    nodes_count = G.number_of_nodes()
    adj_list = [[] for _ in range(nodes_count)]
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        # Adiciona a aresta nos dois sentidos se o grafo for não direcionado
        adj_list[u].append([v, weight])
        adj_list[v].append([u, weight])
    return adj_list

def generate_connected_weighted_graph(nodes_number: int):
    """Gera um grafo ponderado e conectado de forma eficiente."""
    #G = nx.barabasi_albert_graph(nodes_number, 2, seed=42)
    G = nx.gnp_random_graph(nodes_number, 2, 42)
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(1, 20)
    return G

def run_dijkstra_versions(graph, adj_list, source_nodes):
    """
    Executa as três versões de Dijkstra para um conjunto de nós de origem.
    Agora aceita o grafo em dois formatos diferentes.
    """
    results = []
    algorithms = {
        "Dijkstra Clássico": dijkstrasAlgorithm,
        "Dijkstra com Min-Heap": minHeapDijkstrasAlgorithm,
        "NetworkX Dijkstra": nx.single_source_dijkstra,
    }

    for name, func in algorithms.items():
        tracker = OfflineEmissionsTracker(country_iso_code="BRA", log_level='error')
        tracker.start()
        
        start_time = time.time()
        for node in source_nodes:
            # Condicional para chamar cada função com os argumentos e formato corretos
            if "NetworkX" in name:
                func(graph, node)
            else:
                # Chama sua função com (start, edges) na ordem correta
                func(node, adj_list)
        end_time = time.time()
        
        emissions_data = tracker.stop()

        results.append({
            "Algorithm": name,
            "Time (s)": end_time - start_time,
            "CO2 Emission (kg)": emissions_data if emissions_data else 0
        })
    return results

def run_experiment(
    times: int = 20,
    node_sizes: list = [100, 500, 1000, 2500, 5000, 10000]
) -> None:
    """
    Executa o experimento comparativo com diferentes versões do algoritmo de Dijkstra.
    """
    all_results = []
    
    print("Iniciando o experimento...")

    for nodes_number in node_sizes:
        print(f"\nProcessando grafos com {nodes_number} nós...")
        graph = generate_connected_weighted_graph(nodes_number)
        # Converte o grafo para o formato de lista de adjacências uma vez por tamanho
        adj_list_for_custom_func = convert_nx_to_adj_list(graph)
        
        for i in range(times):
            print(f"  Repetição {i + 1}/{times}...")
            source_nodes = random.sample(list(graph.nodes), 5)
            # Passa ambos os formatos de grafo para a função de teste
            run_results = run_dijkstra_versions(graph, adj_list_for_custom_func, source_nodes)
            
            for result in run_results:
                result['Nodes'] = nodes_number
                result['Repetition'] = i + 1
                all_results.append(result)

    df_results = pd.DataFrame(all_results)
    df_results.to_csv("dijkstra_experiment_raw_results.csv", index=False)
    
    summary = df_results.groupby(['Nodes', 'Algorithm']).agg(
        Mean_Time=('Time (s)', 'mean'),
        Std_Time=('Time (s)', 'std'),
        Mean_CO2=('CO2 Emission (kg)', 'mean'),
        Std_CO2=('CO2 Emission (kg)', 'std')
    ).reset_index()

    def calculate_ci(mean, std, n, confidence=0.95):
        if std == 0 or pd.isna(std): return (mean, mean)
        se = std / np.sqrt(n)
        ci = st.t.interval(confidence, df=n-1, loc=mean, scale=se)
        return ci

    summary['Time CI 95%'] = summary.apply(
        lambda row: calculate_ci(row['Mean_Time'], row['Std_Time'], times), axis=1)
    summary['CO2 Emission CI 95%'] = summary.apply(
        lambda row: calculate_ci(row['Mean_CO2'], row['Std_CO2'], times), axis=1)
                       
    summary.to_csv("dijkstra_experiment_summary.csv", index=False)
    print("\nTabela de resumo salva em 'dijkstra_experiment_summary.csv'")
    
    generate_plots(summary)
    print("Gráficos comparativos salvos em 'execution_time_comparison.png' e 'co2_emission_comparison.png'")

def generate_plots(summary_df: pd.DataFrame):
    """Gera e salva gráficos comparativos a partir do DataFrame de resumo."""
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig_time, ax_time = plt.subplots(figsize=(12, 7))
    for name, group in summary_df.groupby('Algorithm'):
        ax_time.plot(group['Nodes'], group['Mean_Time'], marker='o', linestyle='-', label=name)
        
    ax_time.set_title('Tempo de Execução Médio vs. Número de Nós', fontsize=16)
    ax_time.set_xlabel('Número de Nós', fontsize=12)
    ax_time.set_ylabel('Tempo de Execução Médio (s)', fontsize=12)
    ax_time.legend()
    ax_time.grid(True, which='both', linestyle='--')
    fig_time.tight_layout()
    fig_time.savefig("execution_time_comparison.png")

    fig_co2, ax_co2 = plt.subplots(figsize=(12, 7))
    for name, group in summary_df.groupby('Algorithm'):
        ax_co2.plot(group['Nodes'], group['Mean_CO2'], marker='o', linestyle='-', label=name)

    ax_co2.set_title('Emissão Média de CO₂ vs. Número de Nós', fontsize=16)
    ax_co2.set_xlabel('Número de Nós', fontsize=12)
    ax_co2.set_ylabel('Emissão Média de CO₂ (kg)', fontsize=12)
    ax_co2.legend()
    ax_co2.grid(True, which='both', linestyle='--')
    fig_co2.tight_layout()
    fig_co2.savefig("co2_emission_comparison.png")

if __name__ == '__main__':
    node_sizes_to_test = [100,500,1000,5000,10000,50000,100000] 
    #node_sizes_to_test = [10,100]
    run_experiment(times=5, node_sizes=node_sizes_to_test)