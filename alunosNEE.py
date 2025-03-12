import pandas as pd

# Carregar o arquivo Excel
df = pd.read_excel("/Users/fred/Downloads/Relatorio-nee-2 - cópia.xlsx")

# Colunas relevantes para verificar NEE
cols_nee = ["Deficiência", "Transtorno", "Superdotação"]

# Contar registros onde pelo menos uma coluna NEE está preenchida (não é "-")
nee_count = df[cols_nee].apply(
    lambda row: any(value.strip() != "-" for value in row),
    axis=1
).sum()

print(f"Total de estudantes com NEE: {nee_count}")

# Máscara para estudantes com NEE
nee_mask = (df[cols_nee] != "-").any(axis=1)

# 1. Total de alunos de escola pública
total_publicos = df[df["Tipo de Escola de Origem"] == "Pública"].shape[0]

# 2. Alunos de escola pública com NEE
publicos_com_nee = df[nee_mask & (df["Tipo de Escola de Origem"] == "Pública")].shape[0]

# 3. Alunos com NEE por ano de ingresso (2020 a 2025)
anos = [2020, 2021, 2022, 2023, 2024, 2025]
nee_por_ano = {}
for ano in anos:
    mask = nee_mask & (df["Ano de Ingresso"] == ano)
    nee_por_ano[ano] = df[mask].shape[0]

# Exibir resultados
print(f"Total de alunos de escola pública: {total_publicos}")
print(f"Alunos de escola pública com NEE: {publicos_com_nee}")
for ano in anos:
    print(f"Alunos com NEE ingressados em {ano}: {nee_por_ano[ano]}")