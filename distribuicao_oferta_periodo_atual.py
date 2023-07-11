import matplotlib.pyplot as plt
import pandas as pd

filepath = "/Users/fred/Downloads/dados_alunos_final.csv"
df = pd.read_csv(filepath, delimiter=';', encoding='utf-8')

df['Percentual de Progresso'] = df['Percentual de Progresso'].str.replace(',', '.').replace('-', '0').astype(float)

df_evasao = df[df['Situação no Curso'] == 'Evasão']

modalidades = df['Modalidade'].unique()

for modalidade in modalidades:
    df_modalidade = df_evasao[df_evasao['Modalidade'] == modalidade]

    ax = df_modalidade.groupby('Período Atual').size().plot(kind='bar')

    ax.set_xlabel('Período Atual')
    ax.set_ylabel('Número de Evasões')
    ax.set_title(f'Distribuição de Evasões por Período Atual - Modalidade: {modalidade}')

    # Adicionando rótulos de valor em cada barra
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center',
                    xytext=(0, 5), textcoords='offset points')

    plt.show()
