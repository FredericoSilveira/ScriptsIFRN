import matplotlib.pyplot as plt
import pandas as pd

filepath = "/Users/fred/Downloads/dados_alunos_v5.csv"
df = pd.read_csv(filepath, delimiter=';', encoding='utf-8')

df['Percentual de Progresso'] = df['Percentual de Progresso'].str.replace(',', '.').replace('-', '0').astype(float)

df['Percentual de Progresso Segmentado'] = pd.cut(df['Percentual de Progresso'], bins=range(0, 101, 10))

df_evasao = df[df['Situação no Curso'] == 'Evasão']

modalidades = df['Modalidade'].unique()

# Configurar subplots para os histogramas separados
fig, axs = plt.subplots(len(modalidades), 1, figsize=(10, 8*len(modalidades)))
fig.subplots_adjust(hspace=0.5)

# Gerar histograma para cada modalidade
for i, modalidade in enumerate(modalidades):
    df_modalidade = df_evasao[df_evasao['Modalidade'] == modalidade]

    ax = axs[i] if len(modalidades) > 1 else axs  # Caso haja apenas uma modalidade, axs será um único subplot

    df_modalidade.groupby('Percentual de Progresso Segmentado').size().plot(kind='bar', ax=ax)

    ax.set_xlabel('Segmento de Percentual de Progresso')
    ax.set_ylabel('Número de Evasões')
    ax.set_title(f'Distribuição de Evasões por Segmento de Percentual de Progresso\nModalidade: {modalidade}')

    # Adicionar rótulos de valor em cada barra
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')

plt.tight_layout()
plt.show()
