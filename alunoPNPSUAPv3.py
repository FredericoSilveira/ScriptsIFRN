import pandas as pd
from datetime import datetime
import re
import unicodedata
import os

path = "/Users/fred/Downloads/"

# Configurar o arquivo de log
log_file_path = f"{path}debug.log"
with open(log_file_path, 'w', encoding='utf-8') as log_file:
    log_file.write("Iniciando processo de depuração...\n")

# Função para registrar logs no arquivo
def log_message(message):
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{message}\n")

# Função para normalizar strings (remover acentos, converter para maiúsculas e remover espaços extras)
def normalize_string(value):
    if pd.isna(value):  # Verifica se o valor é NaN
        return ""
    # Remove acentos, converte para maiúsculas e remove espaços extras
    normalized = unicodedata.normalize('NFKD', str(value)).encode('ascii', errors='ignore').decode('utf-8')
    # Garantir que espaços múltiplos sejam reduzidos a um único espaço
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized.upper()

# Função para normalizar CPF (remover pontos e traços)
def normalize_cpf(value):
    if pd.isna(value):  # Verifica se o valor é NaN
        return ""
    # Remove pontos, traços e espaços
    normalized = re.sub(r'[.-]', '', str(value)).strip()
    return normalized

# Leitura e normalização do SUAP (fixando codificação utf-8)
suap_df = pd.read_csv(f"{path}SUAP.csv", dtype=str, encoding='utf-8', sep=',')
suap_df.columns = [normalize_string(col) for col in suap_df.columns]  # Normalizar nomes das colunas
suap_df.rename(columns={'MATRICULA': 'MATRICULASUAP', 'DATA DE MATRICULA': 'DATA_DE_MATRICULA'}, inplace=True)

# Verificar se as colunas necessárias existem no SUAP
required_columns_suap = ['MATRICULASUAP', 'NOME', 'ANO DE INGRESSO', 'CPF', 'CAMPUS', 'CODIGO CURSO', 'DATA_DE_MATRICULA', 'DESCRICAO DO CURSO']
missing_columns_suap = [col for col in required_columns_suap if col not in suap_df.columns]
if missing_columns_suap:
    raise KeyError(f"As seguintes colunas estão faltando no arquivo SUAP: {', '.join(missing_columns_suap)}.")[[1]]

# Normalizar Data de Matrícula para datetime com formato explícito
suap_df['DATA_DE_MATRICULA'] = pd.to_datetime(suap_df['DATA_DE_MATRICULA'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

# Normalizar NOME, DESCRICAO DO CURSO e CPF no SUAP
suap_df['NOME_NORMALIZADO'] = suap_df['NOME'].apply(normalize_string)
suap_df['DESCRICAO_CURSO_NORMALIZADA'] = suap_df['DESCRICAO DO CURSO'].apply(normalize_string)
suap_df['CPF_NORMALIZADO'] = suap_df['CPF'].apply(normalize_cpf)

# Detectar registros com ANO DE INGRESSO vazio no SUAP
suap_df['ANO_INGRESSO_VAZIO'] = suap_df['ANO DE INGRESSO'].apply(lambda ano: ano == "" or pd.isna(ano))
registros_sem_ano_suap = suap_df[suap_df['ANO_INGRESSO_VAZIO']]
suap_df = suap_df[~suap_df['ANO_INGRESSO_VAZIO']]  # Remover registros com ANO DE INGRESSO vazio

# Salvar registros sem ANO DE INGRESSO do SUAP em um arquivo separado
if not registros_sem_ano_suap.empty:
    registros_sem_ano_suap[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'MATRICULASUAP']].to_csv(
        f"{path}sem_ano_suap.csv", index=False, sep=';'
    )
    log_message(f"Registros sem ANO DE INGRESSO salvos em 'sem_ano_suap.csv'.")

# Solicitar ao operador o diretório dos arquivos PNP
pnp_directory = input("Informe o diretório onde estão os arquivos PNP: ").strip()
if not os.path.isdir(pnp_directory):
    raise ValueError(f"O diretório '{pnp_directory}' não existe ou não é válido.")[[2]]

# Listar todos os arquivos PNP no diretório
pnp_files = [f for f in os.listdir(pnp_directory) if f.endswith('.csv')]
if not pnp_files:
    raise ValueError(f"Nenhum arquivo PNP encontrado no diretório '{pnp_directory}'.")[[2]]

log_message(f"Arquivos PNP encontrados: {', '.join(pnp_files)}")

# Processar cada arquivo PNP individualmente
for pnp_file in pnp_files:
    pnp_file_path = os.path.join(pnp_directory, pnp_file)
    campus_selecionado = input(f"Informe o nome do campus para o arquivo '{pnp_file}': ").strip().upper()

    # Verificar se o campus selecionado existe no DataFrame do SUAP
    campus_disponiveis = suap_df['CAMPUS'].str.strip().str.upper().unique()
    if campus_selecionado not in campus_disponiveis:
        log_message(f"Erro: O campus '{campus_selecionado}' não foi encontrado no arquivo SUAP. Campi disponíveis: {', '.join(campus_disponiveis)}.")
        continue  # Pula para o próximo arquivo PNP

    # Leitura e normalização do PNP (fixando codificação ISO-8859-1)
    pnp_df = pd.read_csv(pnp_file_path, dtype=str, encoding='ISO-8859-1', sep=';')
    pnp_df.columns = [normalize_string(col) for col in pnp_df.columns]  # Normalizar nomes das colunas
    pnp_df.rename(columns={'MATRICULA': 'MATRICULASISTEC'}, inplace=True)

    # Verificar se as colunas necessárias existem no PNP
    required_columns_pnp = ['CPF', 'MATRICULASISTEC', 'NOME', 'ANO DO CICLO', 'NOME DO CICLO']
    missing_columns_pnp = [col for col in required_columns_pnp if col not in pnp_df.columns]
    if missing_columns_pnp:
        raise KeyError(f"As seguintes colunas estão faltando no arquivo PNP '{pnp_file}': {', '.join(missing_columns_pnp)}.")[[1]]

    # Normalizar NOME e CPF no PNP
    pnp_df['NOME_NORMALIZADO'] = pnp_df['NOME'].apply(normalize_string)
    pnp_df['CPF_NORMALIZADO'] = pnp_df['CPF'].apply(normalize_cpf)

    # Detectar CPFs vazios ou zerados no PNP
    pnp_df['CPF_VAZIO_OU_ZERADO'] = pnp_df['CPF_NORMALIZADO'].apply(lambda cpf: cpf == "" or cpf == "0" * len(cpf))
    registros_sem_cpf_pnp = pnp_df[pnp_df['CPF_VAZIO_OU_ZERADO']]
    pnp_df = pnp_df[~pnp_df['CPF_VAZIO_OU_ZERADO']]  # Remover registros com CPFs inválidos

    # Salvar registros sem CPF do PNP em um arquivo separado
    if not registros_sem_cpf_pnp.empty:
        registros_sem_cpf_pnp[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'MATRICULASISTEC']].to_csv(
            f"{path}sem_cpf_pnp_{campus_selecionado}.csv", index=False, sep=';'
        )
        log_message(f"Registros sem CPF salvos em 'sem_cpf_pnp_{campus_selecionado}.csv'.")

    # Detectar registros com ANO DO CICLO vazio no PNP
    pnp_df['ANO_CICLO_VAZIO'] = pnp_df['ANO DO CICLO'].apply(lambda ano: ano == "" or pd.isna(ano))
    registros_sem_ano_pnp = pnp_df[pnp_df['ANO_CICLO_VAZIO']]
    pnp_df = pnp_df[~pnp_df['ANO_CICLO_VAZIO']]  # Remover registros com ANO DO CICLO vazio

    # Salvar registros sem ANO DO CICLO do PNP em um arquivo separado
    if not registros_sem_ano_pnp.empty:
        registros_sem_ano_pnp[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'MATRICULASISTEC']].to_csv(
            f"{path}sem_ano_pnp_{campus_selecionado}.csv", index=False, sep=';'
        )
        log_message(f"Registros sem ANO DO CICLO salvos em 'sem_ano_pnp_{campus_selecionado}.csv'.")

    # Filtrar apenas os registros do campus selecionado no SUAP
    suap_filtered_df = suap_df[suap_df['CAMPUS'].str.strip().str.upper() == campus_selecionado]

    # Debug: Exibir amostras dos dados antes do merge
    log_message(f"Dados filtrados do SUAP para o campus '{campus_selecionado}':")
    log_message(suap_filtered_df[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'ANO DE INGRESSO']].head().to_string())

    log_message(f"Dados do PNP antes do merge:")
    log_message(pnp_df[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'ANO DO CICLO']].head().to_string())

    # Merge com validação de período e ano de ingresso
    merged = pd.merge(
        suap_filtered_df,
        pnp_df,
        how='inner',
        left_on=['CPF_NORMALIZADO', 'NOME_NORMALIZADO'],
        right_on=['CPF_NORMALIZADO', 'NOME_NORMALIZADO'],
        suffixes=('', '_pnp'),
        indicator=True
    )

    # Log para verificar o resultado do merge
    log_message(f"Resultado do merge para o campus '{campus_selecionado}': {len(merged)} registros combinados.")
    if merged.empty:
        log_message("Erro: O merge resultou em um DataFrame vazio. Verifique as colunas usadas para o merge e os dados normalizados.")
        continue  # Pula para o próximo arquivo PNP

    # Função para validar o ano com logs detalhados
    def validar_ano(row):
        try:
            log_message(f"\n--- Estudante: {row['NOME_NORMALIZADO']} (CPF: {row['CPF_NORMALIZADO']}) ---")
            log_message(f"Ano do ciclo (PNP): {row['ANO DO CICLO']}")
            log_message(f"Ano de ingresso (SUAP): {row['ANO DE INGRESSO']}")

            # Verificar se as colunas existem e são numéricas
            if pd.isna(row['ANO DO CICLO']) or pd.isna(row['ANO DE INGRESSO']):
                log_message("Erro: Ano do ciclo ou Ano de ingresso está vazio.")
                return False

            ano_ciclo = int(row['ANO DO CICLO'])
            ano_ingresso = int(row['ANO DE INGRESSO'])

            log_message(f"Validação de ano: {ano_ciclo == ano_ingresso}")
            return ano_ciclo == ano_ingresso
        except Exception as e:
            log_message(f"Erro ao validar ano: {e}")
            return False

    # Aplicar a função de validação de ano
    merged['ANO_VALIDO'] = merged.apply(validar_ano, axis=1)

    # Separar registros duplicados para o arquivo "ciclos_duplicados_{campus}.csv"
    ciclos_duplicados = merged[merged.duplicated(subset=['CPF_NORMALIZADO', 'NOME_NORMALIZADO'], keep=False)]
    output_ciclos_duplicados = ciclos_duplicados[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'MATRICULASUAP', 'MATRICULASISTEC', 'ANO DO CICLO', 'NOME DO CICLO']]
    output_ciclos_duplicados.to_csv(f"{path}ciclos_duplicados_{campus_selecionado}.csv", index=False, sep=';')  # Usar ';' como separador [[1]]

    # Geração dos arquivos de saída (excluindo duplicados)
    correlated = merged[(merged['_merge'] == 'both') & (merged['ANO_VALIDO'])]
    output_correlated = correlated[['MATRICULASUAP', 'MATRICULASISTEC']].rename(
        columns={'MATRICULASUAP': 'MATRICULA', 'MATRICULASISTEC': 'CODIGO_ALUNO'}
    )
    output_correlated.to_csv(f"{path}correlated_{campus_selecionado}.csv", index=False, sep=';')  # Usar ';' como separador [[1]]

    sem_cor = merged[(merged['_merge'] == 'left_only') | (~merged['ANO_VALIDO'])]
    output_sem_cor = sem_cor[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'MATRICULASUAP']]
    output_sem_cor.to_csv(f"{path}SEM_COR_{campus_selecionado}.csv", index=False, sep=';')  # Usar ';' como separador [[1]]

# Finalizar o log
log_message("\nProcesso de depuração concluído.")