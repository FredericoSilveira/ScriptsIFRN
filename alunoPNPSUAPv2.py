import pandas as pd
from datetime import datetime
import re
import unicodedata

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

# Função para extrair elementos do primeiro elemento do Nome do Ciclo, removendo números e caracteres especiais
def extract_first_element(nome_do_ciclo):
    if pd.isna(nome_do_ciclo):  # Verifica se o valor é NaN
        return []
    # Divide o Nome do Ciclo por hífens e retorna o primeiro elemento
    elements = nome_do_ciclo.split('-')
    if len(elements) > 0:
        first_element = elements[0].strip()
        # Remove números ou strings que representam números
        cleaned_element = re.sub(r'\d+', '', first_element).strip()
        # Remove caracteres especiais, mantendo letras (inclusive acentuadas), números e espaços
        cleaned_element = re.sub(r'[^\w\sáéíóúãõçÁÉÍÓÚÃÕÇ]', '', cleaned_element).strip()
        # Divide o primeiro elemento em palavras individuais
        words = [normalize_string(word.strip()) for word in cleaned_element.split() if word.strip()]
        return words
    return []

# Solicitar ao operador o nome do campus a ser analisado
campus_selecionado = input("Informe o nome do campus para análise: ").strip().upper()

# Leitura e normalização do SUAP (fixando codificação utf-8)
suap_df = pd.read_csv(f"{path}SUAP.csv", dtype=str, encoding='utf-8', sep=',')
suap_df.columns = [normalize_string(col) for col in suap_df.columns]  # Normalizar nomes das colunas
suap_df.rename(columns={'MATRICULA': 'MATRICULASUAP'}, inplace=True)

# Filtrar apenas os registros do campus selecionado
suap_df = suap_df[suap_df['CAMPUS'].str.strip().str.upper() == campus_selecionado]

# Verificar se a coluna 'DATA DE MATRICULA' existe
if 'DATA DE MATRICULA' not in suap_df.columns:
    raise KeyError("A coluna 'DATA DE MATRICULA' não foi encontrada no arquivo SUAP. Verifique o nome da coluna.")

# Normalizar Data de Matrícula para datetime com formato explícito
suap_df['DATA_DE_MATRICULA'] = pd.to_datetime(suap_df['DATA DE MATRICULA'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

# Normalizar NOME, DESCRICAO DO CURSO e CPF no SUAP
suap_df['NOME_NORMALIZADO'] = suap_df['NOME'].apply(normalize_string)
suap_df['DESCRICAO_CURSO_NORMALIZADA'] = suap_df['DESCRICAO DO CURSO'].apply(normalize_string)
suap_df['CPF_NORMALIZADO'] = suap_df['CPF'].apply(normalize_cpf)

# Remover registros com valores ausentes nas colunas de merge
suap_df = suap_df.dropna(subset=['CPF_NORMALIZADO', 'NOME_NORMALIZADO'])

# Leitura e normalização do PNP (fixando codificação ISO-8859-1)
pnp_df = pd.read_csv(f"{path}PNP.csv", dtype=str, encoding='ISO-8859-1', sep=';')
pnp_df.columns = [normalize_string(col) for col in pnp_df.columns]  # Normalizar nomes das colunas
pnp_df.rename(columns={'MATRICULA': 'MATRICULASISTEC'}, inplace=True)

# Normalizar NOME, NOME DO CICLO e CPF no PNP
pnp_df['NOME_NORMALIZADO'] = pnp_df['NOME'].apply(normalize_string)
pnp_df['NOME_DO_CICLO_NORMALIZADO'] = pnp_df['NOME DO CICLO'].apply(normalize_string)
pnp_df['CPF_NORMALIZADO'] = pnp_df['CPF'].apply(normalize_cpf)

# Extrair elementos do primeiro elemento do Nome do Ciclo
pnp_df['ELEMENTOS_PRIMEIRO_ELEMENTO'] = pnp_df['NOME DO CICLO'].apply(extract_first_element)

# Converter ELEMENTOS_PRIMEIRO_ELEMENTO em uma string para permitir a detecção de duplicatas
pnp_df['ELEMENTOS_PRIMEIRO_ELEMENTO_STR'] = pnp_df['ELEMENTOS_PRIMEIRO_ELEMENTO'].apply(lambda x: " ".join(x))

# Identificar registros duplicados no PNP (mesmo CPF e ELEMENTOS_PRIMEIRO_ELEMENTO_STR)
pnp_df['DUPLICADO'] = pnp_df.duplicated(subset=['CPF_NORMALIZADO', 'ELEMENTOS_PRIMEIRO_ELEMENTO_STR'], keep=False)

# Registrar no log a detecção de duplicatas
for _, row in pnp_df[pnp_df['DUPLICADO']].iterrows():
    log_message(f"Duplicidade detectada: Estudante: {row['NOME_NORMALIZADO']} (CPF: {row['CPF_NORMALIZADO']}), Curso: {row['ELEMENTOS_PRIMEIRO_ELEMENTO_STR']}")

# Remover registros com valores ausentes nas colunas de merge
pnp_df = pnp_df.dropna(subset=['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'ELEMENTOS_PRIMEIRO_ELEMENTO'])

# Merge com validação de período e ano de ingresso
merged = pd.merge(
    suap_df,
    pnp_df,
    how='inner',  # Testar com inner para verificar correspondências
    left_on=['CPF_NORMALIZADO', 'NOME_NORMALIZADO'],
    right_on=['CPF_NORMALIZADO', 'NOME_NORMALIZADO'],
    suffixes=('', '_pnp'),
    indicator=True
)

# Filtrar registros onde o ano do ciclo (PNP) corresponde ao ano de ingresso (SUAP)
merged['ANO_VALIDO'] = merged.apply(
    lambda row: (
        log_message(f"\n--- Estudante: {row['NOME_NORMALIZADO']} (CPF: {row['CPF_NORMALIZADO']}) ---") or
        log_message(f"Ano do ciclo (PNP): {row['ANO DO CICLO']}") or
        log_message(f"Ano de ingresso (SUAP): {row['ANO DE INGRESSO']}") or
        log_message(f"Validação de ano: {int(row['ANO DO CICLO']) == int(row['ANO DE INGRESSO'])}") or
        (int(row['ANO DO CICLO']) == int(row['ANO DE INGRESSO']))
    ),
    axis=1
)

# Adicionar validação de nome do curso com logs detalhados
merged['CURSO_VALIDO'] = merged.apply(
    lambda row: (
        log_message(f"Elementos do primeiro elemento do ciclo: {row['ELEMENTOS_PRIMEIRO_ELEMENTO']}") or
        log_message(f"Descrição do curso (SUAP): {row['DESCRICAO_CURSO_NORMALIZADA']}") or
        log_message(f"Comparação de elementos: {all(element in row['DESCRICAO_CURSO_NORMALIZADA'] for element in row['ELEMENTOS_PRIMEIRO_ELEMENTO'])}") or
        all(element in row['DESCRICAO_CURSO_NORMALIZADA'] for element in row['ELEMENTOS_PRIMEIRO_ELEMENTO'])  # Verifica se todos os elementos estão presentes
    ),
    axis=1
)

# Filtrar registros onde o ano e a data de matrícula são válidos
merged['VALID_PERIOD'] = merged.apply(
    lambda row: (
        log_message(f"Data de matrícula (SUAP): {row['DATA_DE_MATRICULA']}") or
        log_message(f"Validação de período: {(row['DATA_DE_MATRICULA'].year == int(row['ANO DE INGRESSO']))}") or
        (row['DATA_DE_MATRICULA'].year == int(row['ANO DE INGRESSO']))
    ),
    axis=1
)

# Separar registros duplicados para o arquivo "ciclos_duplicados.csv"
ciclos_duplicados = merged[merged['DUPLICADO']]
output_ciclos_duplicados = ciclos_duplicados[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'MATRICULASUAP', 'MATRICULASISTEC', 'ANO DO CICLO', 'NOME DO CICLO']]
output_ciclos_duplicados.to_csv(f"{path}ciclos_duplicados.csv", index=False)

# Geração dos arquivos de saída (excluindo duplicados)
correlated = merged[(merged['_merge'] == 'both') & (merged['ANO_VALIDO']) & (merged['CURSO_VALIDO']) & (merged['VALID_PERIOD']) & (~merged['DUPLICADO'])]

# Verificar se as colunas necessárias existem antes de gerar o arquivo
required_columns = ['MATRICULASUAP', 'MATRICULASISTEC']
missing_columns = [col for col in required_columns if col not in correlated.columns]

if missing_columns:
    log_message(f"Colunas ausentes no DataFrame 'correlated': {missing_columns}")
    raise KeyError(f"Colunas ausentes no DataFrame 'correlated': {missing_columns}")

output_correlated = correlated[['MATRICULASUAP', 'MATRICULASISTEC']].rename(
    columns={'MATRICULASUAP': 'MATRICULA', 'MATRICULASISTEC': 'CODIGO_ALUNO'}
)
output_correlated.to_csv(f"{path}correlated.csv", index=False)

sem_cor = merged[(merged['_merge'] == 'left_only') | (~merged['CURSO_VALIDO']) | (~merged['VALID_PERIOD'])]
output_sem_cor = sem_cor[['CPF_NORMALIZADO', 'NOME_NORMALIZADO', 'MATRICULASUAP']]
output_sem_cor.to_csv(f"{path}SEM_COR.csv", index=False)

# Finalizar o log
log_message("\nProcesso de depuração concluído.")