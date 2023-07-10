import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm

filepath = "/Users/fred/Downloads/dados_alunos_v5.csv"
df = pd.read_csv(filepath, delimiter=';', encoding='utf-8')

df['I.R.A.'] = df['I.R.A.'].str.replace(',', '.').astype(float)

df_evasao = df[df['Situação no Curso'] == 'Evasão']

# Histograma geral de todas as modalidades
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(df_evasao['I.R.A.'], bins=range(0, 101, 10), rwidth=0.8, color='blue', edgecolor='black')
plt.xlabel('I.R.A.')
plt.ylabel('Número de Evasões')
plt.title('Distribuição de Evasões por Segmento de I.R.A. (Geral)')

# Adicionar rótulos de valor em cada barra
for i in range(len(patches)):
    plt.text(patches[i].get_x() + patches[i].get_width() / 2, patches[i].get_height(), int(n[i]),
             ha='center', va='bottom')

# Traçar distribuição gaussiana
mu, sigma = norm.fit(df_evasao['I.R.A.'])
x = np.linspace(min(bins), max(bins), 100)
y = norm.pdf(x, mu, sigma)
plt.plot(x, y, 'r-', linewidth=2)

plt.show()

# Histograma por modalidade
modalidades = df['Modalidade'].unique()

for modalidade in modalidades:
    plt.figure(figsize=(10, 6))
    df_modalidade = df_evasao[df_evasao['Modalidade'] == modalidade]
    n, bins, patches = plt.hist(df_modalidade['I.R.A.'], bins=range(0, 101, 10), rwidth=0.8, color='orange', edgecolor='black')
    plt.xlabel('I.R.A.')
    plt.ylabel('Número de Evasões')
    plt.title(f'Distribuição de Evasões por Segmento de I.R.A.\nModalidade: {modalidade}')

    # Adicionar rótulos de valor em cada barra
    for i in range(len(patches)):
        plt.text(patches[i].get_x() + patches[i].get_width() / 2, patches[i].get_height(), int(n[i]),
                 ha='center', va='bottom')

    # Traçar distribuição gaussiana
    mu, sigma = norm.fit(df_modalidade['I.R.A.'])
    x = np.linspace(min(bins), max(bins), 100)
    y = norm.pdf(x, mu, sigma)
    plt.plot(x, y, 'r-', linewidth=2)

    plt.show()
