import pandas as pd
import re
import numpy as np

# --- Configuração dos Nomes de Arquivos e Caminhos ---
# Por favor, certifique-se de que este caminho está correto.
PATH_BASE = "/Users/fred/Downloads/"

ARQUIVO_SUAP = PATH_BASE + "Relatorio-tec.xls"
ARQUIVO_SGP = PATH_BASE + "planilha-movimentacao-conclusao-matricula-pre-preenchida-rede-223254_2024_1-1 (1).xlsx"
ARQUIVO_SAIDA = PATH_BASE + "SGP_dados_atualizados_com_SUAP_sem_data.xlsx"  # Nome do arquivo de saída alterado

# --- Configuração dos Nomes das Colunas ---
# ATENÇÃO: Verifique e ajuste os nomes das colunas do arquivo SUAP conforme necessário!
# Coluna CPF no arquivo SUAP
NOME_COLUNA_CPF_SUAP = 'CPF'
# Coluna que indica a situação do aluno no curso (Ex: Matriculado, Transferido Externo, Jubilado)
NOME_COLUNA_SITUACAO_CURSO_SUAP = 'Situação no Curso'  # Exemplo, pode ser 'Situação', 'Status do Aluno', etc.
# Coluna que indica a situação do aluno no período (Ex: Aprovado)
NOME_COLUNA_SITUACAO_PERIODO_SUAP = 'Situação no Período'  # Exemplo, pode ser 'Status Período', etc.
# A COLUNA DE DATA DO SUAP NÃO É MAIS USADA PARA PREENCHER A PLANILHA SGP
# NOME_COLUNA_DATA_EVENTO_SUAP = 'Data da Situação' # REMOVIDO

# Colunas no arquivo SGP
NOME_COLUNA_CPF_SGP = 'ESTUDANTE_CPF'
NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP = 'MATRICULA_SITUACAO_FINAL'
NOME_COLUNA_DATA_FIM_APROVACAO_SGP = 'DATA_FIM_OU_APROVACAO'  # Esta coluna não será preenchida pelo script


# --- Função para Limpar CPF ---
def limpar_cpf(cpf):
    """Remove caracteres não numéricos de um CPF."""
    if pd.isna(cpf):
        return None
    cpf_str = str(cpf)
    # Remove todos os caracteres que não são dígitos
    cpf_limpo = re.sub(r'\D', '', cpf_str)
    return cpf_limpo


# --- Início do Script ---
print("Iniciando o processamento das planilhas...")

try:
    # --- 1. Carregar os Dados ---
    print(f"Carregando dados do SUAP: {ARQUIVO_SUAP}")
    df_suap = pd.read_excel(ARQUIVO_SUAP)
    print("Dados do SUAP carregados com sucesso.")

    print(f"Carregando dados do SGP: {ARQUIVO_SGP}")
    df_sgp = pd.read_excel(ARQUIVO_SGP, engine='openpyxl')
    print("Dados do SGP carregados com sucesso.")

    colunas_originais_sgp = list(df_sgp.columns)

    # --- 2. Limpar CPFs ---
    print("Limpando CPFs...")
    if NOME_COLUNA_CPF_SUAP not in df_suap.columns:
        raise ValueError(
            f"Coluna CPF '{NOME_COLUNA_CPF_SUAP}' não encontrada no arquivo SUAP. Verifique NOME_COLUNA_CPF_SUAP.")
    df_suap['CPF_LIMPO'] = df_suap[NOME_COLUNA_CPF_SUAP].apply(limpar_cpf)

    if NOME_COLUNA_CPF_SGP not in df_sgp.columns:
        raise ValueError(
            f"Coluna CPF '{NOME_COLUNA_CPF_SGP}' não encontrada no arquivo SGP. Verifique NOME_COLUNA_CPF_SGP.")
    df_sgp['CPF_LIMPO'] = df_sgp[NOME_COLUNA_CPF_SGP].apply(limpar_cpf)
    print("CPFs limpos.")

    # Verificar se as colunas de situação do SUAP existem
    colunas_suap_necessarias = [NOME_COLUNA_SITUACAO_CURSO_SUAP,
                                NOME_COLUNA_SITUACAO_PERIODO_SUAP]  # Removida coluna de data
    for col in colunas_suap_necessarias:
        if col not in df_suap.columns:
            raise ValueError(
                f"Coluna '{col}' não encontrada no arquivo SUAP. Verifique as configurações de NOME_COLUNA_*_SUAP.")

    # --- 3. Preparar Colunas de Saída no DataFrame SGP ---
    if NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP not in df_sgp.columns:
        df_sgp[NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP] = pd.NA
    else:
        df_sgp[NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP] = pd.to_numeric(
            df_sgp[NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP], errors='coerce')

    # Garante que a coluna DATA_FIM_OU_APROVACAO exista e seja do tipo datetime, mas não será preenchida.
    if NOME_COLUNA_DATA_FIM_APROVACAO_SGP not in df_sgp.columns:
        df_sgp[NOME_COLUNA_DATA_FIM_APROVACAO_SGP] = pd.NaT
    else:
        df_sgp[NOME_COLUNA_DATA_FIM_APROVACAO_SGP] = pd.to_datetime(df_sgp[NOME_COLUNA_DATA_FIM_APROVACAO_SGP],
                                                                    errors='coerce')

    # --- 4. Cruzar Dados (Merge) ---
    # Selecionar apenas as colunas necessárias do SUAP para o merge
    df_suap_para_merge = df_suap[['CPF_LIMPO', NOME_COLUNA_SITUACAO_CURSO_SUAP,
                                  NOME_COLUNA_SITUACAO_PERIODO_SUAP]].copy()  # Removida coluna de data

    print("Cruzando dados do SGP com SUAP...")
    df_merged = pd.merge(df_sgp, df_suap_para_merge, on='CPF_LIMPO', how='left')
    print("Dados cruzados.")

    # --- 5. Aplicar Regras para Preencher MATRICULA_SITUACAO_FINAL ---
    print("Aplicando regras para preencher MATRICULA_SITUACAO_FINAL...")

    condicoes_situacao = [
        (df_merged[NOME_COLUNA_SITUACAO_CURSO_SUAP].notna()) & \
        (df_merged[NOME_COLUNA_SITUACAO_CURSO_SUAP].str.strip().str.lower() == 'matriculado') & \
        (df_merged[NOME_COLUNA_SITUACAO_PERIODO_SUAP].notna()) & \
        (df_merged[NOME_COLUNA_SITUACAO_PERIODO_SUAP].str.strip().str.lower() == 'aprovado'),

        (df_merged[NOME_COLUNA_SITUACAO_CURSO_SUAP].notna()) & \
        (df_merged[NOME_COLUNA_SITUACAO_CURSO_SUAP].str.strip().str.lower() == 'transferido externo'),

        (df_merged[NOME_COLUNA_SITUACAO_CURSO_SUAP].notna()) & \
        (df_merged[NOME_COLUNA_SITUACAO_CURSO_SUAP].str.strip().str.lower() == 'jubilado')
    ]

    valores_situacao = [10, 5, 12]

    df_merged[NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP] = np.select(
        condicoes_situacao,
        valores_situacao,
        default=df_merged[NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP]
    )

    # A COLUNA DATA_FIM_OU_APROVACAO_SGP NÃO É MAIS ATUALIZADA AQUI

    print("Regras para MATRICULA_SITUACAO_FINAL aplicadas.")

    # --- 6. Preparar DataFrame Final ---
    if NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP not in colunas_originais_sgp:
        colunas_originais_sgp.append(NOME_COLUNA_MATRICULA_SITUACAO_FINAL_SGP)
    # Garante que a coluna de data esteja na lista se foi criada agora, mas seus valores são os originais ou NaT.
    if NOME_COLUNA_DATA_FIM_APROVACAO_SGP not in colunas_originais_sgp:
        colunas_originais_sgp.append(NOME_COLUNA_DATA_FIM_APROVACAO_SGP)

    colunas_para_manter = [col for col in colunas_originais_sgp if col in df_merged.columns]

    df_final = df_merged[colunas_para_manter]

    # --- 7. Salvar Resultado ---
    print(f"Salvando planilha resultante em: {ARQUIVO_SAIDA}")
    df_final.to_excel(ARQUIVO_SAIDA, index=False, engine='openpyxl')
    print("Planilha salva com sucesso!")
    print(f"O arquivo '{ARQUIVO_SAIDA}' foi gerado no diretório '{PATH_BASE}'.")

except FileNotFoundError as e:
    print(f"Erro: Arquivo não encontrado. Detalhes: {e}")
    print("Por favor, verifique se os nomes dos arquivos e o caminho PATH_BASE estão corretos.")
except ValueError as e:
    print(f"Erro nos dados ou configuração: {e}")
    print("Verifique os nomes das colunas configuradas no script e a estrutura dos seus arquivos Excel.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
    print("Verifique os detalhes do erro e tente novamente.")

