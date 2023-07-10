import matplotlib.pyplot as plt
import pandas as pd

filepath = "/Users/fred/Downloads/dados_alunos_v5.csv"
df = pd.read_csv(filepath, delimiter=';', encoding='utf-8')

df['Percentual de Progresso'] = df['Percentual de Progresso'].str.replace(',', '.').replace('-', '0').astype(float)

df['Percentual de Progresso Segmentado'] = pd.cut(df['Percentual de Progresso'], bins=range(0, 101, 10))

df_evasao = df[df['Situação no Curso'] == 'Evasão']

ax = df_evasao.groupby('Percentual de Progresso Segmentado').size().plot(kind='bar')

ax.set_xlabel('Segmento de Percentual de Progresso')
ax.set_ylabel('Número de Evasões')
ax.set_title('Distribuição de Evasões por Segmento de Percentual de Progresso')

# Adicionando rótulos de valor em cada barra
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')

plt.show()
