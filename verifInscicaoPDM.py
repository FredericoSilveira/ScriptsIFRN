import pandas as pd
import re
import os

# --- Configurações Iniciais ---
CAMINHO_DOWNLOADS = "/Users/fred/Downloads"
ARQUIVO_SUAP = "Relatorio-tec-mat.xls"
ARQUIVO_PE_DE_MEIA = "status-estudante-programa-EMR-rede-223254_1-2025.xlsx"
ARQUIVO_SAIDA = "planilha_nao_detectados_v3.xlsx"  # Nome de arquivo de saída alterado para evitar sobrescrever

# Caminhos completos para os arquivos
caminho_suap = os.path.join(CAMINHO_DOWNLOADS, ARQUIVO_SUAP)
caminho_pe_de_meia = os.path.join(CAMINHO_DOWNLOADS, ARQUIVO_PE_DE_MEIA)
caminho_saida = os.path.join(CAMINHO_DOWNLOADS, ARQUIVO_SAIDA)


# --- Funções Auxiliares ---
def limpar_e_validar_cpf(cpf):
    """
    Limpa o CPF removendo caracteres não numéricos e valida se possui 11 dígitos.
    Retorna o CPF limpo com 11 dígitos ou None caso contrário.
    """
    if pd.isna(cpf):
        return None

    # Garantir que o CPF seja tratado como string para a limpeza
    cpf_str = str(cpf)

    # Remover todos os caracteres não numéricos
    cpf_limpo = re.sub(r'\D', '', cpf_str)

    # Validar se o CPF limpo tem 11 dígitos
    if len(cpf_limpo) == 11:
        return cpf_limpo
    else:
        # print(f"Debug: CPF '{cpf_str}' (limpo: '{cpf_limpo}') invalidado por não ter 11 dígitos.") # Log opcional
        return None


# --- Leitura e Processamento das Planilhas ---
try:
    print(f"Iniciando a leitura da planilha SUAP: {caminho_suap}")
    try:
        df_suap = pd.read_excel(caminho_suap, engine='xlrd', dtype={'CPF': str})  # Ler CPF como string
    except Exception as e_xls:
        print(f"Erro ao ler arquivo .xls com xlrd: {e_xls}. Tentando com o engine padrão.")
        df_suap = pd.read_excel(caminho_suap, dtype={'CPF': str})  # Ler CPF como string

    print(f"Colunas da planilha SUAP: {df_suap.columns.tolist()}")

    if 'CPF' not in df_suap.columns:
        raise ValueError("A coluna 'CPF' não foi encontrada na planilha SUAP. Verifique os nomes das colunas.")

    # Guardar CPF original e aplicar limpeza e validação
    df_suap['CPF_original'] = df_suap['CPF']
    df_suap['CPF_processado'] = df_suap['CPF'].apply(limpar_e_validar_cpf)

    # Diagnóstico SUAP
    total_suap = len(df_suap)
    validos_suap = df_suap['CPF_processado'].notna().sum()
    invalidos_suap = total_suap - validos_suap
    print(f"\nDiagnóstico SUAP:")
    print(f"  Total de registros: {total_suap}")
    print(f"  CPFs válidos (11 dígitos após limpeza): {validos_suap}")
    print(f"  CPFs inválidos ou não preenchidos: {invalidos_suap}")
    if invalidos_suap > 0:
        print("  Exemplos de CPFs originais que resultaram em inválidos/nulos no SUAP (primeiros 5):")
        print(df_suap[df_suap['CPF_processado'].isna()]['CPF_original'].head())

    print(f"\nIniciando a leitura da planilha Pé de Meia: {caminho_pe_de_meia}")
    df_pe_de_meia = pd.read_excel(caminho_pe_de_meia, header=1, dtype={'CPF': str})  # Ler CPF como string
    print(f"Colunas da planilha Pé de Meia: {df_pe_de_meia.columns.tolist()}")

    if 'CPF' not in df_pe_de_meia.columns:
        raise ValueError("A coluna 'CPF' não foi encontrada na planilha Pé de Meia. Verifique os nomes das colunas.")

    df_pe_de_meia['CPF_processado'] = df_pe_de_meia['CPF'].apply(limpar_e_validar_cpf)

    # Diagnóstico Pé de Meia
    total_pdm = len(df_pe_de_meia)
    validos_pdm = df_pe_de_meia['CPF_processado'].notna().sum()
    invalidos_pdm = total_pdm - validos_pdm
    print(f"\nDiagnóstico Pé de Meia:")
    print(f"  Total de registros: {total_pdm}")
    print(f"  CPFs válidos (11 dígitos após limpeza): {validos_pdm}")
    print(f"  CPFs inválidos ou não preenchidos: {invalidos_pdm}")
    if invalidos_pdm > 0:
        print("  Exemplos de CPFs originais que resultaram em inválidos/nulos no Pé de Meia (primeiros 5):")
        print(df_pe_de_meia[df_pe_de_meia['CPF_processado'].isna()]['CPF_original'].head())

    # --- Comparação usando MERGE ---
    print("\nComparando as planilhas usando MERGE com CPFs processados...")

    # Preparar o DataFrame do Pé de Meia para o merge
    # Selecionar apenas CPFs processados válidos e uma coluna indicadora
    df_pe_de_meia_subset = df_pe_de_meia[df_pe_de_meia['CPF_processado'].notna()][['CPF_processado', 'Nome']].copy()
    df_pe_de_meia_subset.rename(columns={'Nome': 'Nome_PDM'}, inplace=True)

    # Remover duplicatas de CPFs processados no Pé de Meia para evitar duplicação de linhas do SUAP
    df_pe_de_meia_subset.drop_duplicates(subset=['CPF_processado'], keep='first', inplace=True)

    print(f"  Número de CPFs únicos e válidos no Pé de Meia para merge: {len(df_pe_de_meia_subset)}")

    # Realizar um "left merge"
    df_merged = pd.merge(df_suap, df_pe_de_meia_subset, on='CPF_processado', how='left')

    # Alunos não detectados são aqueles para os quais 'Nome_PDM' é NaN após o merge
    # E também aqueles cujo CPF no SUAP foi invalidado (CPF_processado é None)
    # Mas focaremos nos que tinham CPF válido no SUAP mas não foram encontrados no PDM

    # Condição: CPF processado no SUAP era válido, mas não encontrou correspondência no PDM
    alunos_nao_detectados = df_merged[
        df_merged['CPF_processado'].notna() & df_merged['Nome_PDM'].isnull()
        ].copy()

    # Alunos cujo CPF no SUAP já era inválido (opcional, mas bom saber)
    alunos_suap_cpf_invalido = df_suap[df_suap['CPF_processado'].isna()].copy()
    print(f"  Número de alunos no SUAP com CPF originalmente inválido/não processável: {len(alunos_suap_cpf_invalido)}")

    # --- Preparação e Salvamento do Resultado ---
    print(f"\nTotal de alunos na planilha SUAP: {total_suap}")
    print(
        f"Total de alunos não detectados na planilha Pé de Meia (tinham CPF válido no SUAP mas não encontrados no PDM): {len(alunos_nao_detectados)}")

    # Selecionar colunas para o arquivo de saída
    colunas_saida_base = ['Matrícula', 'Nome', 'CPF_original', 'Situação no Curso', 'CPF_processado']
    colunas_saida_existentes = [col for col in colunas_saida_base if col in alunos_nao_detectados.columns]

    alunos_nao_detectados_saida = alunos_nao_detectados[colunas_saida_existentes]

    if 'CPF_original' in alunos_nao_detectados_saida.columns:
        alunos_nao_detectados_saida = alunos_nao_detectados_saida.rename(columns={'CPF_original': 'CPF'})
    if 'CPF_processado' in alunos_nao_detectados_saida.columns:
        alunos_nao_detectados_saida = alunos_nao_detectados_saida.rename(
            columns={'CPF_processado': 'CPF_Utilizado_Comparacao'})

    alunos_nao_detectados_saida.to_excel(caminho_saida, index=False, engine='openpyxl')
    print(f"\nPlanilha com alunos não detectados salva em: {caminho_saida}")
    print(
        "  Esta planilha contém alunos que tinham um CPF válido (11 dígitos) no SUAP, mas não foram encontrados com esse CPF no Pé de Meia.")

    # Opcional: Salvar lista de alunos do SUAP com CPF inválido
    # caminho_saida_invalidos_suap = os.path.join(CAMINHO_DOWNLOADS, "planilha_suap_cpfs_invalidos.xlsx")
    # colunas_invalidos_suap = ['Matrícula', 'Nome', 'CPF_original']
    # colunas_invalidos_suap_exist = [col for col in colunas_invalidos_suap if col in alunos_suap_cpf_invalido.columns]
    # if colunas_invalidos_suap_exist:
    #     alunos_suap_cpf_invalido[colunas_invalidos_suap_exist].to_excel(caminho_saida_invalidos_suap, index=False, engine='openpyxl')
    #     print(f"Planilha com alunos do SUAP com CPFs inválidos/não processáveis salva em: {caminho_saida_invalidos_suap}")


except FileNotFoundError as e:
    print(f"ERRO: Arquivo não encontrado. Verifique o caminho e o nome do arquivo: {e}")
except ValueError as e:
    print(f"ERRO de Valor: {e}")
except Exception as e:
    print(f"ERRO inesperado: {e}")
    import traceback

    traceback.print_exc()

