import matplotlib.pyplot as plt
import pandas as pd

def generate_plots(summary_df: pd.DataFrame):
    """
    Gera e salva gráficos comparativos a partir do DataFrame de resumo,
    agora incluindo barras de erro de desvio padrão.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # --- Gráfico de Tempo de Execução com Barras de Erro ---
    fig_time, ax_time = plt.subplots(figsize=(12, 7))
    
    # Agrupa por algoritmo para plotar cada um separadamente
    for name, group in summary_df.groupby('Algorithm'):
        ax_time.errorbar(
            x=group['Nodes'], 
            y=group['Mean_Time'], 
            yerr=group['Std_Time'],  # Usa o Desvio Padrão (Std) como barra de erro
            marker='o', 
            linestyle='-', 
            label=name,
            capsize=5  # Adiciona "caps" nas barras de erro para melhor visualização
        )
        
    ax_time.set_title('Tempo de Execução Médio vs. Número de Nós (com Desvio Padrão)', fontsize=16)
    ax_time.set_xlabel('Número de Nós', fontsize=12)
    ax_time.set_ylabel('Tempo de Execução Médio (s)', fontsize=12)
    ax_time.legend()
    ax_time.grid(True, which='both', linestyle='--')
    fig_time.tight_layout()
    fig_time.savefig("execution_time_comparison.png")

    # --- Gráfico de Emissões de CO₂ com Barras de Erro ---
    fig_co2, ax_co2 = plt.subplots(figsize=(12, 7))
    
    for name, group in summary_df.groupby('Algorithm'):
        ax_co2.errorbar(
            x=group['Nodes'], 
            y=group['Mean_CO2'], 
            yerr=group['Std_CO2'],  # Usa o Desvio Padrão (Std) como barra de erro
            marker='o', 
            linestyle='-', 
            label=name,
            capsize=5
        )

    ax_co2.set_title('Emissão Média de CO₂ vs. Número de Nós (com Desvio Padrão)', fontsize=16)
    ax_co2.set_xlabel('Número de Nós', fontsize=12)
    ax_co2.set_ylabel('Emissão Média de CO₂ (kg)', fontsize=12)
    ax_co2.legend()
    ax_co2.grid(True, which='both', linestyle='--')
    fig_co2.tight_layout()
    fig_co2.savefig("co2_emission_comparison.png")

summary = pd.read_csv('dijkstra_experiment_summary.csv')

generate_plots(summary)