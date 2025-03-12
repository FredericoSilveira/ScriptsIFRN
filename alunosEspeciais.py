import pandas as pd

# Função para filtrar "Matrizes" que contenham "Alunos Especiais"
def filtrar_matrizes_com_alunos_especiais(df):
    return df[df['Matriz'].str.contains("Alunos Especiais", case=False, na=False)]

# Ler as planilhas
planilha1 = pd.read_excel('/Users/fred/Downloads/Pasta2.xlsx')
planilha2 = pd.read_excel('/Users/fred/Downloads/alunos_doutorado.xls')

# Filtrar a planilha 2 para obter apenas as linhas com "Alunos Especiais"
planilha2_filtrada = filtrar_matrizes_com_alunos_especiais(planilha2)

# Obter CPFs únicos da planilha 2 filtrada
cpfs_planilha2 = set(planilha2_filtrada['CPF'])

# Filtrar a planilha 1 para obter os CPFs que não estão na planilha 2 filtrada
planilha1_filtrada = planilha1[~planilha1['CPF'].isin(cpfs_planilha2)]

# Salvar o resultado em uma nova planilha
planilha1_filtrada.to_excel('/Users/fred/Downloads/resultado.xlsx', index=False)

print("A nova planilha foi gerada com sucesso e salva como 'resultado.xlsx'.")
