import pandas as pd
import os
import re  # Para extrair ano e período do nome do arquivo


def processar_e_separar_planilhas(caminho_pasta, arquivos_entrada_padrao,
                                  coluna_modalidade, valor_modalidade_eja,
                                  valor_modalidade_integrado,
                                  arquivo_saida_eja, arquivo_saida_integrado):
    """
    Lê múltiplas planilhas Excel, adiciona colunas de ano e período,
    e separa os dados em duas planilhas de saída com base na modalidade.

    Args:
        caminho_pasta (str): Caminho para a pasta com as planilhas.
        arquivos_entrada_padrao (str): Padrão para gerar nomes de arquivo (ex: "Relatorio-{ano}-{periodo}.xls").
        coluna_modalidade (str): Nome da coluna na planilha que contém a modalidade.
        valor_modalidade_eja (str): Valor na coluna_modalidade para "Técnico Integrado EJA".
        valor_modalidade_integrado (str): Valor na coluna_modalidade para "Técnico Integrado".
        arquivo_saida_eja (str): Nome do arquivo de saída para Técnico Integrado EJA.
        arquivo_saida_integrado (str): Nome do arquivo de saída para Técnico Integrado.
    """
    lista_dfs_eja = []
    lista_dfs_integrado = []
    arquivos_processados_count = 0

    print(f"Iniciando o processo na pasta: '{caminho_pasta}'")
    print(f"Buscando pela coluna de modalidade: '{coluna_modalidade}'")
    print(f"Modalidade EJA: '{valor_modalidade_eja}'")
    print(f"Modalidade Integrado: '{valor_modalidade_integrado}'\n")

    # Gerar a lista de nomes de arquivos esperados
    nomes_arquivos_entrada = []
    for ano_sufixo in range(18, 25):  # De 18 (2018) a 24 (2024)
        for periodo_num in range(1, 3):  # Períodos 1 e 2
            nomes_arquivos_entrada.append(
                arquivos_entrada_padrao.format(ano=ano_sufixo, periodo=periodo_num)
            )

    for nome_arquivo in nomes_arquivos_entrada:
        caminho_completo_arquivo = os.path.join(caminho_pasta, nome_arquivo)

        if not os.path.exists(caminho_completo_arquivo):
            print(f"AVISO: Arquivo '{nome_arquivo}' não encontrado em '{caminho_pasta}'. Pulando.")
            continue

        try:
            print(f"Processando arquivo: '{nome_arquivo}'...")
            # Extrair ano e período do nome do arquivo
            # Ex: Relatorio-18-1.xls -> ano_sufixo=18, periodo_val=1
            match = re.search(r'-(\d{2})-(\d)\.xls$', nome_arquivo)
            if not match:
                print(f"AVISO: Não foi possível extrair ano/período do nome do arquivo '{nome_arquivo}'. Pulando.")
                continue

            ano_sufixo = int(match.group(1))
            periodo_val = int(match.group(2))

            ano_letivo = 2000 + ano_sufixo
            periodo_letivo = periodo_val

            # Lê a planilha
            df = pd.read_excel(caminho_completo_arquivo, engine='xlrd')

            # Adiciona as novas colunas
            df['Ano Letivo'] = ano_letivo
            df['Período Letivo'] = periodo_letivo

            # Verifica se a coluna de modalidade existe
            if coluna_modalidade not in df.columns:
                print(
                    f"  AVISO: Coluna '{coluna_modalidade}' não encontrada em '{nome_arquivo}'. Não será possível separar por modalidade para este arquivo.")
            else:
                # Filtra para Técnico Integrado EJA
                # Mesmo que o arquivo seja X-2 (só EJA), o filtro funciona
                df_eja_temp = df[df[
                                     coluna_modalidade] == valor_modalidade_eja].copy()  # Usar .copy() para evitar SettingWithCopyWarning
                if not df_eja_temp.empty:
                    lista_dfs_eja.append(df_eja_temp)
                    print(f"  {len(df_eja_temp)} linhas adicionadas para EJA.")

                # Filtra para Técnico Integrado
                # Se o arquivo for X-2, este DataFrame estará vazio, o que é esperado.
                df_integrado_temp = df[df[coluna_modalidade] == valor_modalidade_integrado].copy()
                if not df_integrado_temp.empty:
                    lista_dfs_integrado.append(df_integrado_temp)
                    print(f"  {len(df_integrado_temp)} linhas adicionadas para Integrado.")

            arquivos_processados_count += 1

        except FileNotFoundError:  # Redundante devido à verificação os.path.exists, mas bom ter
            print(f"ERRO: Arquivo '{nome_arquivo}' não encontrado. (Esta mensagem não deveria aparecer)")
        except Exception as e:
            print(f"ERRO ao processar o arquivo '{nome_arquivo}': {e}")
        print("-" * 30)

    if not lista_dfs_eja and not lista_dfs_integrado:
        print("\nNenhum dado foi processado ou encontrado para as modalidades especificadas.")
        return

    # Salvar dados de Técnico Integrado EJA
    if lista_dfs_eja:
        df_consolidado_eja = pd.concat(lista_dfs_eja, ignore_index=True)
        caminho_completo_saida_eja = os.path.join(caminho_pasta, arquivo_saida_eja)
        try:
            df_consolidado_eja.to_excel(caminho_completo_saida_eja, index=False, engine='openpyxl')
            print(
                f"\nPlanilha consolidada para '{valor_modalidade_eja}' salva como '{caminho_completo_saida_eja}' ({len(df_consolidado_eja)} linhas).")
        except Exception as e:
            print(f"ERRO ao salvar o arquivo '{arquivo_saida_eja}': {e}")
    else:
        print(f"\nNenhum dado encontrado para a modalidade '{valor_modalidade_eja}'.")

    # Salvar dados de Técnico Integrado
    if lista_dfs_integrado:
        df_consolidado_integrado = pd.concat(lista_dfs_integrado, ignore_index=True)
        caminho_completo_saida_integrado = os.path.join(caminho_pasta, arquivo_saida_integrado)
        try:
            df_consolidado_integrado.to_excel(caminho_completo_saida_integrado, index=False, engine='openpyxl')
            print(
                f"Planilha consolidada para '{valor_modalidade_integrado}' salva como '{caminho_completo_saida_integrado}' ({len(df_consolidado_integrado)} linhas).")
        except Exception as e:
            print(f"ERRO ao salvar o arquivo '{arquivo_saida_integrado}': {e}")
    else:
        print(f"\nNenhum dado encontrado para a modalidade '{valor_modalidade_integrado}'.")

    print(f"\nTotal de arquivos de entrada processados (ou tentados): {arquivos_processados_count}")


# --- Configuração ---
PASTA_DAS_PLANILHAS = "/Users/fred/Downloads/"

# Padrão do nome dos arquivos de entrada. {ano} e {periodo} serão substituídos.
# Exemplo: Relatorio-18-1.xls
PADRAO_NOME_ARQUIVO_ENTRADA = "Relatorio-{ano}-{periodo}.xls"

# Nome da coluna em suas planilhas que identifica a modalidade do curso.
# !!! IMPORTANTE: Verifique se este é o nome correto da coluna em seus arquivos Excel !!!
NOME_COLUNA_MODALIDADE = "Modalidade"  # Exemplo: "Tipo de Curso", "Modalidade de Ensino"

# Valores exatos que aparecem na coluna NOME_COLUNA_MODALIDADE
VALOR_MODALIDADE_EJA = "Técnico Integrado EJA"
VALOR_MODALIDADE_INTEGRADO = "Técnico Integrado"

# Nomes dos arquivos de saída
NOME_ARQUIVO_SAIDA_EJA = "Consolidado_Tecnico_Integrado_EJA.xlsx"
NOME_ARQUIVO_SAIDA_INTEGRADO = "Consolidado_Tecnico_Integrado.xlsx"

# --- Execução ---
if __name__ == "__main__":
    if not os.path.isdir(PASTA_DAS_PLANILHAS):
        print(f"ERRO: A pasta especificada '{PASTA_DAS_PLANILHAS}' não existe. Verifique o caminho.")
    else:
        processar_e_separar_planilhas(
            PASTA_DAS_PLANILHAS,
            PADRAO_NOME_ARQUIVO_ENTRADA,
            NOME_COLUNA_MODALIDADE,
            VALOR_MODALIDADE_EJA,
            VALOR_MODALIDADE_INTEGRADO,
            NOME_ARQUIVO_SAIDA_EJA,
            NOME_ARQUIVO_SAIDA_INTEGRADO
        )

