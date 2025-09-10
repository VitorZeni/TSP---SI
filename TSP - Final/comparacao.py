import time
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# importa a função do genetico e da tempera
from genetico import genetico
from tempera import tempera
from guloso import guloso

# aqui gera uma instancia do problema
def gerar_instancia_problema(num_cidades, max_val):
    cidades = {}
    for i in range(num_cidades):
        cidades[i] = (random.randint(0, max_val), random.randint(0, max_val))
    return cidades

# parâmetros chills
NUM_CIDADES = 10
MAX_VAL = 100
NUM_EXECUCOES = 2

# executa e coleta os dados tsc tsc
resultados = []
amostras = [50, 100, 500]

for j in range(3):
    print(f"executando amostra {amostras[j]}")
    for i in range(NUM_EXECUCOES):

        instancia_cidades = gerar_instancia_problema(amostras[j], MAX_VAL)

        print(f"executando interação {i}")
        start_time = time.time()
        _, distancia = genetico(instancia_cidades.copy())
        end_time = time.time()

        resultados.append({
            'algoritmo': f'Genético {amostras[j]}',
            'execucao': i + 1,
            'distancia': distancia,
            'tempo_s': end_time - start_time
        })

        start_time = time.time()
        _, distancia = tempera(instancia_cidades.copy())
        end_time = time.time()

        resultados.append({
            'algoritmo': f'Têmpera Simulada {amostras[j]}',
            'execucao': i + 1,
            'distancia': distancia,
            'tempo_s': end_time - start_time
        })

        start_time = time.time()
        distancia = guloso(instancia_cidades.copy())
        end_time = time.time()

        resultados.append({
            'algoritmo': f'Guloso {amostras[j]}',
            'execucao': i + 1,
            'distancia': distancia,
            'tempo_s': end_time - start_time
        })

# pra ver e refletir
df_resultados = pd.DataFrame(resultados)

print("\n--- Análise Estatística ---")
print(df_resultados.groupby('algoritmo')['distancia'].describe())


print("\nGerando gráfico de comparação...")
# Box Plot para comparar a distribuição das distâncias
plt.figure(figsize=(10, 6))
sns.boxplot(x='algoritmo', y='distancia', data=df_resultados)
plt.title(f'Comparação de Desempenho ')
plt.xlabel('Algoritmo')
plt.ylabel('Distância Total do Caminho')
plt.grid(True)
plt.show()

# Box Plot para comparar o tempo de execução
plt.figure(figsize=(10, 6))
sns.boxplot(x='algoritmo', y='tempo_s', data=df_resultados)
plt.title(f'Comparação de Tempo de Execução')
plt.xlabel('Algoritmo')
plt.ylabel('Tempo de Execução (segundos)')
plt.grid(True)
plt.show()