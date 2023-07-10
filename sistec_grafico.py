import matplotlib.pyplot as plt
import pandas as pd

# Definindo variáveis
input_file = "/Users/fred/Downloads/CSV/input.csv"
ano_evasao = 2022
data_limite_retidos = "2023-01-01 00:00:00"

# Lendo o arquivo CSV
df = pd.read_csv(input_file)

# Calculando o total de alunos em curso com status “EM_CURSO” na coluna “NO_STATUS_MATRICULA”
total_em_curso = len(df[df["NO_STATUS_MATRICULA"] == "EM_CURSO"])

# Calculando o total de alunos retidos que estão “EM_CURSO” e que em ”DT_DATA_FIM_PREVISTO” é menor que “2023-01-01 00:00:00”
total_retidos = len(df[(df["NO_STATUS_MATRICULA"] == "EM_CURSO") & (df["DT_DATA_FIM_PREVISTO"] < data_limite_retidos)])

# Calculando os alunos com o status "ABANDONO" que ocorreram no ano de 2022 quando analisado a coluna "MES_DE_OCORRENCIA”. Esses alunos serão considerados evadidos.
total_evasao = len(df[(df["NO_STATUS_MATRICULA"] == "ABANDONO") & (df["MES_DE_OCORRENCIA"].str.contains(str(ano_evasao)))])
total_em_curso_por_campus = df[df["NO_STATUS_MATRICULA"] == "EM_CURSO"].groupby("CAMPUS").size()
total_retidos_por_campus = df[(df["NO_STATUS_MATRICULA"] == "EM_CURSO") & (df["DT_DATA_FIM_PREVISTO"] < data_limite_retidos)].groupby("CAMPUS").size()
total_evasao_por_campus = df[(df["NO_STATUS_MATRICULA"] == "ABANDONO") & (df["MES_DE_OCORRENCIA"].str.contains(str(ano_evasao)))].groupby("CAMPUS").size()

# Gerando gráficos
plt.figure(figsize=(10, 5))
plt.bar(total_em_curso_por_campus.index, total_em_curso_por_campus.values)
plt.title("Quantitativo dos alunos EM_CURSO por campus")
plt.xlabel("Campus")
plt.ylabel("Quantidade")
for i in range(len(total_em_curso_por_campus)):
    plt.annotate(str(total_em_curso_por_campus.values[i]), xy=(i, total_em_curso_por_campus.values[i]), ha='center', va='bottom')
plt.show()

plt.figure(figsize=(10, 5))
plt.bar(total_retidos_por_campus.index, total_retidos_por_campus.values)
plt.title("Quantitativo dos alunos retidos por campus")
plt.xlabel("Campus")
plt.ylabel("Quantidade")
for i in range(len(total_retidos_por_campus)):
    plt.annotate(str(total_retidos_por_campus.values[i]), xy=(i, total_retidos_por_campus.values[i]), ha='center', va='bottom')
plt.show()

plt.figure(figsize=(10, 5))
plt.bar(total_evasao_por_campus.index, total_evasao_por_campus.values)
plt.title("Quantitativo dos alunos evadidos por campus")
plt.xlabel("Campus")
plt.ylabel("Quantidade")
for i in range(len(total_evasao_por_campus)):
    plt.annotate(str(total_evasao_por_campus.values[i]), xy=(i, total_evasao_por_campus.values[i]), ha='center', va='bottom')
plt.show()

total_em_curso_percentual_por_campus = total_em_curso_por_campus / total_em_curso * 100
total_retidos_percentual_por_campus = total_retidos_por_campus / total_retidos * 100
total_evasao_percentual_por_campus = total_evasao_por_campus / total_evasao * 100

plt.figure(figsize=(10, 5))
plt.pie(total_em_curso_percentual_por_campus.values, labels=total_em_curso_percentual_por_campus.index, autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Percentual dos alunos EM_CURSO por campus")
plt.show()

plt.figure(figsize=(10, 5))
plt.pie(total_retidos_percentual_por_campus.values, labels=total_retidos_percentual_por_campus.index, autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Percentual dos alunos retidos por campus")
plt.show()

plt.figure(figsize=(10, 5))
plt.pie(total_evasao_percentual_por_campus.values, labels=total_evasao_percentual_por_campus.index, autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Percentual dos alunos evadidos por campus")
plt.show()

print(f"Total de alunos em curso: {total_em_curso}")
print(f"Total de alunos retidos: {total_retidos}")
print(f"Total de evasão: {total_evasao}")
print(f"Total de alunos em curso por campus:\n{total_em_curso_por_campus}")
print(f"Total de alunos retidos por campus:\n{total_retidos_por_campus}")
print(f"Total de alunos evadidos por campus:\n{total_evasao_por_campus}")
print(f"Percentual de alunos em curso por campus:\n{total_em_curso_percentual_por_campus}")
print(f"Percentual de alunos retidos por campus:\n{total_retidos_percentual_por_campus}")
print(f"Percentual de alunos evadidos por campus:\n{total_evasao_percentual_por_campus}")