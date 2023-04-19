import os
import csv

# definindo a pasta com os arquivos CSV
pasta_csv = "/Users/fred/Downloads/CSV"

# definindo as colunas que serão mantidas no arquivo de saída
colunas_saida = ["NO_ALUNO", "NU_CPF", "DT_DATA_INICIO", "DT_DATA_FIM_PREVISTO",
                 "NO_CICLO_MATRICULA", "NO_STATUS_MATRICULA", "MES_DE_OCORRENCIA", "CAMPUS"]

# inicializando a lista de dados que será escrita no arquivo de saída
dados_saida = []

# percorrendo todos os arquivos da pasta e lendo os dados
for nome_arquivo in os.listdir(pasta_csv):
    if nome_arquivo.endswith(".csv"):
        # removendo a extensão do nome do arquivo
        nome_arquivo = os.path.splitext(nome_arquivo)[0]
        caminho_arquivo = os.path.join(pasta_csv, nome_arquivo + ".csv")
        with open(caminho_arquivo, 'r', encoding='iso-8859-1') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv, delimiter=';')
            for linha in leitor_csv:
                # selecionando apenas as colunas de interesse
                linha_saida = {chave: valor for chave, valor in linha.items() if chave in colunas_saida[:-1]}
                # adicionando a coluna CAMPUS
                linha_saida["CAMPUS"] = os.path.splitext(nome_arquivo)[0]
                # adicionando a linha de dados à lista de saída
                dados_saida.append(linha_saida)

# escrevendo os dados no arquivo de saída
with open("/Users/fred/Downloads/CSV/arquivo_saida.csv", "w", newline="") as arquivo_saida:
    escritor_csv = csv.DictWriter(arquivo_saida, fieldnames=colunas_saida)
    escritor_csv.writeheader()
    for linha in dados_saida:
        escritor_csv.writerow(linha)

