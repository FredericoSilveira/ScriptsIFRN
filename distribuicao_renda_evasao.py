import pandas as pd
import matplotlib.pyplot as plt

filepath = "/Users/fred/Downloads/dados_alunos_v5.csv"
df = pd.read_csv(filepath, delimiter=';', encoding='utf-8')

df['Percentual de Progresso'] = df['Percentual de Progresso'].str.replace(',', '.').replace('-', '0').astype(float)

df['Renda Per Capita'] = df['Renda Per Capita'].str.replace('.', '').str.replace(',', '.').replace('-', 'NaN').astype(float).clip(lower=0, upper=10000)

df['RPC Segmentada'] = pd.cut(df['Renda Per Capita'], bins=[0, 0.5, 1, 1.5, 2.5, 3.5, float('inf')], labels=['0 < RPC <= 0.5', '0.5 < RPC <= 1', '1 < RPC <= 1.5', '1.5 < RPC <= 2.5', '2.5 < RPC <= 3.5', 'RPC > 3.5'])

df['Situação no Curso'] = df['Situação no Curso'].replace('Desistência', 'Evasão')

df_evasao = df[df['Situação no Curso'] == 'Evasão']

df_evasao.groupby(['Modalidade'])['Matrícula'].count().plot(kind='bar')

plt.show()

for modalidade in df_evasao['Modalidade'].unique():
    df_evasao[df_evasao['Modalidade'] == modalidade].groupby(['RPC Segmentada'])['Matrícula'].count().plot(kind='bar', title=modalidade)

    plt.show()
