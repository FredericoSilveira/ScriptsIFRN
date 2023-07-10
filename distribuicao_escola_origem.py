import pandas as pd
import matplotlib.pyplot as plt

filepath = "/Users/fred/Downloads/dados_alunos_v5.csv"
df = pd.read_csv(filepath, delimiter=';', encoding='utf-8')

df['Percentual de Progresso'] = df['Percentual de Progresso'].str.replace(',', '.').replace('-', '0').astype(float)

df_evasao = df[df['Situação no Curso'] == 'Evasão']

# Histograma geral
plt.figure(figsize=(10, 6))
df_evasao['Percentual de Progresso'].plot(kind='hist', bins=range(0, 101, 10), rwidth=0.8, color='blue')
plt.xlabel('Percentual de Progresso')
plt.ylabel('Número de Evasões')
plt.title('Distribuição de Evasões\npor Segmento de Percentual de Progresso (Geral)')
plt.show()

# Histograma por modalidade, dividido por Tipo de Escola de Origem
modalidades = df['Modalidade'].unique()

for modalidade in modalidades:
    plt.figure(figsize=(10, 6))
    df_modalidade = df_evasao[df_evasao['Modalidade'] == modalidade]

    # Histograma para Tipo de Escola de Origem = "Privada"
    df_privada = df_modalidade[df_modalidade['Tipo de Escola de Origem'] == 'Privada']
    plt.hist(df_privada['Percentual de Progresso'], bins=range(0, 101, 10), rwidth=0.8, color='orange')
    plt.xlabel('Percentual de Progresso')
    plt.ylabel('Número de Evasões')
    plt.title(f'Distribuição de Evasões\npor Segmento de Percentual de Progresso\nModalidade: {modalidade}\nTipo de Escola de Origem: Privada')
    plt.show()

    # Histograma para Tipo de Escola de Origem = "Pública"
    df_publica = df_modalidade[df_modalidade['Tipo de Escola de Origem'] == 'Pública']
    plt.hist(df_publica['Percentual de Progresso'], bins=range(0, 101, 10), rwidth=0.8, color='green')
    plt.xlabel('Percentual de Progresso')
    plt.ylabel('Número de Evasões')
    plt.title(f'Distribuição de Evasões\npor Segmento de Percentual de Progresso\nModalidade: {modalidade}\nTipo de Escola de Origem: Pública')
    plt.show()
